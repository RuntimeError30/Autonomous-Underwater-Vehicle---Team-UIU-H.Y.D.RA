import time
import numpy as np
import psutil
import socket
import serial
import cv2
import pygame
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QProgressBar,
    QSpacerItem,
    QSizePolicy,
    QSlider,
    QFrame,
    QGraphicsOpacityEffect
)
from PyQt6.QtGui import QPixmap, QImage, QPainter, QBrush, QColor, QPainterPath, QKeyEvent, QPixmap
from PyQt6.QtCore import Qt, QRectF, QTimer
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class ControlPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.active_commands = []  # Store active commands
        self.joystick_init()  # Initialize joystick
        self.timer = QTimer(self)  
        self.timer.timeout.connect(self.read_joystick)  
        self.timer.start(50)  # Read joystick every 50ms
        self.last_command_time = 0
        self.command_delay = 0.1  

    def init_ui(self):
        main_layout = QVBoxLayout(self) 

        main_row = QHBoxLayout()

        frame_buttonLayout = QVBoxLayout()
        
        self.small_frame = QLabel()
        self.small_frame.setStyleSheet(" border: 1px solid #005767; border-radius: 20px; margin-bottom: 10px;")
        self.small_frame.setFixedSize(384, 216)

        camerabtn_label = QLabel("SWITCH CAMERAS")
        camerabtn_label.setStyleSheet("""color: white; font-size: 12px; font-weight: bold; margin-top: 20px;""")
        opacity_effect = QGraphicsOpacityEffect()
        camerabtn_label.setGraphicsEffect(opacity_effect)
        opacity_effect.setOpacity(0.6)  # Set opacity for the label

        camera01_btn = QPushButton("Camera 01")
        camera01_btn.setFixedSize(150, 50)
        camera01_btn.setStyleSheet("""
            background-color: transparent;
            color: white;
            font-size: 10px;
            padding: 5px;
            border: 1px solid #FF8800;
            border-radius: 5px;
            margin-top: 10px;
            
        """)

        camera02_btn = QPushButton("Camera 02")
        camera02_btn.setFixedSize(150, 50)
        camera02_btn.setStyleSheet("""
            background-color: transparent;
            color: white;
            font-size: 10px;
            padding: 5px;
            border: 1px solid #FF8800;
            border-radius: 5px;
            margin-top: 10px;
            
        """)

        frame_buttonLayout.addWidget(self.small_frame)
        frame_buttonLayout.addWidget(camerabtn_label)
        frame_buttonLayout.addWidget(camera01_btn)
        frame_buttonLayout.addWidget(camera02_btn)
        frame_buttonLayout.addStretch()


        # Main camera display
        self.main_camera = QLabel()
        self.main_camera.setFixedSize(960, 540)
        self.main_camera.setStyleSheet(" border: 1px solid #005767; border-radius: 20px;")



        # Thrusters and Status
        thrusterstatus_layout = QVBoxLayout()


        status_container = QWidget()
        status_container.setStyleSheet("""
            background-color: #181818;
            border: 1px solid #0D363E;
            border-radius: 10px;
            padding: 10px;
        """)
        container_layout = QVBoxLayout()

        # Create and style the label inside
        status_label = QLabel("Communication Status")
        status_label.setStyleSheet("""
            color: white;
            font-size: 8px;
            border: none;
        """)
        conn_label = QLabel("CONNECTED")
        conn_label.setStyleSheet("""
            color: #FF8800;
            font-size: 20px;
            height: 30px;
            border: none;
        """)
        ip_label = QLabel("IP ADDRESS: 192.168.2.3")
        ip_label.setStyleSheet("""
            color: white;
            font-size: 8px;
            border: none;
        """)
        container_layout.addWidget(status_label)
        container_layout.addWidget(conn_label)
        container_layout.addWidget(ip_label)
        status_container.setLayout(container_layout)
        status_container.setFixedSize(400, 130)


        # Create thruster buttons
        control_status = QWidget()
        control_status.setStyleSheet("""
            background-color:
            #181818;
            border: 1px solid #0D363E;
            border-radius: 10px;
            padding: 10px;
        """)

        control_layout = QVBoxLayout()

        main_label = QLabel("DIRECTION")
        main_label.setStyleSheet("""
            color: white;
            font-size: 8px;
            border: none;
        """)

        dir_status = QLabel("NEUTRAL")
        dir_status.setStyleSheet("""
            color: #FF8800;
            font-size: 20px;
            border: none;
        """)

        
        up_label = QLabel("UP/DOWN")
        up_label.setStyleSheet("""
            color: white;
            font-size: 8px;
            border: none;
        """)

        thruster2_Layout = QHBoxLayout()
        thruster2_label = QLabel("THRUSTER 2")
        thruster2_label.setStyleSheet("""
            color: white;
            border: none;
        """)
        thruster2 = QLabel("0")
        thruster2.setStyleSheet("""
            color: #FF8800;
        """)
        thruster2_Layout.addWidget(thruster2_label)
        thruster2_Layout.addWidget(thruster2)

        thruster3_layout = QHBoxLayout()
        thruster3_label = QLabel("THRUSTER 3")
        thruster3_label.setStyleSheet("""
            color: white;
            border: none;
        """)
        thruster3_value = QLabel("0")
        thruster3_value.setStyleSheet("""
            color: #FF8800;

        """)
        thruster3_layout.addWidget(thruster3_label)
        thruster3_layout.addWidget(thruster3_value)

        thruster6_layout = QHBoxLayout()
        thruster6_label = QLabel("THRUSTER 6")
        thruster6_label.setStyleSheet("""
            color: white;
            border: none;
        """)
        thruster6_value = QLabel("0")
        thruster6_value.setStyleSheet("""
            color: #FF8800;
        """)
        thruster6_layout.addWidget(thruster6_label)
        thruster6_layout.addWidget(thruster6_value)

        thruster7_layout = QHBoxLayout()
        thruster7_label = QLabel("THRUSTER 7")
        thruster7_label.setStyleSheet("""
            border: none;
        """)
        thruster7_value = QLabel("0")
        thruster7_value.setStyleSheet("""
            color: #FF8800;

        """)
        thruster7_layout.addWidget(thruster7_label)
        thruster7_layout.addWidget(thruster7_value)

        fwd_label = QLabel("FORWARD/BACKWARD")
        fwd_label.setStyleSheet("""
            font-size: 8px;
            border: none;
        """)

        # Thruster 1
        thruster1_layout = QHBoxLayout()
        thruster1_label = QLabel("THRUSTER 1")
        thruster1_label.setStyleSheet("""
            color: white;
            border: none;
        """)
        thruster1_value = QLabel("0")
        thruster1_value.setStyleSheet("""
            color: #FF8800;
        """)
        thruster1_layout.addWidget(thruster1_label)
        thruster1_layout.addWidget(thruster1_value)

        # Thruster 4
        thruster4_layout = QHBoxLayout()
        thruster4_label = QLabel("THRUSTER 4")
        thruster4_label.setStyleSheet("""
            color: white;
            border: none;
        """)
        thruster4_value = QLabel("0")
        thruster4_value.setStyleSheet("""
            color: #FF8800;
        """)
        thruster4_layout.addWidget(thruster4_label)
        thruster4_layout.addWidget(thruster4_value)

        # Thruster 5
        thruster5_layout = QHBoxLayout()
        thruster5_label = QLabel("THRUSTER 5")
        thruster5_label.setStyleSheet("""
            color: white;
            border: none;
        """)
        thruster5_value = QLabel("0")
        thruster5_value.setStyleSheet("""
            color: #FF8800;
        """)
        thruster5_layout.addWidget(thruster5_label)
        thruster5_layout.addWidget(thruster5_value)

        # Thruster 8
        thruster8_layout = QHBoxLayout()
        thruster8_label = QLabel("THRUSTER 8")
        thruster8_label.setStyleSheet("""
            color: white;
            border: none;
        """)
        thruster8_value = QLabel("0")
        thruster8_value.setStyleSheet("""
            color: #FF8800;
        """)
        thruster8_layout.addWidget(thruster8_label)
        thruster8_layout.addWidget(thruster8_value)


        control_layout.addWidget(main_label)
        control_layout.addWidget(dir_status)
        control_layout.addWidget(up_label)

        control_layout.addLayout(thruster2_Layout)
        control_layout.addLayout(thruster3_layout)
        control_layout.addLayout(thruster6_layout)
        control_layout.addLayout(thruster7_layout)

        control_layout.addWidget(fwd_label)
        control_layout.addLayout(thruster1_layout)
        control_layout.addLayout(thruster4_layout)
        control_layout.addLayout(thruster5_layout)
        control_layout.addLayout(thruster8_layout)
        


        control_status.setLayout(control_layout)

        thrusterstatus_layout.addWidget(status_container)
        thrusterstatus_layout.addWidget(control_status)
        thrusterstatus_layout.addStretch()


        main_row.addLayout(frame_buttonLayout)
        main_row.addWidget(self.main_camera, alignment=Qt.AlignmentFlag.AlignTop)
        main_row.addLayout(thrusterstatus_layout)
        

        main_row.addStretch()

        second_row = QHBoxLayout()

        sensor_layout = QVBoxLayout()
        
        sensor_label = QLabel("SENSORS")
        sensor_label.setStyleSheet("""font-size: 12px; font-weight: bold; color: white; margin-bottom: 40px;""")
        
        depth_layout = QHBoxLayout()
        depth_label = QLabel("DEPTH")
        depth_value = QLabel("0 m")
        depth_value.setStyleSheet("border: 1px solid #0D363E; border-radius: 5px; padding: 10px; color: #FF8800;")
        depth_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        depth_label.setStyleSheet("color: white; font-size: 8px;")
        depth_layout.addWidget(depth_label)
        depth_layout.addWidget(depth_value)

        temp_layout = QHBoxLayout()
        temp_label = QLabel("TEMPERATURE")
        temp_value = QLabel("0 °C")
        temp_value.setStyleSheet("border: 1px solid #0D363E; border-radius: 5px; padding: 10px; color: #FF8800;")
        temp_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        temp_layout.addWidget(temp_label)
        temp_layout.addWidget(temp_value)

        pressure_layout = QHBoxLayout()
        pressure_label = QLabel("PRESSURE")
        pressure_value = QLabel("0 Pa")
        pressure_value.setStyleSheet("border: 1px solid #0D363E; border-radius: 5px; padding: 10px; color: #FF8800;")
        pressure_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pressure_layout.addWidget(pressure_label)
        pressure_layout.addWidget(pressure_value)

        sensor_layout.addWidget(sensor_label)
        sensor_layout.addLayout(depth_layout)
        sensor_layout.addLayout(temp_layout)
        sensor_layout.addLayout(pressure_layout)
        sensor_layout.addStretch()

        #leak and Emergency Alarm

        alarm_layout = QVBoxLayout()

        leak_label = QLabel("LEAK ALARM")
        leak_label.setStyleSheet("color: 4F4F4F; background: #4F4F4F; font-size: 10px;border-radius: 50px; padding: 10px; color: white;")
        leak_label.setFixedSize(100, 100)
        leak_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        emergency_label = QPushButton("EMERGENCY")
        emergency_label.setStyleSheet("border: 1px solid red; border-radius: 5px; padding: 10px; color: red; font-size: 10px; background-color: transparent;")


        alarm_layout.addWidget(leak_label)
        alarm_layout.addWidget(emergency_label) 
        alarm_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)


        joystick_layout = QVBoxLayout()
        image1_label = QLabel()
        pixmap1 = QPixmap("Autonomous-Underwater-Vehicle---Team-UIU-H.Y.D.RA/assets/joystick.png")  
        image1_label.setPixmap(pixmap1)

        joystick_layout2 = QVBoxLayout()
        image2_label = QLabel()
        pixmap2 = QPixmap("Autonomous-Underwater-Vehicle---Team-UIU-H.Y.D.RA/assets/joystick.png")  
        image2_label.setPixmap(pixmap1)

        label1 = QLabel("ARM JOYSTICK")
        label1.setStyleSheet("font-size: 10px;")
        conn_joystick1 = QLabel("XBox 360 Controller")
        conn_joystick1.setStyleSheet("font-size: 20px; color: #FF8800")

        label2 = QLabel("ARM JOYSTICK")
        label2.setStyleSheet("font-size: 10px;")
        conn_joystick2 = QLabel("XBox 360 Controller")
        conn_joystick2.setStyleSheet("font-size: 20px; color: #FF8800")

        joystick_layout.addWidget(image1_label)
        joystick_layout.addWidget(label1)
        joystick_layout.addWidget(conn_joystick1)

        joystick_layout2.addWidget(image2_label)
        joystick_layout2.addWidget(label2)
        joystick_layout2.addWidget(conn_joystick2)

        taske_layout = QVBoxLayout()
        

        
        second_row.addLayout(sensor_layout)
        second_row.addLayout(alarm_layout)
        second_row.addLayout(joystick_layout)
        second_row.addLayout(joystick_layout2)
        
        # Add rows to main layout
        main_layout.addLayout(main_row)
        main_layout.addLayout(second_row)
        main_layout.addStretch()






        # Camera functions
        # GStreamer pipelines
        self.cap0 = cv2.VideoCapture(
            'udpsrc port=5000 caps="application/x-rtp, media=video, encoding-name=H264, payload=96" ! '
            'rtph264depay ! avdec_h264 ! videoconvert ! appsink',
            cv2.CAP_GSTREAMER)

        self.cap1 = cv2.VideoCapture(
            'udpsrc port=5001 caps="application/x-rtp, media=video, encoding-name=H264, payload=97" ! '
            'rtph264depay ! avdec_h264 ! videoconvert ! appsink',
            cv2.CAP_GSTREAMER)
        
        # Timers to update feeds
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frames)
        self.timer.start(30)

        self.setLayout(main_layout)

    def update_frames(self):
        self.show_frame(self.cap0, self.small_frame)
        self.show_frame(self.cap1, self.main_camera)

    def show_frame(self, cap, label):
        ret, frame = cap.read()
        if ret:
            # Convert BGR to RGB
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            self.small_frame.setPixmap(QPixmap.fromImage(qt_image))
        else:
            self.small_frame.setText("No feed")

# # Color detection Code
#     def update_frame(self):
#         ret, frame = self.cap.read()
#         if ret:
#             if self.is_detecting:
#                 frame = self.detect_colors(frame)

#             # Convert the frame to RGB (OpenCV uses BGR by default)
#             rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#             # Convert to QImage and set it on the QLabel
#             h, w, c = rgb_frame.shape
#             q_img = QImage(rgb_frame.data, w, h, c * w, QImage.Format.Format_RGB888)
#             self.main_cam.setPixmap(QPixmap.fromImage(q_img))

#     def detect_colors(self, frame):
#         # Convert the image to HSV color space
#         hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

#         for color, (lower, upper) in self.color_ranges.items():
#             # Create mask for each color range
#             lower_bound = np.array(lower)
#             upper_bound = np.array(upper)
#             mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)

#             # Apply Gaussian blur to smooth the mask
#             mask = cv2.GaussianBlur(mask, (5, 5), 0)

#             # Morphological operations to remove small noise and fill gaps
#             kernel = np.ones((5, 5), np.uint8)
#             mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # Close gaps
#             mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)  # Remove noise

#             # Find contours of the detected color
#             contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#             for contour in contours:
#                 if cv2.contourArea(contour) > 500:  # Filter out small contours
#                     # Get the bounding box
#                     x, y, w, h = cv2.boundingRect(contour)
#                     # Draw the bounding box and label the color
#                     cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#                     cv2.putText(frame, color, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

#         return frame

#     def toggle_detection(self):
#         # Toggle the color detection state
#         self.is_detecting = not self.is_detecting
#         print(f"Color Detection is now: {'ON' if self.is_detecting else 'OFF'}")  # Debug print to verify state
#         if self.is_detecting:
#             self.task2_button.setText("Stop Detection")
#         else:
#             self.task2_button.setText("Cargo Detection")


#     def closeEvent(self, event):
#         # Release the webcam capture when closing the application
#         self.cap.release()
#         event.accept()



    # def send_command(self, command):
    #     """Send command to Raspberry Pi MAVProxy server"""
    #     HOST = "192.168.125.27"  # Change if necessary
    #     PORT = 7000

    #     try:
    #         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    #             client_socket.connect((HOST, PORT))
    #             client_socket.sendall(command.encode())
    #             print(f"Sent: {command}")
    #     except Exception as e:
    #         print(f"Error sending command: {e}")

    # def keyPressEvent(self, event: QKeyEvent):
    #     """Handle keyboard input"""
    #     key_map = {
    #         Qt.Key.Key_W: ["rc 3 1000", "rc 4 1000"],  # Forward
    #         Qt.Key.Key_S: ["rc 3 2000", "rc 4 2000"],  # Backward
    #         Qt.Key.Key_A: ["rc 1 2000", "rc 2 2000"],  # Left
    #         Qt.Key.Key_D: ["rc 1 1000", "rc 2 1000"],  # Right
    #         Qt.Key.Key_Up: ["rc 5 1000", "rc 6 1000"],  # Up Tilt
    #         Qt.Key.Key_Down: ["rc 5 2000", "rc 6 2000"],  # Down Tilt
    #         Qt.Key.Key_U: ["rc 5 1000", "rc 8 2000"],  # Up Normal
    #     }

    #     if event.key() in key_map:
    #         commands = key_map[event.key()]
    #         for command in commands:
    #             if command not in self.active_commands:
    #                 self.active_commands.append(command)
    #             self.send_command(command)
    #             self.last_command_time = time.time()

    #     elif event.key() == Qt.Key.Key_Q:  # Reset command
    #         self.reset_commands()

    # def joystick_init(self):
    #     """Initialize joystick"""
    #     pygame.init()
    #     pygame.joystick.init()
    #     if pygame.joystick.get_count() > 0:
    #         self.joystick = pygame.joystick.Joystick(0)
    #         self.joystick.init()
    #         print("Joystick Connected!")
    #     else:
    #         self.joystick = None
    #         print("No Joystick Found!")

    # def read_joystick(self):
    #     """Read joystick input and send appropriate RC commands"""
    #     if not self.joystick:
    #         return

    #     pygame.event.pump()

    #     # Axis values
    #     axis_0 = self.joystick.get_axis(0)  # Left/Right
    #     axis_1 = self.joystick.get_axis(1)  # Forward/Backward
    #     axis_5 = self.joystick.get_axis(3)  # Up/Down
    #     axis_4 = self.joystick.get_axis(4)  # Forward Tilt

    #     # Button states
    #     reset_button = self.joystick.get_button(0)  # Reset Hover
    #     stop_button = self.joystick.get_button(9)  # Stop everything
    #     send_arm = self.joystick.get_button(0)  # Arm/Disarm
    #     close_arm = self.joystick.get_button(1)  # Close Arm

    #     commands = []

    #     # Forward/Backward
    #     if axis_1 > 0.03:
    #         value_3 = int(1550 - (axis_1 * 450))
    #         value_4 = int(1450 + (axis_1 * 450))
    #         commands.append(f"rc 3 {value_3}")
    #         commands.append(f"rc 4 {value_4}")

    #     elif axis_1 < -0.03:
    #         value_3 = int(1450 - (axis_1 * 450))
    #         value_4 = int(1550 + (axis_1 * 450))
    #         commands.append(f"rc 3 {value_3}")
    #         commands.append(f"rc 4 {value_4}")

    #     else:
    #         commands.append("rc 3 1500")
    #         commands.append("rc 4 1500")

    #     # Left/Right
    #     if axis_0 > 0.3:
    #         value = int(1450 + (axis_0 * 450))
    #         commands.append(f"rc 1 {value}")
    #         commands.append(f"rc 2 {value}")

    #     elif axis_0 < -0.3:
    #         value = int(1550 - (-axis_0 * 450))
    #         commands.append(f"rc 1 {value}")
    #         commands.append(f"rc 2 {value}")

    #     else:
    #         commands.append("rc 1 1500")
    #         commands.append("rc 2 1500")

    #     # Up/Down
    #     if axis_5 > 0.03:
    #         thrust = int(1500 + (axis_5 * 500))
    #         thrust2 = int(1500 - (axis_5 * 500))
    #         commands.append(f"rc 5 {thrust2}")
    #         commands.append(f"rc 8 {thrust}")

    #     elif axis_5 < -0.03:
    #         thrust = int(1500 - (abs(axis_5) * 500))
    #         commands.append(f"rc 5 {thrust}")
    #         commands.append(f"rc 8 {thrust}")

    #     else:
    #         commands.append("rc 5 1500")
    #         commands.append("rc 6 1500")
    #         commands.append("rc 7 1500")
    #         commands.append("rc 8 1500")

    #     # Reset Hover
    #     if reset_button:
    #         commands.append("rc 5 1500")
    #         commands.append("rc 6 1500")
    #         commands.append("rc 7 1500")
    #         commands.append("rc 8 1500")

    #     # Arm Commands
    #     if send_arm:
    #         commands.append("open")
    #     elif close_arm:
    #         commands.append("close")

    #     # Stop Everything
    #     if stop_button:
    #         commands.extend([
    #             "rc 3 1500", "rc 4 1500", "rc 1 1500", "rc 2 1500",
    #             "rc 5 1500", "rc 6 1500", "rc 8 1500"
    #         ])

    #     # Throttle sending commands based on time delay
    #     current_time = time.time()
    #     if current_time - self.last_command_time > self.command_delay:
    #         for command in commands:
    #             if command not in self.active_commands:
    #                 self.active_commands.append(command)
    #             self.send_command(command)
    #         self.last_command_time = current_time

    # def reset_commands(self):
    #     """Reset all RC commands"""
    #     reset_commands = ["rc 1 1500", "rc 2 1500", "rc 3 1500", "rc 4 1500",
    #                       "rc 5 1500", "rc 6 1500", "rc 8 1500"]
    #     for command in reset_commands:
    #         self.send_command(command)
    #     self.active_commands.clear()