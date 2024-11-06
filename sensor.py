import sys
import time
import serial
import psutil
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
    QTextEdit,
     QScrollArea
)
from PyQt6.QtGui import QPainter, QColor, QPen, QFont, QBrush
from PyQt6.QtCore import Qt,QDateTime, QPointF, QTimer
from PyQt6.QtCharts import QChart, QChartView, QLineSeries,QDateTimeAxis,QValueAxis
from pymongo import MongoClient
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.dates as mdates

class DepthMeterWidget(QWidget):
    def __init__(self, depth, parent=None):
        super().__init__(parent)
        self.depth = depth
        


class SensorPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()


    def init_ui(self): 
        main_layout = QHBoxLayout(self)
        self.setLayout(main_layout)


