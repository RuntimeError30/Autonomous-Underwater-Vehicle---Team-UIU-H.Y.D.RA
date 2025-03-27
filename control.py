import time
import psutil
import serial
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
from PyQt6.QtGui import QPixmap, QImage, QPainter, QBrush, QColor, QPainterPath
from PyQt6.QtCore import Qt, QRectF, QTimer
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class ControlPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)  # Main vertical layout

        # First Row (Camera Feed)
        first_row = QVBoxLayout()
        mainCam_label = QLabel("Camera Feed", self)
        mainCam_label.setStyleSheet("font-size: 10px; color: #d1d2d2; font-family: Montserrat;")

        main_cam = QLabel(self)
        main_cam.setFixedSize(1260, 440)
        main_cam.setStyleSheet("background: transparent; border: 1px solid #72eeee; border-radius: 5px;")

        first_row.addWidget(mainCam_label, alignment=Qt.AlignmentFlag.AlignCenter)
        first_row.addWidget(main_cam, alignment=Qt.AlignmentFlag.AlignCenter)
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
        tasks_button_section.setFixedSize(250, 100)
        tasks_button_section.setStyleSheet(
            "background-color: rgba(114, 238, 238, 40);"
        )
        tasks_button_Layout = QVBoxLayout(tasks_button_section)
        tasks_button_label = QLabel("Perform Tasks", self)
        tasks_button_label.setStyleSheet("font-size: 10px; color: #d1d2d2; background-color: transparent; font-family: Montserrat;")

        task1_button = QPushButton("Capture Panorama", self)
        task1_button.setStyleSheet("font-size: 20px; color: #d1d2d2; background-color: transparent; font-family: Montserrat;")
        task1_button.setFixedSize(200, 40)

        tasks_button_Layout.addWidget(tasks_button_label, alignment=Qt.AlignmentFlag.AlignCenter)
        tasks_button_Layout.addStretch()
        tasks_button_Layout.addWidget(task1_button, alignment=Qt.AlignmentFlag.AlignCenter)

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
