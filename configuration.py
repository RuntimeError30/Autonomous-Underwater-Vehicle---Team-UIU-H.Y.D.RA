# import sys
# import time
# import psutil
# from PyQt6.QtWidgets import (
#     QApplication,
#     QLabel,
#     QPushButton,
#     QVBoxLayout,
#     QHBoxLayout,
#     QWidget,
#     QProgressBar,
#     QSpacerItem,
#     QSizePolicy,
#     QSlider,
#     QTextEdit,
#     QComboBox
# )
# from PyQt6.QtGui import QPainter, QColor, QPen, QFont, QBrush
# from PyQt6.QtCore import Qt, QRectF, QTimer
# from PyQt6.QtCharts import QChart, QChartView, QLineSeries
# import serial.tools.list_ports


# app = QApplication([])
# main_window = QWidget()

# main_window.setWindowTitle("H.Y.D.R.A")
# main_window.resize(1920, 1080)

# # Navbar
# navbar = QHBoxLayout()

# # Navbar --- Admin Button 
# admin_button = QPushButton("Admin")
# admin_button.setStyleSheet("""
# background-color: #F95A00;
# width: 40px;
# padding: 5px;
# border-radius:5px;
# color:white;
# font-size:10px;                 
# """)
# navbar.addWidget(admin_button)
# navbar.addStretch()

# # Navbar --- Links
# for labeles in ['CONTROL', 'CONFIGURATION', 'SENSOR']:
#     routebtn = QPushButton(labeles)
#     routebtn.setStyleSheet("""
# color: white;
# font-size:10px;
# opacity:70%;
# """)
#     # routebtn.clicked.connect(switch_widget)
#     navbar.setSpacing(40)
#     navbar.addWidget(routebtn)

# navbar.addStretch()

# toggle_switch = QPushButton('day')
# toggle_switch.setCheckable(True)
# navbar.addWidget(toggle_switch)
# # NAVBAR _______________FINISHED

# # MAIN_BODY_______________STARTS
# dashboard = QHBoxLayout()

# First_Col = QVBoxLayout()


# # Log
# # Log Panel
# logLayout = QVBoxLayout()
# logLayout.setContentsMargins(10, 10, 10, 10)
# logLayout.setSpacing(10)
# logWidget = QWidget()
# logWidget.setLayout(logLayout)
# logWidget.setStyleSheet("""
#     background-color: #222222;
#     border-radius: 5px;
#     padding: 5px;
# """)

# logLabel = QLabel("LOG PANEL")
# logLabel.setStyleSheet("""border-bottom: 1px solid #F95A00;""")
# logLayout.addWidget(logLabel)

# logTextEdit = QTextEdit()
# logTextEdit.setReadOnly(True)
# logLayout.addWidget(logTextEdit)


# First_Col.addWidget(logWidget)

# # Second col 
# Second_col = QVBoxLayout()


# comLayout = QVBoxLayout()
# comLayout.setContentsMargins(10, 10, 10, 10)
# comLayout.setSpacing(10)
# comWidget = QWidget()
# comWidget.setLayout(comLayout)
# comWidget.setStyleSheet("""
#     background-color: #222222;
#     border-radius: 5px;
#     padding: 5px;
# """)

# Comlabel = QLabel("COMMUNICATION CONFIGURATION")
# Comlabel.setStyleSheet("""color:white; border-bottom: 1px solid #F95A00;""")



# btnLayout = QHBoxLayout()
# connectLabel = QLabel('H.Y.D.R.A')
# connctBtn = QPushButton('Connect')

# btnLayout.addWidget(connectLabel)
# btnLayout.addWidget(connctBtn)

# serialLayout = QVBoxLayout()
# serialLabel = QLabel("Choose Serial Port")
# serialComBox = QComboBox()

# ports = serial.tools.list_ports.comports()

# for port in ports:
#     serialComBox.addItem(port.device)

# serialLayout.addWidget(serialLabel)
# serialLayout.addWidget(serialComBox)

# comLayout.addWidget(Comlabel)
# comLayout.addLayout(serialLayout)



# # Thruster Control 
# thrustLayout = QVBoxLayout()
# thrustLayout.setContentsMargins(10, 10, 10, 10)
# thrustLayout.setSpacing(10)
# thrustWidget = QWidget()
# thrustWidget.setLayout(thrustLayout)
# thrustWidget.setStyleSheet("""
#     background-color: #222222;
#     border-radius: 5px;
#     padding: 5px;
# """)

# mainLabel = QLabel('THRUSTERS TESTER')
# mainLabel.setStyleSheet("""border-bottom: 1px solid #F95A00;""")

# thrusterLabel1 =  QLabel('THRUSTER 01')
# thrusterLabel1.setStyleSheet("""font-size:12px""")

# thrusterLabelSpeed1 =  QLabel('Speed: ')
# thrusterLabelSpeed1.setStyleSheet("""font-size:8px""")
# thrusterSlider1 = QSlider(Qt.Orientation.Horizontal)
# thrusterSlider1.setMinimum(0)
# thrusterSlider1.setMaximum(100)
# thrusterSlider1.setValue(21)


# thrustLayout.addWidget(mainLabel)
# thrustLayout.addWidget(thrusterLabel1)
# thrustLayout.addWidget(thrusterLabelSpeed1)
# thrustLayout.addWidget(thrusterSlider1)



# # Thruster 02 

# thrustLayout2 = QVBoxLayout()
# thrustLayout2.setContentsMargins(10, 10, 10, 10)
# thrustLayout2.setSpacing(10)
# thrustWidget2 = QWidget()
# thrustWidget2.setLayout(thrustLayout2)
# thrustWidget2.setStyleSheet("""
#     background-color: #222222;
#     border-radius: 5px;
#     padding: 5px;
# """)

# mainLabel2 = QLabel('THRUSTER 02')
# mainLabel2.setStyleSheet("""border-bottom: 1px solid #F95A00;""")

# thrusterLabelSpeed2 = QLabel('Speed: ')
# thrusterLabelSpeed2.setStyleSheet("""font-size:8px""")
# thrusterSlider2 = QSlider(Qt.Orientation.Horizontal)
# thrusterSlider2.setMinimum(0)
# thrusterSlider2.setMaximum(100)
# thrusterSlider2.setValue(21)


# thrustLayout2.addWidget(mainLabel2)
# thrustLayout2.addWidget(thrusterLabelSpeed2)
# thrustLayout2.addWidget(thrusterSlider2)



# # Thruster 03 

# thrustLayout3 = QVBoxLayout()
# thrustLayout3.setContentsMargins(10, 10, 10, 10)
# thrustLayout3.setSpacing(10)
# thrustWidget3 = QWidget()
# thrustWidget3.setLayout(thrustLayout3)
# thrustWidget3.setStyleSheet("""
#     background-color: #222222;
#     border-radius: 5px;
#     padding: 5px;
# """)

# mainLabel3 = QLabel('THRUSTER 03')
# mainLabel3.setStyleSheet("""border-bottom: 1px solid #F95A00;""")

# thrusterLabelSpeed3 = QLabel('Speed: ')
# thrusterLabelSpeed3.setStyleSheet("""font-size:8px""")
# thrusterSlider3 = QSlider(Qt.Orientation.Horizontal)
# thrusterSlider3.setMinimum(0)
# thrusterSlider3.setMaximum(100)
# thrusterSlider3.setValue(21)


# thrustLayout3.addWidget(mainLabel3)
# thrustLayout3.addWidget(thrusterLabelSpeed3)
# thrustLayout3.addWidget(thrusterSlider3)




# # Thruster 04 

# thrustLayout4 = QVBoxLayout()
# thrustLayout4.setContentsMargins(10, 10, 10, 10)
# thrustLayout4.setSpacing(10)
# thrustWidget4 = QWidget()
# thrustWidget4.setLayout(thrustLayout4)
# thrustWidget4.setStyleSheet("""
#     background-color: #222222;
#     border-radius: 5px;
#     padding: 5px;
# """)

# mainLabel4 = QLabel('THRUSTER 04')
# mainLabel4.setStyleSheet("""border-bottom: 1px solid #F95A00;""")

# thrusterLabelSpeed4 = QLabel('Speed: ')
# thrusterLabelSpeed4.setStyleSheet("""font-size:8px""")
# thrusterSlider4 = QSlider(Qt.Orientation.Horizontal)
# thrusterSlider4.setMinimum(0)
# thrusterSlider4.setMaximum(100)
# thrusterSlider4.setValue(21)


# thrustLayout4.addWidget(mainLabel4)
# thrustLayout4.addWidget(thrusterLabelSpeed4)
# thrustLayout4.addWidget(thrusterSlider4)



# # Thruster 05 

# Second_col.addWidget(comWidget)
# Second_col.addWidget(thrustWidget)
# Second_col.addWidget(thrustWidget2)
# Second_col.addWidget(thrustWidget3)
# Second_col.addWidget(thrustWidget4)

# Second_col.addStretch()





# # Third Layout
# Third_col = QVBoxLayout()



# thrustLayout5 = QVBoxLayout()
# thrustLayout5.setContentsMargins(10, 10, 10, 10)
# thrustLayout5.setSpacing(10)
# thrustWidget5 = QWidget()
# thrustWidget5.setLayout(thrustLayout5)
# thrustWidget5.setStyleSheet("""
#     background-color: #222222;
#     border-radius: 5px;
#     padding: 5px;
# """)

# mainLabel5 = QLabel('THRUSTER 05')
# mainLabel5.setStyleSheet("""border-bottom: 1px solid #F95A00;""")

# thrusterLabelSpeed5 = QLabel('Speed: ')
# thrusterLabelSpeed5.setStyleSheet("""font-size:8px""")
# thrusterSlider5 = QSlider(Qt.Orientation.Horizontal)
# thrusterSlider5.setMinimum(0)
# thrusterSlider5.setMaximum(100)
# thrusterSlider5.setValue(21)


# thrustLayout5.addWidget(mainLabel5)
# thrustLayout5.addWidget(thrusterLabelSpeed5)
# thrustLayout5.addWidget(thrusterSlider5)

# # Thruster 06 
# thrustLayout6 = QVBoxLayout()
# thrustLayout6.setContentsMargins(10, 10, 10, 10)
# thrustLayout6.setSpacing(10)
# thrustWidget6 = QWidget()
# thrustWidget6.setLayout(thrustLayout6)
# thrustWidget6.setStyleSheet("""
#     background-color: #222222;
#     border-radius: 5px;
#     padding: 5px;
# """)

# mainLabel6 = QLabel('THRUSTER 06')
# mainLabel6.setStyleSheet("""border-bottom: 1px solid #F95A00;""")

# thrusterLabelSpeed6 = QLabel('Speed: ')
# thrusterLabelSpeed6.setStyleSheet("""font-size:8px""")
# thrusterSlider6 = QSlider(Qt.Orientation.Horizontal)
# thrusterSlider6.setMinimum(0)
# thrusterSlider6.setMaximum(100)
# thrusterSlider6.setValue(21)

# thrustLayout6.addWidget(mainLabel6)
# thrustLayout6.addWidget(thrusterLabelSpeed6)
# thrustLayout6.addWidget(thrusterSlider6)




# # KEY BINDINGS
# keyLayout = QVBoxLayout()
# keyLayout.setContentsMargins(10, 10, 10, 10)
# keyLayout.setSpacing(10)
# keyWidget = QWidget()
# keyWidget.setLayout(keyLayout)
# keyWidget.setStyleSheet("""
#     background-color: #222222;
#     border-radius: 5px;
#     padding: 5px;
        
# """)
# keyLabel = QLabel('KEY BINDINGS')
# keyLabel.setStyleSheet("""border-bottom: 1px solid #F95A00;""")

# # Trn lft
# leftLay = QHBoxLayout()
# leftComBox = QComboBox()
# leftLab = QLabel("TURN LEFT")
# control_keys = ["W", "A", "S", "D", "Up Arrow", "Down Arrow"]
# for key in control_keys:
#     leftComBox.addItem(key)

# leftLay.addWidget(leftLab) 
# leftLay.addWidget(leftComBox)

# # Trn ryt
# rightLay = QHBoxLayout()
# rightComBox = QComboBox()
# rightLab = QLabel("TURN RIGHT")
# control_keys2 = ["W", "A", "S", "D", "Up Arrow", "Down Arrow"]
# for key2 in control_keys:
#     rightComBox.addItem(key2)

# rightLay.addWidget(rightLab) 
# rightLay.addWidget(rightComBox)

# # Trn up
# upLay = QHBoxLayout()
# upComBox = QComboBox()
# upLab = QLabel("TURN UP")
# control_keys3 = ["W", "A", "S", "D", "Up Arrow", "Down Arrow"]
# for key3 in control_keys:
#     upComBox.addItem(key3)

# upLay.addWidget(upLab) 
# upLay.addWidget(upComBox)


# # Trn down
# downLay = QHBoxLayout()
# downComBox = QComboBox()
# downLab = QLabel("TURN DOWN")
# control_keys4 = ["W", "A", "S", "D", "Up Arrow", "Down Arrow"]
# for key4 in control_keys4:
#     downComBox.addItem(key4)

# downLay.addWidget(downLab) 
# downLay.addWidget(downComBox)


# keyLayout.addWidget(keyLabel)
# keyLayout.addLayout(leftLay)
# keyLayout.addLayout(rightLay)
# keyLayout.addLayout(upLay)
# keyLayout.addLayout(downLay)

# Third_col.addWidget(thrustWidget5)
# Third_col.addWidget(thrustWidget6)
# Third_col.addWidget(keyWidget)

# Third_col.addStretch()

# dashboard.addLayout(First_Col)
# dashboard.addLayout(Second_col)
# dashboard.addLayout(Third_col)
# dashboard.addStretch()

# # Main layout that combines navbar and dashboard
# main_layout = QVBoxLayout()
# main_layout.addLayout(navbar)
# main_layout.addLayout(dashboard)
# main_window.setLayout(main_layout)

# main_window.setStyleSheet("""
#     QWidget {
#         background-color: #141416;
#         margin: 0;
#         padding: 0;
#         font-family: Montserrat;
#         color: white;
#     }
#     QVBoxLayout, QHBoxLayout {
#         margin: 0;
#         spacing: 0;
#     }
# """)

# def add_log_message(message):
#     logTextEdit.append(message)
# add_log_message("Application started.")

# main_window.show()
# app.exec()


import sys
import time
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
    QComboBox
)
from PyQt6.QtGui import QPainter, QColor, QPen, QFont, QBrush
from PyQt6.QtCore import Qt, QRectF, QTimer
from PyQt6.QtCharts import QChart, QChartView, QLineSeries
import serial.tools.list_ports

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class ConfigPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.serial_port = None

    def update_pwm_value(self, value):
        self.thrusterLabelSpeed1.setText(f"PWM Value: {value}")
        self.serial_port.write(f"{value}\n".encode())
    
    def switch_serial(self, index):
        ports = serial.tools.list_ports.comports()
        selected_port = ports[index].device

        if self.serial_port is not None: 
            self.serial_port.close()

        self.serial_port = serial.Serial(selected_port, 9600, timeout=1)
        print(f"Switched to serial port: {selected_port}")



    def init_ui(self):
        main_layout = QHBoxLayout(self)
        First_Col = QVBoxLayout()


        # Log
        # Log Panel
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

        logLabel = QLabel("LOG PANEL")
        logLabel.setStyleSheet("""border-bottom: 1px solid #F95A00;""")
        logLayout.addWidget(logLabel)

        logTextEdit = QTextEdit("Pressed Button 1")

        logTextEdit.setReadOnly(True)
        logLayout.addWidget(logTextEdit)


        # Second col 
        Second_col = QVBoxLayout()


        comLayout = QVBoxLayout()
        comLayout.setContentsMargins(10, 10, 10, 10)
        comLayout.setSpacing(10)
        comWidget = QWidget()
        comWidget.setLayout(comLayout)
        comWidget.setStyleSheet("""
            background-color: #222222;
            border-radius: 5px;
            padding: 5px;
        """)

        Comlabel = QLabel("COMMUNICATION CONFIGURATION")
        Comlabel.setStyleSheet("""color:white; border-bottom: 1px solid #F95A00;""")



        btnLayout = QHBoxLayout()
        connectLabel = QLabel('H.Y.D.R.A')
        connctBtn = QPushButton('Connect')

        btnLayout.addWidget(connectLabel)
        btnLayout.addWidget(connctBtn)

        serialLayout = QVBoxLayout()
        serialLabel = QLabel("Choose Serial Port")
        serialComBox = QComboBox()

        ports = serial.tools.list_ports.comports()


        for port in ports:
            serialComBox.addItem(port.device)

        serialComBox.currentIndexChanged.connect(self.switch_serial)

        serialLayout.addWidget(serialLabel)
        serialLayout.addWidget(serialComBox)

        comLayout.addWidget(Comlabel)
        comLayout.addLayout(serialLayout)



        # Thruster Control 
        thrustLayout = QVBoxLayout()
        thrustLayout.setContentsMargins(10, 10, 10, 10)
        thrustLayout.setSpacing(10)
        thrustWidget = QWidget()
        thrustWidget.setLayout(thrustLayout)
        thrustWidget.setStyleSheet("""
            background-color: #222222;
            border-radius: 5px;
            padding: 5px;
        """)

        mainLabel = QLabel('THRUSTERS TESTER')
        mainLabel.setStyleSheet("""border-bottom: 1px solid #F95A00;""")

        thrusterLabel1 =  QLabel('THRUSTER 01')
        thrusterLabel1.setStyleSheet("""font-size:12px""")

        self.thrusterLabelSpeed1 =  QLabel(f"PWM Value: 1")
        self.thrusterLabelSpeed1.setStyleSheet("""font-size:8px""")
        self.thrusterSlider1 = QSlider(Qt.Orientation.Horizontal)
        self.thrusterSlider1.setMinimum(0)
        self.thrusterSlider1.setMaximum(255)
        self.thrusterSlider1.setValue(1)
        self.thrusterSlider1.valueChanged.connect(self.update_pwm_value)


        thrustLayout.addWidget(mainLabel)
        thrustLayout.addWidget(thrusterLabel1)
        thrustLayout.addWidget(self.thrusterLabelSpeed1)
        thrustLayout.addWidget(self.thrusterSlider1)



        # Thruster 02 

        thrustLayout2 = QVBoxLayout()
        thrustLayout2.setContentsMargins(10, 10, 10, 10)
        thrustLayout2.setSpacing(10)
        thrustWidget2 = QWidget()
        thrustWidget2.setLayout(thrustLayout2)
        thrustWidget2.setStyleSheet("""
            background-color: #222222;
            border-radius: 5px;
            padding: 5px;
        """)

        mainLabel2 = QLabel('THRUSTER 02')
        mainLabel2.setStyleSheet("""border-bottom: 1px solid #F95A00;""")

        thrusterLabelSpeed2 = QLabel('Speed: ')
        thrusterLabelSpeed2.setStyleSheet("""font-size:8px""")
        thrusterSlider2 = QSlider(Qt.Orientation.Horizontal)
        thrusterSlider2.setMinimum(0)
        thrusterSlider2.setMaximum(100)
        thrusterSlider2.setValue(21)


        thrustLayout2.addWidget(mainLabel2)
        thrustLayout2.addWidget(thrusterLabelSpeed2)
        thrustLayout2.addWidget(thrusterSlider2)



        # Thruster 03 

        thrustLayout3 = QVBoxLayout()
        thrustLayout3.setContentsMargins(10, 10, 10, 10)
        thrustLayout3.setSpacing(10)
        thrustWidget3 = QWidget()
        thrustWidget3.setLayout(thrustLayout3)
        thrustWidget3.setStyleSheet("""
            background-color: #222222;
            border-radius: 5px;
            padding: 5px;
        """)

        mainLabel3 = QLabel('THRUSTER 03')
        mainLabel3.setStyleSheet("""border-bottom: 1px solid #F95A00;""")

        thrusterLabelSpeed3 = QLabel('Speed: ')
        thrusterLabelSpeed3.setStyleSheet("""font-size:8px""")
        thrusterSlider3 = QSlider(Qt.Orientation.Horizontal)
        thrusterSlider3.setMinimum(0)
        thrusterSlider3.setMaximum(100)
        thrusterSlider3.setValue(21)


        thrustLayout3.addWidget(mainLabel3)
        thrustLayout3.addWidget(thrusterLabelSpeed3)
        thrustLayout3.addWidget(thrusterSlider3)




        # Thruster 04 

        thrustLayout4 = QVBoxLayout()
        thrustLayout4.setContentsMargins(10, 10, 10, 10)
        thrustLayout4.setSpacing(10)
        thrustWidget4 = QWidget()
        thrustWidget4.setLayout(thrustLayout4)
        thrustWidget4.setStyleSheet("""
            background-color: #222222;
            border-radius: 5px;
            padding: 5px;
        """)

        mainLabel4 = QLabel('THRUSTER 04')
        mainLabel4.setStyleSheet("""border-bottom: 1px solid #F95A00;""")

        thrusterLabelSpeed4 = QLabel('Speed: ')
        thrusterLabelSpeed4.setStyleSheet("""font-size:8px""")
        thrusterSlider4 = QSlider(Qt.Orientation.Horizontal)
        thrusterSlider4.setMinimum(0)
        thrusterSlider4.setMaximum(100)
        thrusterSlider4.setValue(21)


        thrustLayout4.addWidget(mainLabel4)
        thrustLayout4.addWidget(thrusterLabelSpeed4)
        thrustLayout4.addWidget(thrusterSlider4)



        # Thruster 05 




        # Third Layout
        Third_col = QVBoxLayout()



        thrustLayout5 = QVBoxLayout()
        thrustLayout5.setContentsMargins(10, 10, 10, 10)
        thrustLayout5.setSpacing(10)
        thrustWidget5 = QWidget()
        thrustWidget5.setLayout(thrustLayout5)
        thrustWidget5.setStyleSheet("""
            background-color: #222222;
            border-radius: 5px;
            padding: 5px;
        """)

        mainLabel5 = QLabel('THRUSTER 05')
        mainLabel5.setStyleSheet("""border-bottom: 1px solid #F95A00;""")

        thrusterLabelSpeed5 = QLabel('Speed: ')
        thrusterLabelSpeed5.setStyleSheet("""font-size:8px""")
        thrusterSlider5 = QSlider(Qt.Orientation.Horizontal)
        thrusterSlider5.setMinimum(0)
        thrusterSlider5.setMaximum(100)
        thrusterSlider5.setValue(21)


        thrustLayout5.addWidget(mainLabel5)
        thrustLayout5.addWidget(thrusterLabelSpeed5)
        thrustLayout5.addWidget(thrusterSlider5)

        # Thruster 06 
        thrustLayout6 = QVBoxLayout()
        thrustLayout6.setContentsMargins(10, 10, 10, 10)
        thrustLayout6.setSpacing(10)
        thrustWidget6 = QWidget()
        thrustWidget6.setLayout(thrustLayout6)
        thrustWidget6.setStyleSheet("""
            background-color: #222222;
            border-radius: 5px;
            padding: 5px;
        """)

        mainLabel6 = QLabel('THRUSTER 06')
        mainLabel6.setStyleSheet("""border-bottom: 1px solid #F95A00;""")

        thrusterLabelSpeed6 = QLabel('Speed: ')
        thrusterLabelSpeed6.setStyleSheet("""font-size:8px""")
        thrusterSlider6 = QSlider(Qt.Orientation.Horizontal)
        thrusterSlider6.setMinimum(0)
        thrusterSlider6.setMaximum(100)
        thrusterSlider6.setValue(21)

        thrustLayout6.addWidget(mainLabel6)
        thrustLayout6.addWidget(thrusterLabelSpeed6)
        thrustLayout6.addWidget(thrusterSlider6)




        # KEY BINDINGS
        keyLayout = QVBoxLayout()
        keyLayout.setContentsMargins(10, 10, 10, 10)
        keyLayout.setSpacing(10)
        keyWidget = QWidget()
        keyWidget.setLayout(keyLayout)
        keyWidget.setStyleSheet("""
            background-color: #222222;
            border-radius: 5px;
            padding: 5px;
                
        """)
        keyLabel = QLabel('KEY BINDINGS')
        keyLabel.setStyleSheet("""border-bottom: 1px solid #F95A00;""")

        # Trn lft
        leftLay = QHBoxLayout()
        leftComBox = QComboBox()
        leftLab = QLabel("TURN LEFT")
        control_keys = ["W", "A", "S", "D", "Up Arrow", "Down Arrow"]
        for key in control_keys:
            leftComBox.addItem(key)

        leftLay.addWidget(leftLab) 
        leftLay.addWidget(leftComBox)

        # Trn ryt
        rightLay = QHBoxLayout()
        rightComBox = QComboBox()
        rightLab = QLabel("TURN RIGHT")
        control_keys2 = ["W", "A", "S", "D", "Up Arrow", "Down Arrow"]
        for key2 in control_keys:
            rightComBox.addItem(key2)

        rightLay.addWidget(rightLab) 
        rightLay.addWidget(rightComBox)

        # Trn up
        upLay = QHBoxLayout()
        upComBox = QComboBox()
        upLab = QLabel("TURN UP")
        control_keys3 = ["W", "A", "S", "D", "Up Arrow", "Down Arrow"]
        for key3 in control_keys:
            upComBox.addItem(key3)

        upLay.addWidget(upLab) 
        upLay.addWidget(upComBox)


        # Trn down
        downLay = QHBoxLayout()
        downComBox = QComboBox()
        downLab = QLabel("TURN DOWN")
        control_keys4 = ["W", "A", "S", "D", "Up Arrow", "Down Arrow"]
        for key4 in control_keys4:
            downComBox.addItem(key4)

        downLay.addWidget(downLab) 
        downLay.addWidget(downComBox)


        keyLayout.addWidget(keyLabel)
        keyLayout.addLayout(leftLay)
        keyLayout.addLayout(rightLay)
        keyLayout.addLayout(upLay)
        keyLayout.addLayout(downLay)





        First_Col.addWidget(logWidget)
        Second_col.addWidget(comWidget)
        Second_col.addWidget(thrustWidget)
        Second_col.addWidget(thrustWidget2)
        Second_col.addWidget(thrustWidget3)
        Second_col.addWidget(thrustWidget4)
        Third_col.addWidget(thrustWidget5)
        Third_col.addWidget(thrustWidget6)
        Third_col.addWidget(keyWidget)

        Third_col.addStretch()

        Second_col.addStretch()
        main_layout.addLayout(First_Col)
        main_layout.addLayout(Second_col)
        main_layout.addLayout(Third_col)



        self.setLayout(main_layout)
