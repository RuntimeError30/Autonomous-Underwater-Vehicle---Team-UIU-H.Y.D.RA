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
from dbconnection import connection
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.dates as mdates

class DepthMeterWidget(QWidget):
    def __init__(self, depth, parent=None):
        super().__init__(parent)
        self.depth = depth
        

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Background
        painter.setBrush(QColor("#222222"))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 20, 20)

        # Draw the scale
        painter.setPen(QPen(QColor("#F95A00"), 2))
        for i in range(20):
            y = self.height() - (i * self.height() // 20) - 20
            painter.drawLine(20, y, 40, y)
            painter.drawText(45, y + 4, str(i))

        # Draw the indicator
        indicator_y = self.height() - (self.depth * self.height() // 20) - 20
        painter.setPen(QPen(QColor("#F95A00"), 2))
        painter.drawLine(15, indicator_y, 45, indicator_y)

class SensorPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.fetch_data_logs()
        QTimer.singleShot(1000, self.fetch_and_update_data)
        
        self.serial_port = serial.Serial('/dev/cu.usbserial-120',9600, timeout=1)


                # DEMO SENSOR TEST
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.soil_sensor_val)
        self.timer.start(2000) 

    def fetch_and_update_data(self):
        self.fetch_data()
        self.update_graph()

    
    def fetch_data(self):
        sensor_collection = connection("sensor") 
        document = sensor_collection.find().sort("timestamp",1)

        self.depth_val = []
        self.vol_val = []
        self.temp_val = []

        for doc in document:
            timestamp = doc.get('timestamp')
            if timestamp:
                timestamp = QDateTime.fromMSecsSinceEpoch(int(timestamp.timestamp()*1000))
                depth = doc.get('depth', 0)
                temp = doc.get('temperature', 0)
                volt = doc.get('voltage', 0)

                print(f"Fetched Data - Timestamp: {timestamp}, Depth: {depth}, Temp: {temp}, Volt: {volt}")

                self.depth_val.append(QPointF(timestamp.toMSecsSinceEpoch(),depth))
                self.temp_val.append(QPointF(timestamp.toMSecsSinceEpoch(),temp))
                self.vol_val.append(QPointF(timestamp.toMSecsSinceEpoch(),volt))
        
            print(f"Depth values: {self.depth_val}")
            print(f"Temperature values: {self.temp_val}")
            print(f"Voltage values: {self.vol_val}")


        # if document:
        #     self.depthShow.setText(str(document.get('depth', 'N/A')))
        #     self.TemphShow.setText(str(document.get('temperature', 'N/A')))
        #     self.voltageShow.setText(str(document.get('voltage', 'N/A')))
        # else:
        #     print("No data found.")


    def update_graph(self):
        print("Updating graphs")
        self.depth_series.clear()
        self.temp_series.clear()
        self.voltage_series.clear()

        # Define colors
        depth_color = QColor('#FF0000')  # Red
        temp_color = QColor('#00FF00')   # Green
        voltage_color = QColor('#0000FF')  # Blue

        # Set colors for series
        self.depth_series.setColor(depth_color)
        self.temp_series.setColor(temp_color)
        self.voltage_series.setColor(voltage_color)

        if not self.depth_val and not self.temp_val and not self.vol_val:
            print("No data to update graphs.")
            return

        print(f"Updating Depth Series with {len(self.depth_val)} points")
        for point in self.depth_val:
            print(f"Adding Depth Data Point: {point}")
            self.depth_series.append(point)

        print(f"Updating Temperature Series with {len(self.temp_val)} points")
        for point in self.temp_val:
            print(f"Adding Temperature Data Point: {point}")
            self.temp_series.append(point)

        print(f"Updating Voltage Series with {len(self.vol_val)} points")
        for point in self.vol_val:
            print(f"Adding Voltage Data Point: {point}")
            self.voltage_series.append(point)



    def create_sensor_graph(self, title, series):
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle(title)
        chart.createDefaultAxes()

        # XAXIS
        axis_X = QDateTimeAxis()
        axis_X.setFormat("hh:mm:ss")
        axis_X.setTitleText("Time")
        chart.addAxis(axis_X, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_X)

        if series.count() > 0:
            min_time = series.at(0).x()
            max_time = series.at(series.count() - 1).x()
            axis_X.setRange(QDateTime.fromMSecsSinceEpoch(min_time), QDateTime.fromMSecsSinceEpoch(max_time))
            

        # YAXIS
        axis_Y = QValueAxis()
        axis_Y.setTitleText("Value")
        chart.addAxis(axis_Y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_Y)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        return chart_view



    def fetch_data_logs(self):
        logs_collection = connection("log_data ")
        docs = logs_collection.find()
        
        log_text = ""
        if docs:
            for doc in docs:
                depth_log = doc.get('depth_log', 'NO DEPTH SENSOR LOG')
                temp_log = doc.get('temperature_log', 'NO TEMP SENSOR LOG')
                volt_log = doc.get('voltage_log', 'NO VOLT SENSOR LOG')

                log_text += f"Depth Sensor: {depth_log}\n"
                log_text += f"Temperature Sensor: {temp_log}\n"
                log_text += f"Voltage Sensor: {volt_log}\n"
                log_text += " "*30 + "\n"
            
            self.sensorlogTextEdit.setText(log_text)  
        else:
            print("No data found")

    def soil_sensor_val(self):
        if self.serial_port.in_waiting > 0:
            soil_val = self.serial_port.readline().decode('utf-8').strip()
            self.voltageShow.setText(soil_val)

    def init_ui(self): 
        main_layout = QHBoxLayout(self)
        First_Col = QVBoxLayout()



        sensorLayout = QVBoxLayout()
        sensorLayout.setContentsMargins(10, 10, 10, 10)
        sensorLayout.setSpacing(10)

        sensorWidget = QWidget()
        sensorWidget.setLayout(sensorLayout)
        sensorWidget.setStyleSheet("""
            background-color: #222222;
            border-radius: 5px;
            padding: 5px;
        """)

        sensorLabel = QLabel("SENSOR VALUES")
        sensorLabel.setStyleSheet("border-bottom: 1px solid #F95A00;")

        depthLayout = QHBoxLayout()
        depthLabel = QLabel("DEPTH")
        self.depthShow = QLabel()
        self.depthShow.setStyleSheet("background-color: #373737; width: 30px;")

        TempLayout = QHBoxLayout()
        TempLabel = QLabel("Temperature")
        self.TemphShow = QLabel("20")
        self.TemphShow.setStyleSheet("background-color: #373737; width: 30px;")

        voltageLayout = QHBoxLayout()
        voltageLabel = QLabel("Voltage")
        self.voltageShow = QLabel("20")
        self.voltageShow.setStyleSheet("background-color: #373737; width: 30px;")

        depthLayout.addWidget(depthLabel)
        depthLayout.addWidget(self.depthShow)
        TempLayout.addWidget(TempLabel)
        TempLayout.addWidget(self.TemphShow)
        voltageLayout.addWidget(voltageLabel)
        voltageLayout.addWidget(self.voltageShow)

        sensorLayout.addWidget(sensorLabel)
        sensorLayout.addLayout(depthLayout)
        sensorLayout.addLayout(TempLayout)
        sensorLayout.addLayout(voltageLayout)

        #Generel Log Panel
        logLayout = QVBoxLayout()
        logLayout.setContentsMargins(10, 10, 10, 10)
        logLayout.setSpacing(10)

        logWidget = QWidget()
        logWidget.setLayout(logLayout)
        logWidget.setStyleSheet("""
            background-color: #222222;
            border-radius: 5px;
            padding: 5px;
        """)

        logLabel = QLabel("GENEREL LOGS")
        logLabel.setStyleSheet("border-bottom: 1px solid #F95A00;")
        logLayout.addWidget(logLabel)

        self.logTextEdit = QTextEdit()
        self.logTextEdit.setReadOnly(True)
        logLayout.addWidget(self.logTextEdit)


        #Sensor Log Panel
        SensorlogLayout = QVBoxLayout()
        SensorlogLayout.setContentsMargins(10, 10, 10, 10)
        SensorlogLayout.setSpacing(10)

        sensorlogLabel = QLabel("SENSOR LOGS")
        sensorlogLabel.setStyleSheet("border-bottom: 1px solid #F95A00;")
        SensorlogLayout.addWidget(sensorlogLabel)

        self.sensorlogTextEdit = QTextEdit()
        self.sensorlogTextEdit.setReadOnly(True)
        SensorlogLayout.addWidget(self.sensorlogTextEdit)

        sensorlogWidget = QWidget()
        sensorlogWidget.setLayout(SensorlogLayout)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(sensorlogWidget)


        # Second col 
        Second_col = QVBoxLayout()

        layout = QVBoxLayout()
        depth_meter_widget = DepthMeterWidget(depth=13)
        depth_meter_widget.setMinimumWidth(100)
        depth_meter_widget.setMinimumHeight(650)

        depth_label = QLabel("Depth: 21 Meter")
        depth_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(depth_meter_widget)
        layout.addWidget(depth_label)



         # Third Layout
        Third_col = QVBoxLayout()

        graphrow1 = QHBoxLayout()
        graphrow2 = QHBoxLayout()

        self.depth_series = QLineSeries()
        self.temp_series = QLineSeries()
        self.voltage_series = QLineSeries()

        graphrow1.addWidget(self.create_sensor_graph("Depth Sensor", self.depth_series))
        graphrow1.addWidget(self.create_sensor_graph("Temperature Sensor", self.temp_series))
        graphrow2.addWidget(self.create_sensor_graph("Voltage Sensor", self.voltage_series))

        # self.fetch_data()
        # self.update_graph()

        # scroll_area = QScrollArea()



        # Add the widgets to the first column layout
        First_Col.addWidget(sensorWidget)
        First_Col.addWidget(logWidget)
        First_Col.addWidget(scroll_area)

        Second_col.addLayout(layout)
        Second_col.addStretch()
        Third_col.addLayout(graphrow1)
        Third_col.addLayout(graphrow2)

        # Add First_Col layout to main_layout
        main_layout.addLayout(First_Col)
        main_layout.addLayout(Second_col)
        main_layout.addLayout(Third_col)


