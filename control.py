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
    QSlider
)
from PyQt6.QtGui import QPixmap, QImage, QPainter, QBrush, QColor, QPainterPath
from PyQt6.QtCore import Qt, QRectF, QTimer


from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class ControlPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):

        main_layout = QVBoxLayout(self)

        first_row = QVBoxLayout(self)

        mainCam_label = QLabel("Main Camera")
        mainCam_label.setStyleSheet("font-size: 10px; color: #d1d2d2; font-family: Montserrat;")
        main_cam = QLabel(self)
        main_cam.setFixedSize(1920, 480)
        main_cam.setStyleSheet("background: transparent; border: 1px solid #72eeee; border-radius: 5px;")


        first_row.addWidget(mainCam_label)
        first_row.addWidget(main_cam)
        


        second_col = QVBoxLayout(self)
    

        main_layout.addLayout(first_row)
        main_layout.addStretch()

        


        
        
        self.setLayout(main_layout)
