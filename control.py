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

        main_layout = QHBoxLayout(self)

        first_col = QVBoxLayout(self)

        mainCam_label = QLabel("Main Camera")
        mainCam_label.setStyleSheet("font-size: 10px; color: #d1d2d2; font-family: Montserrat;")
        main_cam = QLabel(self)
        main_cam.setFixedSize(960, 480)
        main_cam.setStyleSheet("background: transparent; border: 1px solid #72eeee; border-radius: 5px;")

        stackCam_layout = QHBoxLayout(self)

        back_cam = QLabel(self)
        back_cam.setFixedSize(315, 216)
        back_cam.setStyleSheet("background: transparent; border: 1px solid #72eeee; border-radius: 5px;")

        left_cam = QLabel(self)
        left_cam.setFixedSize(315, 216)
        left_cam.setStyleSheet("background: transparent; border: 1px solid #72eeee; border-radius: 5px;")

        right_cam = QLabel(self)
        right_cam.setFixedSize(315, 216)
        right_cam.setStyleSheet("background: transparent; border: 1px solid #72eeee; border-radius: 5px;")




        stackCam_layout.addWidget(back_cam)
        stackCam_layout.addWidget(left_cam)
        stackCam_layout.addWidget(right_cam)
        stackCam_layout.addStretch()


        
        first_col.addWidget(mainCam_label)
        first_col.addWidget(main_cam)
        first_col.addLayout(stackCam_layout)

        second_col = QVBoxLayout(self)
        
        statusWidget = QWidget()
        statusWidget.setStyleSheet(" border: 1px solid #72eeee; border-radius: 5px;")
        status_layout = QVBoxLayout(statusWidget)

        status_label = QLabel("Status")
        status_layout.addWidget(status_label)
        status_layout.addStretch()

        second_col.addWidget(statusWidget)




        main_layout.addLayout(first_col)
        main_layout.addLayout(second_col)
        main_layout.addStretch()

        


        
        
        self.setLayout(main_layout)
