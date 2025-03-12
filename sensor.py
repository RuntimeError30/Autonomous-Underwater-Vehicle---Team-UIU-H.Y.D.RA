import sys
import random
import time
from dbconnect import connection
from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout
)
from PyQt6.QtCore import QThread, pyqtSignal

class DataGeneratorThread(QThread):
    """Thread to generate and insert sensor data into MongoDB asynchronously."""
    data_inserted = pyqtSignal(dict)  # Signal to update UI with new data

    def __init__(self, collection_name):
        super().__init__()
        self.collection = connection(collection_name)
        self.running = True  # Control flag

    def run(self):
        max_entries = 500  # Maximum number of data points
        for _ in range(max_entries):
            if not self.running:
                break  # Stop if the flag is set to False

            data = self.generate_data()
            self.collection.insert_one(data)  # Insert into MongoDB
            self.data_inserted.emit(data)  # Emit signal to update UI
            print(f"Inserted: {data}")

            time.sleep(1)  # Wait for 1 second

    def generate_data(self):
        """Generate random sensor data."""
        return {
            "temperature": round(random.uniform(0, 50), 2),  # Temperature in Celsius
            "pressure": round(random.uniform(900, 1100), 2),  # Pressure in hPa
            "depth": round(random.uniform(0, 500), 2),  # Depth in meters
            "leak": random.choice(["Yes", "No"]),  # Leak status
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

    def stop(self):
        """Stop the thread gracefully."""
        self.running = False

class SensorPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

        # Start data generation in a separate thread
        self.data_thread = DataGeneratorThread("sensors")
        self.data_thread.data_inserted.connect(self.update_ui)
        self.data_thread.start()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        first_row = QVBoxLayout()

        # Temperature
        self.temp_label = QLabel("Temperature: 0°C")
        first_row.addWidget(self.temp_label)

        # Pressure
        self.pressure_label = QLabel("Pressure: 0 hPa")
        first_row.addWidget(self.pressure_label)

        # Leak
        self.leak_label = QLabel("Leak: No")
        first_row.addWidget(self.leak_label)

        # Depth
        self.depth_label = QLabel("Depth: 0 m")
        first_row.addWidget(self.depth_label)

        main_layout.addLayout(first_row)
        self.setLayout(main_layout)

    def update_ui(self, data):
        """Update labels with real-time sensor data."""
        self.temp_label.setText(f"Temperature: {data['temperature']}°C")
        self.pressure_label.setText(f"Pressure: {data['pressure']} hPa")
        self.leak_label.setText(f"Leak: {data['leak']}")
        self.depth_label.setText(f"Depth: {data['depth']} m")

    def closeEvent(self, event):
        """Stop the data thread when closing the window."""
        self.data_thread.stop()
        self.data_thread.wait()
        super().closeEvent(event)
