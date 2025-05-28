import sys
import cv2
import socket
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
from PyQt6.QtCore import QTimer, Qt, QThread, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap

PI_IP = '192.168.125.192'  # Replace with your Raspberry Pi's IP
PI_PORT = 6000


class CommandSender(QThread):
    finished = pyqtSignal(str)

    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        try:
            with socket.create_connection((PI_IP, PI_PORT), timeout=2) as s:
                s.sendall(self.command.encode())
                response = s.recv(1024).decode()
                self.finished.emit(response)
        except Exception as e:
            self.finished.emit(f"Error: {e}")


class CameraApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Camera Switcher")

        self.label = QLabel("No Video")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.btn_cam1 = QPushButton("Cam 1")
        self.btn_cam2 = QPushButton("Cam 2")
        self.btn_stop = QPushButton("Stop")

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.btn_cam1)
        layout.addWidget(self.btn_cam2)
        layout.addWidget(self.btn_stop)
        self.setLayout(layout)

        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        self.btn_cam1.clicked.connect(lambda: self.start_stream('CAM1'))
        self.btn_cam2.clicked.connect(lambda: self.start_stream('CAM2'))
        self.btn_stop.clicked.connect(self.stop_stream)

        self.cmd_thread = None

    def send_command(self, command, callback=None):
        # If previous thread is running, wait for it to finish before starting a new one
        if self.cmd_thread and self.cmd_thread.isRunning():
            self.cmd_thread.quit()
            self.cmd_thread.wait()

        self.cmd_thread = CommandSender(command)
        if callback:
            self.cmd_thread.finished.connect(callback)
        self.cmd_thread.finished.connect(lambda resp: print("Server response:", resp))
        self.cmd_thread.start()

    def start_stream(self, cam_id):
        self.stop_stream()
        # Start command and after it's done, setup stream
        self.send_command(cam_id, lambda _: self.setup_stream(cam_id))

    def setup_stream(self, cam_id):
        port_map = {
            'CAM1': 5001,
            'CAM2': 5002,
        }
        cam_port = port_map.get(cam_id, 5001)
        QTimer.singleShot(1000, lambda: self.init_camera(cam_port))

    def init_camera(self, cam_port=5001):
        if self.cap:
            self.cap.release()

        pipeline = (
            f"udpsrc port={cam_port} caps=\"application/x-rtp, media=video, encoding-name=H264, payload=96\" ! "
            "rtph264depay ! avdec_h264 ! videoconvert ! appsink"
        )
        print("GStreamer pipeline:", pipeline)
        self.cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)

        if self.cap.isOpened():
            self.timer.start(30)
        else:
            print("Failed to open video capture")

    def update_frame(self):
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb.shape
                img = QImage(rgb.data, w, h, ch * w, QImage.Format.Format_RGB888)
                self.label.setPixmap(QPixmap.fromImage(img))
            else:
                print("Failed to read frame.")
        else:
            self.label.setText("No stream")

    def stop_stream(self):
        self.timer.stop()
        if self.cap:
            self.cap.release()
            self.cap = None
        self.send_command("STOP")
        self.label.setText("Stopped")

    def closeEvent(self, event):
        self.stop_stream()
        if self.cmd_thread and self.cmd_thread.isRunning():
            self.cmd_thread.quit()
            self.cmd_thread.wait()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = CameraApp()
    win.resize(640, 480)
    win.show()
    sys.exit(app.exec())
