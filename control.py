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

        # Thruster section layout with background
        movementSpeed_Layout = QVBoxLayout()
        movementSpeed_Layout.setContentsMargins(10, 10, 10, 10)  # Add padding
        movementSpeed_Layout.setSpacing(5)
        
        # Applying Background and Border using Stylesheet on Parent Widget
        self.setStyleSheet(
            """
            QLabel#thrusterSection {
                background-color: rgba(114, 238, 238, 40);
                border: 1px solid #72eeee;
                padding: 10px;
            }
            """
        )

        # Create a dummy QLabel as a container to apply styles
        thruster_section = QLabel(self)
        thruster_section.setObjectName("thrusterSection")
        thruster_section.setFixedSize(250, 200)  # Adjust size as needed
        thruster_section.setLayout(movementSpeed_Layout)

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

        # Add widgets inside the thruster section
        movementSpeed_Layout.addWidget(movementSpeed_label, alignment=Qt.AlignmentFlag.AlignLeft)
        movementSpeed_Layout.addWidget(moveLeft, alignment=Qt.AlignmentFlag.AlignLeft)
        movementSpeed_Layout.addWidget(movementSpeedLeft, alignment=Qt.AlignmentFlag.AlignLeft)
        movementSpeed_Layout.addWidget(movemRight, alignment=Qt.AlignmentFlag.AlignLeft)
        movementSpeed_Layout.addWidget(movementSpeedRight, alignment=Qt.AlignmentFlag.AlignLeft)

        colfirstRow.addWidget(thruster_section)
        second_row.addLayout(colfirstRow)

        # Add rows to main layout
        main_layout.addLayout(first_row)
        main_layout.addSpacing(20)
        main_layout.addLayout(second_row)
        main_layout.addStretch()

        self.setLayout(main_layout)