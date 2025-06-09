import sys
import re
import serial
from serial import SerialException
from datetime import datetime

from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QHBoxLayout, QFrame
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont
import pyqtgraph as pg


class FloatDashboard(QWidget):
    def __init__(self, port='/dev/ttyACM0', baudrate=9600):
        super().__init__()
        self.setWindowTitle("MATE FLOAT DASHBOARD")
        self.setGeometry(100, 100, 1920, 1080)
        self.setStyleSheet(self.load_stylesheet())

        self.port_name = port
        self.baudrate = baudrate
        self.serial_port = None
        self.serial_connected = False

        self.initUI()
        self.initData()

        # Start connection checker timer
        self.connection_timer = QTimer()
        self.connection_timer.timeout.connect(self.checkSerialConnection)
        self.connection_timer.start(1000)  # Check every 1 second

    def initUI(self):
        main_layout = QVBoxLayout(self)

        # Top bar layout
        top_layout = QHBoxLayout()
        title = QLabel("MATE FLOAT DASHBOARD")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #ff9900")

        self.telemetry_button = QPushButton("START TELEMETRY")
        self.telemetry_button.clicked.connect(self.toggleTelemetry)
        self.telemetry_button.setObjectName("telemetryButton")

        self.emergency_button = QPushButton("EMERGENCY STOP")
        self.emergency_button.clicked.connect(self.emergencyStop)
        self.emergency_button.setObjectName("emergencyButton")

        comm_status = QFrame()
        comm_status.setObjectName("statusFrame")
        comm_status_layout = QVBoxLayout(comm_status)
        stat_title = QLabel("FLOAT COMMUNICATION STATUS")
        stat_title.setStyleSheet("color: gray; font-size: 10px;")

        self.stat_label = QLabel("DISCONNECTED")
        self.stat_label.setStyleSheet("color: red; font-size: 16px;")

        self.ip_label = QLabel("NO SERIAL PORT")
        self.ip_label.setStyleSheet("color: gray; font-size: 10px;")

        comm_status_layout.addWidget(stat_title)
        comm_status_layout.addWidget(self.stat_label)
        comm_status_layout.addWidget(self.ip_label)

        top_layout.addWidget(title)
        top_layout.addStretch()
        top_layout.addWidget(self.telemetry_button)
        top_layout.addWidget(self.emergency_button)
        top_layout.addWidget(comm_status)

        # Graph layout
        graph_layout = QHBoxLayout()
        self.pressure_plot = pg.PlotWidget(title="Live Pressure Graph")
        self.pressure_plot.setBackground("#202020")
        self.pressure_curve = self.pressure_plot.plot(pen=pg.mkPen('#ff9900', width=2))

        self.depth_plot = pg.PlotWidget(title="Live Altitude Graph")
        self.depth_plot.setBackground("#202020")
        self.depth_curve = self.depth_plot.plot(pen=pg.mkPen('#00aaff', width=2))

        graph_layout.addWidget(self.pressure_plot)
        graph_layout.addWidget(self.depth_plot)

        # Sensor value labels
        sensor_layout = QHBoxLayout()
        self.temp_label = QLabel("Temperature: -- °C")
        self.pressure_label = QLabel("Pressure: -- mbar")
        self.altitude_label = QLabel("Altitude: -- m")

        for label in [self.temp_label, self.pressure_label, self.altitude_label]:
            label.setStyleSheet("color: white; font-size: 14px;")
            sensor_layout.addWidget(label)

        # Table layout
        table_title = QLabel("Live Data From Sensors")
        table_title.setStyleSheet("color: gray; font-size: 12px;")
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Team ID", "Time", "Temperature (°C)", "Altitude (m)", "Pressure (Pa)"])
        self.table.setStyleSheet("background-color: #121212; color: white; border: 1px solid #2e2e2e;")

        # Combine layouts
        main_layout.addLayout(top_layout)
        main_layout.addLayout(graph_layout)
        main_layout.addLayout(sensor_layout)
        main_layout.addWidget(table_title)
        main_layout.addWidget(self.table)

        # Timer for telemetry
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateTelemetry)

    def initData(self):
        self.team_id = "PN06"
        self.x_data = []
        self.pressure_data = []
        self.altitude_data = []
        self.counter = 0

    def toggleTelemetry(self):
        if self.timer.isActive():
            self.timer.stop()
            self.telemetry_button.setText("START TELEMETRY")
        else:
            self.timer.start(1000)
            self.telemetry_button.setText("STOP TELEMETRY")

    def emergencyStop(self):
        self.timer.stop()
        self.telemetry_button.setText("START TELEMETRY")
        print("!!! EMERGENCY STOP ACTIVATED !!!")

    def updateTelemetry(self):
        self.read_serial()

    def read_serial(self):
        if self.serial_port and self.serial_port.is_open and self.serial_port.in_waiting:
            try:
                line = self.serial_port.readline().decode('utf-8', errors='ignore').strip()
                print("Received:", line)

                if line.startswith("Received -> "):
                    line = line[len("Received -> "):]

                match = re.search(
                    r"T:\s*(ovf|[-\d.]+)\s*C\s*\|\s*P:\s*(ovf|[-\d.]+)\s*mbar\s*\|\s*Alt:\s*(ovf|[-\d.]+)",
                    line
                )

                if match:
                    temp_str, pressure_str, altitude_str = match.groups()

                    temp = 0.0 if temp_str == "ovf" else float(temp_str)
                    pressure = 0.0 if pressure_str == "ovf" else float(pressure_str)
                    altitude = 0.0 if altitude_str == "ovf" else float(altitude_str)

                    self.temp_label.setText(f"Temperature: {temp:.2f} °C")
                    self.pressure_label.setText(f"Pressure: {pressure:.2f} mbar")
                    self.altitude_label.setText(f"Altitude: {altitude:.2f} m")

                    self.counter += 1
                    self.x_data.append(self.counter)
                    self.pressure_data.append(pressure)
                    self.altitude_data.append(altitude)

                    self.x_data = self.x_data[-50:]
                    self.pressure_data = self.pressure_data[-50:]
                    self.altitude_data = self.altitude_data[-50:]

                    self.pressure_curve.setData(self.x_data, self.pressure_data)
                    self.depth_curve.setData(self.x_data, self.altitude_data)

                    timestamp = datetime.now().strftime("%H:%M:%S")
                    row = self.table.rowCount()
                    self.table.insertRow(row)
                    self.table.setItem(row, 0, QTableWidgetItem(self.team_id))
                    self.table.setItem(row, 1, QTableWidgetItem(timestamp))
                    self.table.setItem(row, 2, QTableWidgetItem(f"{temp:.2f}"))
                    self.table.setItem(row, 3, QTableWidgetItem(f"{altitude:.2f}"))
                    self.table.setItem(row, 4, QTableWidgetItem(f"{pressure:.2f}"))

                    self.table.scrollToBottom()

                else:
                    print("Line did not match expected format.")

            except Exception as e:
                print("Error parsing serial data:", e)

    def checkSerialConnection(self):
        if self.serial_port is None or not self.serial_port.is_open:
            try:
                self.serial_port = serial.Serial(self.port_name, self.baudrate, timeout=1)
                self.serial_connected = True
                print("Serial connected.")
            except SerialException:
                self.serial_port = None
                self.serial_connected = False

        # Update status label
        if self.serial_connected:
            self.stat_label.setText("CONNECTED")
            self.stat_label.setStyleSheet("color: #ff9900; font-size: 16px;")
            self.ip_label.setText(f"CONNECTED TO: {self.serial_port.port}")
        else:
            self.stat_label.setText("DISCONNECTED")
            self.stat_label.setStyleSheet("color: red; font-size: 16px;")
            self.ip_label.setText("NO SERIAL PORT")

    def load_stylesheet(self):
        return """
        QWidget {
            background-color: #121212;
            font-family: 'Segoe UI', sans-serif;
            font-size: 13px;
        }
        QPushButton#telemetryButton {
            background-color: #292929;
            color: white;
            border: 1px solid #444;
            border-radius: 6px;
            padding: 6px 12px;
        }
        QPushButton#telemetryButton:hover {
            background-color: #ff9900;
            color: black;
        }
        QPushButton#emergencyButton {
            background-color: red;
            color: white;
            font-weight: bold;
            border-radius: 6px;
            padding: 6px 12px;
        }
        QTableWidget {
            gridline-color: #2e2e2e;
            border-radius: 8px;
        }
        QHeaderView::section {
            background-color: #1e1e1e;
            color: #aaa;
            padding: 4px;
            border: none;
        }
        QFrame#statusFrame {
            border: 1px solid #2e2e2e;
            border-radius: 12px;
            padding: 10px;
            background-color: #1a1a1a;
        }
        """


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FloatDashboard(port='/dev/ttyACM0')
    window.show()
    sys.exit(app.exec())

