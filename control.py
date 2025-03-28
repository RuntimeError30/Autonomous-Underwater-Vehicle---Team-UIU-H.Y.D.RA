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
    QFrame
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
        main_layout = QVBoxLayout(self)  # Main vertical layout

        # First Row (Camera Feed)
        first_row = QVBoxLayout()
        mainCam_label = QLabel("Camera Feed", self)
        mainCam_label.setStyleSheet("font-size: 10px; color: #d1d2d2; font-family: Montserrat;")

        self.main_cam = QLabel(self)
        self.main_cam.setFixedSize(1260, 440)
        self.main_cam.setStyleSheet("background: transparent; border: 1px solid #72eeee; border-radius: 5px;")

        # # Create the Color Detect button
        # self.detect_button = QPushButton("Color Detect", self)
        # self.layout.addWidget(self.detect_button)

        # Initialize webcam capture
        self.cap = cv2.VideoCapture(0)
        self.is_detecting = False

        # Define the color ranges for red, yellow, black, and white
        self.color_ranges = {
            'red': ((0, 100, 100), (10, 255, 255)),
            'yellow': ((20, 100, 100), (40, 255, 255)),
            'black': ((0, 0, 0), (180, 255, 50)),
            'white': ((0, 0, 200), (180, 20, 255)),
        }

        # Create a timer to continuously update the camera feed
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Refresh every 30 ms (around 33 fps)

        # Connect the button to the toggle method
        

        first_row.addWidget(mainCam_label, alignment=Qt.AlignmentFlag.AlignCenter)
        first_row.addWidget(self.main_cam, alignment=Qt.AlignmentFlag.AlignCenter)
        first_row.addStretch()

        # Second Row (Thruster Speed Section)
        second_row = QVBoxLayout()
        colfirstRow = QHBoxLayout()

        # --- Thrusters Left & Right Section ---
        thruster_section = QWidget(self)
        thruster_section.setFixedSize(250, 200)
        thruster_section.setStyleSheet(
            "background-color: rgba(114, 238, 238, 40);  border-radius: 10px;"
        )

        movementSpeed_Layout = QVBoxLayout(thruster_section)
        movementSpeed_label = QLabel("Thrusters Left & Right", self)
        movementSpeed_label.setStyleSheet("font-size: 12px; color: #d1d2d2; background-color: transparent; font-family: Montserrat;")

        moveLeft = QLabel('Thrusters 1', self)
        moveLeft.setStyleSheet("font-size: 10px; color: #d1d2d2; background-color: transparent; font-family: Montserrat;")

        movementSpeedLeft = QLabel('1590', self)
        movementSpeedLeft.setStyleSheet("font-size: 30px; color: #d1d2d2; background-color: transparent; font-family: Montserrat;")

        movemRight = QLabel('Thrusters 2', self)
        movemRight.setStyleSheet("font-size: 10px; color: #d1d2d2; background-color: transparent; font-family: Montserrat;")

        movementSpeedRight = QLabel('1590', self)
        movementSpeedRight.setStyleSheet("font-size: 30px; color: #d1d2d2; background-color: transparent; font-family: Montserrat;")

        movementSpeed_Layout.addWidget(movementSpeed_label, alignment=Qt.AlignmentFlag.AlignLeft)
        movementSpeed_Layout.addWidget(moveLeft, alignment=Qt.AlignmentFlag.AlignLeft)
        movementSpeed_Layout.addWidget(movementSpeedLeft, alignment=Qt.AlignmentFlag.AlignLeft)
        movementSpeed_Layout.addWidget(movemRight, alignment=Qt.AlignmentFlag.AlignLeft)
        movementSpeed_Layout.addWidget(movementSpeedRight, alignment=Qt.AlignmentFlag.AlignLeft)



        # --- Thrusters Direction Section ---
        direction_task_layout = QVBoxLayout()


        # --- Thrusters Direction Section ---
        thruster_direction_section = QWidget(self)
        thruster_direction_section.setFixedSize(250, 100)
        thruster_direction_section.setStyleSheet(
            "background-color: rgba(114, 238, 238, 40);"
        )
        
        thruster_direction_Layout = QVBoxLayout(thruster_direction_section)
        thruster_direction_label = QLabel("Thrusters Direction", self)
        thruster_direction_label.setStyleSheet("font-size: 10px; color: #d1d2d2; background-color: transparent; font-family: Montserrat;")
        moveForward = QLabel('Forward', self)
        moveForward.setStyleSheet("font-size: 20px; color: #d1d2d2; background-color: transparent; font-family: Montserrat;")


        thruster_direction_Layout.addWidget(thruster_direction_label, alignment=Qt.AlignmentFlag.AlignCenter)
        thruster_direction_Layout.addStretch()
        thruster_direction_Layout.addWidget(moveForward, alignment=Qt.AlignmentFlag.AlignCenter)
        thruster_direction_Layout.addStretch()

        direction_task_layout.addWidget(thruster_direction_section)
        direction_task_layout.addStretch()

        # Tasks button section
        tasks_button_section = QWidget(self)
        tasks_button_section.setFixedSize(250, 150)
        tasks_button_section.setStyleSheet(
            "background-color: rgba(114, 238, 238, 40);"
        )
        tasks_button_Layout = QVBoxLayout(tasks_button_section)
        tasks_button_label = QLabel("Perform Tasks", self)
        tasks_button_label.setStyleSheet("font-size: 10px; color: #d1d2d2; background-color: transparent; font-family: Montserrat;")

        task1_button = QPushButton("Capture Panorama", self)
        task1_button.setStyleSheet("font-size: 10px; color: #d1d2d2; background-color: rgba(114, 238, 238, 40); font-family: Montserrat;")
        task1_button.setFixedSize(200, 40)
        task1_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.task2_button = QPushButton("Recognize Cargo", self)
        self.task2_button.setStyleSheet("font-size: 10px; color: #d1d2d2; background-color: rgba(114, 238, 238, 40); margin-top:20px; font-family: Montserrat;")
        self.task2_button.setFixedSize(200, 40)
        self.task2_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.task2_button.clicked.connect(self.toggle_detection)


        tasks_button_Layout.addWidget(tasks_button_label, alignment=Qt.AlignmentFlag.AlignCenter)

        tasks_button_Layout.addWidget(task1_button, alignment=Qt.AlignmentFlag.AlignCenter)
        tasks_button_Layout.addWidget(self.task2_button, alignment=Qt.AlignmentFlag.AlignCenter)

        tasks_button_Layout.addStretch()
        direction_task_layout.addWidget(tasks_button_section)
        direction_task_layout.addStretch()



        # --- Thrusters Up & Down Section ---
        updownthruster_section = QWidget(self)
        updownthruster_section.setFixedSize(250, 200)
        updownthruster_section.setStyleSheet(
            "background-color: rgba(114, 238, 238, 40); border-radius: 10px; "
        )

        updownSpeed_Layout = QVBoxLayout(updownthruster_section)
        updown_movementSpeed_label = QLabel("Thrusters Up & Down", self)
        updown_movementSpeed_label.setStyleSheet("font-size: 12px; background-color: transparent;  font-family: Montserrat;")

        moveUp = QLabel('Thrusters 5', self)
        moveUp.setStyleSheet("font-size: 10px; color: #d1d2d2; background-color: transparent; font-family: Montserrat;")

        movementSpeedUp = QLabel('1590', self)
        movementSpeedUp.setStyleSheet("font-size: 30px; color: #d1d2d2; background-color: transparent; font-family: Montserrat;")

        moveDown = QLabel('Thrusters 8', self)
        moveDown.setStyleSheet("font-size: 10px; color: #d1d2d2; background-color: transparent; font-family: Montserrat;")

        movementSpeedDown = QLabel('1590', self)
        movementSpeedDown.setStyleSheet("font-size: 30px; color: #d1d2d2; background-color: transparent; font-family: Montserrat;")

        updownSpeed_Layout.addWidget(updown_movementSpeed_label, alignment=Qt.AlignmentFlag.AlignLeft)
        updownSpeed_Layout.addWidget(moveUp, alignment=Qt.AlignmentFlag.AlignLeft)
        updownSpeed_Layout.addWidget(movementSpeedUp, alignment=Qt.AlignmentFlag.AlignLeft)
        updownSpeed_Layout.addWidget(moveDown, alignment=Qt.AlignmentFlag.AlignLeft)
        updownSpeed_Layout.addWidget(movementSpeedDown, alignment=Qt.AlignmentFlag.AlignLeft)

        # Add both sections to the second row
        colfirstRow.addWidget(thruster_section)
        colfirstRow.addSpacing(20)
        colfirstRow.addLayout(direction_task_layout)
        colfirstRow.addSpacing(20)
        colfirstRow.addWidget(updownthruster_section)
        colfirstRow.addSpacing(20)
  
        second_row.addLayout(colfirstRow)

        # Add rows to main layout
        main_layout.addLayout(first_row)
        main_layout.addSpacing(20)
        main_layout.addLayout(second_row)
        main_layout.addStretch()

        self.setLayout(main_layout)

# Color detection Code
    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            if self.is_detecting:
                frame = self.detect_colors(frame)

            # Convert the frame to RGB (OpenCV uses BGR by default)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert to QImage and set it on the QLabel
            h, w, c = rgb_frame.shape
            q_img = QImage(rgb_frame.data, w, h, c * w, QImage.Format.Format_RGB888)
            self.main_cam.setPixmap(QPixmap.fromImage(q_img))

    def detect_colors(self, frame):
        # Convert the image to HSV color space
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        for color, (lower, upper) in self.color_ranges.items():
            # Create mask for each color range
            lower_bound = np.array(lower)
            upper_bound = np.array(upper)
            mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)

            # Apply Gaussian blur to smooth the mask
            mask = cv2.GaussianBlur(mask, (5, 5), 0)

            # Morphological operations to remove small noise and fill gaps
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # Close gaps
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)  # Remove noise

            # Find contours of the detected color
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                if cv2.contourArea(contour) > 500:  # Filter out small contours
                    # Get the bounding box
                    x, y, w, h = cv2.boundingRect(contour)
                    # Draw the bounding box and label the color
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, color, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        return frame

    def toggle_detection(self):
        # Toggle the color detection state
        self.is_detecting = not self.is_detecting
        print(f"Color Detection is now: {'ON' if self.is_detecting else 'OFF'}")  # Debug print to verify state
        if self.is_detecting:
            self.task2_button.setText("Stop Detection")
        else:
            self.task2_button.setText("Cargo Detection")


    def closeEvent(self, event):
        # Release the webcam capture when closing the application
        self.cap.release()
        event.accept()



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