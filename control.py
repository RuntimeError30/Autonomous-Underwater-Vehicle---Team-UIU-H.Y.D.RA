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
from PyQt6.QtGui import QPixmap, QImage, QPainter, QBrush, QColor, QPainterPath, QKeyEvent
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
        
        small_frame = QLabel()
        small_frame.setStyleSheet("background-color: transparent; border: 1px solid #005767; border-radius: 20px; margin-bottom: 10px;")
        small_frame.setFixedSize(384, 216)

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

        frame_buttonLayout.addWidget(small_frame)
        frame_buttonLayout.addWidget(camerabtn_label)
        frame_buttonLayout.addWidget(camera01_btn)
        frame_buttonLayout.addWidget(camera02_btn)
        frame_buttonLayout.addStretch()


        # Main camera display
        main_camera = QLabel()
        main_camera.setFixedSize(960, 540)
        main_camera.setStyleSheet("background-color: transparent; border: 1px solid #005767; border-radius: 20px;")



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



        thrusterstatus_layout.addWidget(status_container)
        thrusterstatus_layout.addStretch()

        # Control Status

        pwm_layout = QVBoxLayout()
        
        control_status = QWidget()
        control_status.setStyleSheet("""
            background-color:
            #181818;
            border: 1px solid #0D363E;
            border-radius: 10px;
            padding: 10px;
        """)

        main_row.addLayout(frame_buttonLayout)
        main_row.addWidget(main_camera)
        main_row.addLayout(thrusterstatus_layout)

        main_row.addStretch()
        

        # Add rows to main layout
        main_layout.addLayout(main_row)
        main_layout.addStretch()

        self.setLayout(main_layout)

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



    def send_command(self, command):
        """Send command to Raspberry Pi MAVProxy server"""
        HOST = "192.168.2.3"  # Change if necessary
        PORT = 7000

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((HOST, PORT))
                client_socket.sendall(command.encode())
                print(f"Sent: {command}")
        except Exception as e:
            print(f"Error sending command: {e}")

    def keyPressEvent(self, event: QKeyEvent):
        """Handle keyboard input"""
        key_map = {
            Qt.Key.Key_W: ["rc 3 1000", "rc 4 1000"],  # Forward
            Qt.Key.Key_S: ["rc 3 2000", "rc 4 2000"],  # Backward
            Qt.Key.Key_A: ["rc 1 2000", "rc 2 2000"],  # Left
            Qt.Key.Key_D: ["rc 1 1000", "rc 2 1000"],  # Right
            Qt.Key.Key_Up: ["rc 5 1000", "rc 6 1000"],  # Up Tilt
            Qt.Key.Key_Down: ["rc 5 2000", "rc 6 2000"],  # Down Tilt
            Qt.Key.Key_U: ["rc 5 1000", "rc 8 2000"],  # Up Normal
        }

        if event.key() in key_map:
            commands = key_map[event.key()]
            for command in commands:
                if command not in self.active_commands:
                    self.active_commands.append(command)
                self.send_command(command)
                self.last_command_time = time.time()

        elif event.key() == Qt.Key.Key_Q:  # Reset command
            self.reset_commands()

    def joystick_init(self):
        """Initialize joystick"""
        pygame.init()
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            print("Joystick Connected!")
        else:
            self.joystick = None
            print("No Joystick Found!")

    def read_joystick(self):
        """Read joystick input and send appropriate RC commands"""
        if not self.joystick:
            return

        pygame.event.pump()

        # Axis values
        axis_0 = self.joystick.get_axis(0)  # Left/Right
        axis_1 = self.joystick.get_axis(1)  # Forward/Backward
        axis_5 = self.joystick.get_axis(3)  # Up/Down
        axis_4 = self.joystick.get_axis(4)  # Forward Tilt

        # Button states
        reset_button = self.joystick.get_button(0)  # Reset Hover
        stop_button = self.joystick.get_button(9)  # Stop everything
        send_arm = self.joystick.get_button(0)  # Arm/Disarm
        close_arm = self.joystick.get_button(1)  # Close Arm

        commands = []

        # Forward/Backward
        if axis_1 > 0.03:
            value_3 = int(1550 - (axis_1 * 450))
            value_4 = int(1450 + (axis_1 * 450))
            commands.append(f"rc 3 {value_3}")
            commands.append(f"rc 4 {value_4}")

        elif axis_1 < -0.03:
            value_3 = int(1450 - (axis_1 * 450))
            value_4 = int(1550 + (axis_1 * 450))
            commands.append(f"rc 3 {value_3}")
            commands.append(f"rc 4 {value_4}")

        else:
            commands.append("rc 3 1500")
            commands.append("rc 4 1500")

        # Left/Right
        if axis_0 > 0.3:
            value = int(1450 + (axis_0 * 450))
            commands.append(f"rc 1 {value}")
            commands.append(f"rc 2 {value}")

        elif axis_0 < -0.3:
            value = int(1550 - (-axis_0 * 450))
            commands.append(f"rc 1 {value}")
            commands.append(f"rc 2 {value}")

        else:
            commands.append("rc 1 1500")
            commands.append("rc 2 1500")

        # Up/Down
        if axis_5 > 0.03:
            thrust = int(1500 + (axis_5 * 500))
            thrust2 = int(1500 - (axis_5 * 500))
            commands.append(f"rc 5 {thrust2}")
            commands.append(f"rc 8 {thrust}")

        elif axis_5 < -0.03:
            thrust = int(1500 - (abs(axis_5) * 500))
            commands.append(f"rc 5 {thrust}")
            commands.append(f"rc 8 {thrust}")

        else:
            commands.append("rc 5 1500")
            commands.append("rc 6 1500")
            commands.append("rc 7 1500")
            commands.append("rc 8 1500")

        # Reset Hover
        if reset_button:
            commands.append("rc 5 1500")
            commands.append("rc 6 1500")
            commands.append("rc 7 1500")
            commands.append("rc 8 1500")

        # Arm Commands
        if send_arm:
            commands.append("open")
        elif close_arm:
            commands.append("close")

        # Stop Everything
        if stop_button:
            commands.extend([
                "rc 3 1500", "rc 4 1500", "rc 1 1500", "rc 2 1500",
                "rc 5 1500", "rc 6 1500", "rc 8 1500"
            ])

        # Throttle sending commands based on time delay
        current_time = time.time()
        if current_time - self.last_command_time > self.command_delay:
            for command in commands:
                if command not in self.active_commands:
                    self.active_commands.append(command)
                self.send_command(command)
            self.last_command_time = current_time

    def reset_commands(self):
        """Reset all RC commands"""
        reset_commands = ["rc 1 1500", "rc 2 1500", "rc 3 1500", "rc 4 1500",
                          "rc 5 1500", "rc 6 1500", "rc 8 1500"]
        for command in reset_commands:
            self.send_command(command)
        self.active_commands.clear()