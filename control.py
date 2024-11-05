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
from camera import Camera
from pymongo import MongoClient
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class ControlPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.init_ui()

        

        

    

    def create_camera_label(self):
            self.camera_label = QLabel()
            self.camera_label.setFixedSize(160, 90)
            self.camera_label.setStyleSheet("""
            border: 1px solid #F95A00;
            padding: 5px;
            border-radius: 10px;
            overflow: hidden;
            """)
            return self.camera_label
    

    # Thruster Func

# T1
    def t1_toggle(self):
        if self.t1btn.isChecked():
            self.t1btn.setText("Power On")
            self.t1btn.setStyleSheet("""
                background-color: #F95A00;
                width: 90px;
                padding: 5px;
                border-radius:5px;
                color:white;
                font-size:10px;
                position: relative;
                left: 40px; 
            """)
        else:
            self.t1btn.setText("Power Off")
            self.t1btn.setStyleSheet("""
                background-color: #474747;
                width: 90px;
                padding: 5px;
                border-radius:5px;
                color:white;
                font-size:10px;
                position: relative;
                left: 40px; 
        """)
# T2
    def t2_toggle(self):    
        if self.t2btn.isChecked():
            self.t2btn.setText("Power On")
            self.t2btn.setStyleSheet("""
                background-color: #F95A00;
                width: 90px;
                padding: 5px;
                border-radius:5px;
                color:white;
                font-size:10px;
                position: relative;
                left: 40px; 
            """)
        else:
            self.t2btn.setText("Power Off")
            self.t2btn.setStyleSheet("""
                background-color: #474747;
                width: 90px;
                padding: 5px;
                border-radius:5px;
                color:white;
                font-size:10px;
                position: relative;
                left: 40px; 
            """)

# T3
    def t3_toggle(self):
        if self.t3btn.isChecked():
            self.t3btn.setText("Power On")
            self.t3btn.setStyleSheet("""
                background-color: #F95A00;
                width: 90px;
                padding: 5px;
                border-radius:5px;
                color:white;
                font-size:10px;
                position: relative;
                left: 40px; 
            """)
        else:
            self.t3btn.setText("Power Off")
            self.t3btn.setStyleSheet("""
                background-color: #474747;
                width: 90px;
                padding: 5px;
                border-radius:5px;
                color:white;
                font-size:10px;
                position: relative;
                left: 40px; 
            """)

# T4
    def t4_toggle(self):
        if self.t4btn.isChecked():
            self.t4btn.setText("Power On")
            self.t4btn.setStyleSheet("""
                background-color: #F95A00;
                width: 90px;
                padding: 5px;
                border-radius:5px;
                color:white;
                font-size:10px;
                position: relative;
                left: 40px; 
            """)
        else:
            self.t4btn.setText("Power Off")
            self.t4btn.setStyleSheet("""
                background-color: #474747;
                width: 90px;
                padding: 5px;
                border-radius:5px;
                color:white;
                font-size:10px;
                position: relative;
                left: 40px; 
            """)

# T5
    def t5_toggle(self):
        if self.t5btn.isChecked():
            self.t5btn.setText("Power On")
            self.t5btn.setStyleSheet("""
                background-color: #F95A00;
                width: 90px;
                padding: 5px;
                border-radius:5px;
                color:white;
                font-size:10px;
                position: relative;
                left: 40px; 
            """)
        else:
            self.t5btn.setText("Power Off")
            self.t5btn.setStyleSheet("""
                background-color: #474747;
                width: 90px;
                padding: 5px;
                border-radius:5px;
                color:white;
                font-size:10px;
                position: relative;
                left: 40px; 
            """)


# T6
    def t6_toggle(self):
        if self.t6btn.isChecked():
            self.t6btn.setText("Power On")
            self.t6btn.setStyleSheet("""
                background-color: #F95A00;
                width: 90px;
                padding: 5px;
                border-radius:5px;
                color:white;
                font-size:10px;
                position: relative;
                left: 40px; 
            """)
        else:
            self.t6btn.setText("Power Off")
            self.t6btn.setStyleSheet("""
                background-color: #474747;
                width: 90px;
                padding: 5px;
                border-radius:5px;
                color:white;
                font-size:10px;
                position: relative;
                left: 40px; 
            """)

    # Video Quality
    def adjust_camera_settings(self):
        brightness = self.bslider.value()
        contrast = self.cslider.value()
        gain = self.gslider.value()

        self.camera5.set_brightness(brightness)
        self.camera5.set_brightness(contrast)
        self.camera5.set_brightness(gain)

    def on_slider_value_changed(self,value):
        self.bSliderlabel.setText(str(value))
        self.adjust_camera_settings()

    def contrast_on_slider_value_changed(self,value):
        self.cSliderlabel.setText(str(value))
        self.adjust_camera_settings()

    def gain_on_slider_value_changed(self,value):
        self.gSliderlabel.setText(str(value))
        self.adjust_camera_settings()

    def update_camera_image(self, label, image):
        label.setPixmap(QPixmap.fromImage(image))



    # Camera Toggle 

    # def camera1_toggle(self):
    #     if self.cam1Button.isChecked():
    #         self.cam1Button.setText("Turn Off")
    #         self.cam1Button.setStyleSheet("""
    #             background-color: #F95A00;
    #             width: 90px;
    #             padding: 5px;
    #             border-radius:5px;
    #             color:white;
    #             font-size:10px;
    #             position: relative;
    #             left: 40px; 
    #         """)
    #         self.camera1.start()  # Assuming start method turns on the camera
    #     else:
    #         self.cam1Button.setText("Turn On")
    #         self.cam1Button.setStyleSheet("""
    #             background-color: #474747;
    #             width: 90px;
    #             padding: 5px;
    #             border-radius:5px;
    #             color:white;
    #             font-size:10px;
    #             position: relative;
    #             left: 40px; 
    #         """)
    #         self.camera1.stop()  # Assuming stop method turns off the camera

    # def camera2_toggle(self):
    #     if self.self.cam2Button.isChecked():
    #         self.self.cam2Button.setText("Turn Off")
    #         self.self.cam2Button.setStyleSheet("""
    #             background-color: #F95A00;
    #             width: 90px;
    #             padding: 5px;
    #             border-radius:5px;
    #             color:white;
    #             font-size:10px;
    #             position: relative;
    #             left: 40px; 
    #         """)
    #         self.self.camera2.start()
    #     else:
    #         self.self.cam2Button.setText("Turn On")
    #         self.self.cam2Button.setStyleSheet("""
    #             background-color: #474747;
    #             width: 90px;
    #             padding: 5px;
    #             border-radius:5px;
    #             color:white;
    #             font-size:10px;
    #             position: relative;
    #             left: 40px; 
    #         """)
    #         self.camera2.stop()

    # def camera3_toggle(self):
    #     if self.cam3Button.isChecked():
    #         self.cam3Button.setText("Turn Off")
    #         self.cam3Button.setStyleSheet("""
    #             background-color: #F95A00;
    #             width: 90px;
    #             padding: 5px;
    #             border-radius:5px;
    #             color:white;
    #             font-size:10px;
    #             position: relative;
    #             left: 40px; 
    #         """)
    #         self.camera3.start()
    #     else:
    #         self.cam3Button.setText("Turn On")
    #         self.cam3Button.setStyleSheet("""
    #             background-color: #474747;
    #             width: 90px;
    #             padding: 5px;
    #             border-radius:5px;
    #             color:white;
    #             font-size:10px;
    #             position: relative;
    #             left: 40px; 
    #         """)
    #         self.camera3.stop()



    # def camera4_toggle(self):
    #     if self.cam4Button.isChecked():
    #         self.cam4Button.setText("Turn Off")
    #         self.cam4Button.setStyleSheet("""
    #             background-color: #F95A00;
    #             width: 90px;
    #             padding: 5px;
    #             border-radius:5px;
    #             color:white;
    #             font-size:10px;
    #             position: relative;
    #             left: 40px; 
    #         """)
    #         self.camera4.start()
    #     else:
    #         self.cam4Button.setText("Turn On")
    #         self.cam4Button.setStyleSheet("""
    #             background-color: #474747;
    #             width: 90px;
    #             padding: 5px;
    #             border-radius:5px;
    #             color:white;
    #             font-size:10px;
    #             position: relative;
    #             left: 40px; 
    #         """)
    #         self.camera4.stop()

    # def camera5_toggle(self):
    #     if self.cam5Button.isChecked():
    #         self.cam5Button.setText("Turn Off")
    #         self.cam5Button.setStyleSheet("""
    #             background-color: #F95A00;
    #             width: 90px;
    #             padding: 5px;
    #             border-radius:5px;
    #             color:white;
    #             font-size:10px;
    #             position: relative;
    #             left: 40px; 
    #         """)
    #         self.camera5.start()
    #     else:
    #         self.cam5Button.setText("Turn On")
    #         self.cam5Button.setStyleSheet("""
    #             background-color: #474747;
    #             width: 90px;
    #             padding: 5px;
    #             border-radius:5px;
    #             color:white;
    #             font-size:10px;
    #             position: relative;
    #             left: 40px; 
    #         """)
    #         self.camera5.stop()


    
    def init_ui(self):

        main_layout = QHBoxLayout(self)
        second_col = QVBoxLayout()
        First_Col = QVBoxLayout()
        Third_Col = QVBoxLayout()

        voltage_label = QLabel("Voltage Label")
        voltage_label.setStyleSheet("""
                    
            color: white;
            font-size:12px;
        """)
        voltage_bar = QProgressBar()
        voltage_bar.setStyleSheet("""
        border: 1px solid #F95A00;
        border-radius: 10px;
        height: 20px;
        color:white;
        """)

        First_Col.addWidget(voltage_label)
        First_Col.addWidget(voltage_bar)

        # Cameras
        camera_layout = QHBoxLayout()
        camera_label1 = self.create_camera_label()
        camera_label2 = self.create_camera_label()
        camera_label3 = self.create_camera_label()
        camera_label4 = self.create_camera_label()

        camera_label5 = QLabel()
        camera_label5.setFixedSize(660, 360)
        camera_label5.setStyleSheet("""
        border: 1px solid #F95A00;
        padding: 5px;
        border-radius: 10px;
        overflow: hidden;
""")

        camera_layout.addWidget(camera_label1)
        camera_layout.addWidget(camera_label2)
        camera_layout.addWidget(camera_label3)
        camera_layout.addWidget(camera_label4)
        camera_layout.addStretch()

        First_Col.addLayout(camera_layout)
        First_Col.addWidget(camera_label5)
        First_Col.addStretch()


        # SECOND COL STARTS HERE


        # Communication_Setup
        communicationLayout = QVBoxLayout()
        communicationLayout.setContentsMargins(10, 10, 10, 10)
        communicationLayout.setSpacing(10)
        communicationWidget = QWidget()
        communicationWidget.setLayout(communicationLayout)
        communicationWidget.setStyleSheet("""
         background-color: #222222;
            border-radius: 5px;
            padding: 5px;
        
        """)

        comLabel = QLabel("Communication Setup")
        comLabel.setStyleSheet("""color:white; border-bottom: 1px solid #F95A00;""")

        
        hydraLayout = QHBoxLayout()
        hydraLabel = QLabel('H.Y.D.R.A')
        hydraLabel.setStyleSheet("""color:white;""")
        hydraButton = QPushButton("Connect")
        hydraButton.setStyleSheet("""
        background-color: #F95A00;
        width: 90px;
        padding: 5px;
        border-radius:5px;
        color:white;
        font-size:10px;
        position: relative;
        left: 40px;                 
        """)
        hydraLayout.addWidget(hydraLabel)
        hydraLayout.addSpacerItem(QSpacerItem(60, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        hydraLayout.addWidget(hydraButton)
        hydraLayout.setAlignment(hydraButton, Qt.AlignmentFlag.AlignRight)
        hydraLayout.addStretch()

        communicationLayout.addWidget(comLabel)
        communicationLayout.addLayout(hydraLayout)



        # THRUSTURS SETUP
        thrustersLayout = QVBoxLayout()
        thrustersLayout.setContentsMargins(10, 10, 10, 10)
        thrustersLayout.setSpacing(10)
        thrustersWidget = QWidget()
        thrustersWidget.setLayout(thrustersLayout)
        thrustersWidget.setStyleSheet("""
            background-color: #222222;
            border-radius: 5px;
            padding: 5px;

        """)

        thrusterlabel = QLabel("THRUSTERS POWER")
        thrusterlabel.setStyleSheet("""border-bottom: 1px solid #F95A00""")


        # THRUSTER 01 
        t1layout = QHBoxLayout()
        t1label = QLabel("Thruster 01")
        t1btn = QPushButton("Power Off")
        t1btn.setCheckable(True)
        t1btn.setChecked(False)
        t1btn.clicked.connect(self.t1_toggle)
        t1btn.setStyleSheet("""
            background-color: #474747;
            width: 90px;
            padding: 5px;
            border-radius:5px;
            color:white;
            font-size:10px;
            position: relative;
            left: 40px; 
        """)

        # THRUSTER 02
        t2layout = QHBoxLayout()
        t2label = QLabel("Thruster 02")
        t2btn = QPushButton("Power Off")
        t2btn.setCheckable(True)
        t2btn.setChecked(False)
        t2btn.clicked.connect(self.t2_toggle)
        t2btn.setStyleSheet("""
            background-color: #474747;
            width: 90px;
            padding: 5px;
            border-radius:5px;  
            color:white;
            font-size:10px;
            position: relative;
            left: 40px; 
            """)

        # THRUSTER 03
        t3layout = QHBoxLayout()
        t3label = QLabel("Thruster 03")
        t3btn = QPushButton("Power Off")
        t3btn.setCheckable(True)
        t3btn.setChecked(False)
        t3btn.clicked.connect(self.t3_toggle)
        t3btn.setStyleSheet("""
            background-color: #474747;
            width: 90px;
            padding: 5px;
            border-radius:5px;
            color:white;
            font-size:10px;
            position: relative;
            left: 40px; 
        """)

        # THRUSTER 04
        t4layout = QHBoxLayout()
        t4label = QLabel("Thruster 04")
        t4btn = QPushButton("Power Off")
        t4btn.setCheckable(True)
        t4btn.setChecked(False)
        t4btn.clicked.connect(self.t4_toggle)
        t4btn.setStyleSheet("""
            background-color: #474747;
            width: 90px;
            padding: 5px;
            border-radius:5px;
            color:white;
            font-size:10px;
            position: relative;
            left: 40px; 
        """)
        # THRUSTER 05
        t5layout = QHBoxLayout()
        t5label = QLabel("Thruster 05")
        t5btn = QPushButton("Power Off")
        t5btn.setCheckable(True)
        t5btn.setChecked(False)
        t5btn.clicked.connect(self.t5_toggle)
        t5btn.setStyleSheet("""
            background-color: #474747;
            width: 90px;
            padding: 5px;
            border-radius:5px;
            color:white;
            font-size:10px;
            position: relative;
            left: 40px; 
        """)
        # THRUSTER 06
        t6layout = QHBoxLayout()
        t6label = QLabel("Thruster 06")
        t6btn = QPushButton("Power Off")
        t6btn.setCheckable(True)
        t6btn.setChecked(False)
        t6btn.clicked.connect(self.t6_toggle)
        t6btn.setStyleSheet("""
            background-color: #474747;
            width: 90px;
            padding: 5px;
            border-radius:5px;
            color:white;
            font-size:10px;
            position: relative;
            left: 40px; 
        """)





        t1layout.addWidget(t1label)
        t1layout.addWidget(t1btn)
        t2layout.addWidget(t2label)
        t2layout.addWidget(t2btn)
        t3layout.addWidget(t3label)
        t3layout.addWidget(t3btn)
        t4layout.addWidget(t4label)
        t4layout.addWidget(t4btn)
        t5layout.addWidget(t5label)
        t5layout.addWidget(t5btn)
        t6layout.addWidget(t6label)
        t6layout.addWidget(t6btn)

        thrustersLayout.addWidget(thrusterlabel)
        thrustersLayout.addLayout(t1layout)
        thrustersLayout.addLayout(t2layout)
        thrustersLayout.addLayout(t3layout)
        thrustersLayout.addLayout(t4layout)
        thrustersLayout.addLayout(t5layout)
        thrustersLayout.addLayout(t6layout)



        # SENSITIVITY
        SensitivityLayout = QVBoxLayout()
        SensitivityLayout.setContentsMargins(10, 10, 10, 10)
        SensitivityLayout.setSpacing(10)
        SensitivityWidget = QWidget()
        SensitivityWidget.setLayout(SensitivityLayout)
        SensitivityWidget.setStyleSheet("""
            background-color: #222222;
            border-radius: 5px;
            padding: 5px;

        """)

        SensitivityLabel = QLabel("CONTROLLER SENSITIVITY")
        SensitivityLabel.setStyleSheet("""border-bottom: 1px solid #F95A00;""")

        sensSliderlabel = QLabel("Sensitivity: ",)
        sensSlider =  QSlider(Qt.Orientation.Horizontal)
        sensSlider.setRange(0,100)
        sensSlider.setValue(0)
        sensSlider.valueChanged.connect(lambda value: self.sens_slider_func(value))


        SensitivityLayout.addWidget(SensitivityLabel)
        SensitivityLayout.addLayout(SensitivityLayout)
        SensitivityLayout.addWidget(sensSliderlabel)
        SensitivityLayout.addWidget(sensSlider)



        # Stopwatch
        stopwatchLayout = QVBoxLayout()
        stopwatchLayout.setContentsMargins(10, 10, 10, 10)
        stopwatchLayout.setSpacing(10)
        stopwatchWidget = QWidget()
        stopwatchWidget.setLayout(stopwatchLayout)
        stopwatchWidget.setStyleSheet("""
            background-color: #222222;
            border-radius: 5px;
            padding: 5px;c

        """)

        stoplabel = QLabel("COMPETITION STOPWATCH")
        stoplabel.setStyleSheet("""border-bottom: 1px solid #F95A00;""")

        stopwatchLayout.addWidget(stoplabel)

        watchLabelLayout = QHBoxLayout()
        watcButtonLayout = QHBoxLayout()

        hrBtn = QLabel("00")
        hrBtn.setStyleSheet("""background-color: #373737; width: 30px;""")
        minBtn = QLabel("00")
        minBtn.setStyleSheet("""background-color: #373737; width: 30px;""")
        secBtn = QLabel("00")
        secBtn.setStyleSheet("""background-color: #373737; width: 30px;""")

        startbtn = QPushButton("Start")
        startbtn.setStyleSheet("""
            background-color: #F95A00;
            width: 50px;
            padding: 5px;
            border-radius:5px;
            color:white;
            font-size:10px;
            position: relative;
            left: 40px;                 
        """)
        pausebtn = QPushButton("Pause")
        pausebtn.setStyleSheet("""
            background-color: #F95A00;
            width: 50px;
            padding: 5px;
            border-radius:5px;
            color:white;
            font-size:10px;
            position: relative;
            left: 40px;                 
        """)
        lapbtn = QPushButton("Lap")
        lapbtn.setStyleSheet("""
            background-color: #F95A00;
            width: 50px;
            padding: 5px;
            border-radius:5px;
            color:white;
            font-size:10px;
            position: relative;
            left: 40px;                 
        """)
        Resetbtn = QPushButton("Reset")
        Resetbtn.setStyleSheet("""
            background-color: #F95A00;
            width: 50px;
            padding: 5px;
            border-radius:5px;
            color:white;
            font-size:10px;
            position: relative;
            left: 40px;                 
        """)

        watchLabelLayout.addWidget(hrBtn)
        watchLabelLayout.addWidget(minBtn)
        watchLabelLayout.addWidget(secBtn)

        watcButtonLayout.addWidget(startbtn)
        watcButtonLayout.addWidget(pausebtn)
        watcButtonLayout.addWidget(lapbtn)
        watcButtonLayout.addWidget(Resetbtn)

        stopwatchLayout.addLayout(watchLabelLayout)
        stopwatchLayout.addLayout(watcButtonLayout )

        second_col.addWidget(communicationWidget)
        second_col.addWidget(thrustersWidget)
        second_col.addWidget(SensitivityWidget)
        second_col.addWidget(stopwatchWidget)
        # Second_Col.addStretch()



        #Third Col


        camLayout = QVBoxLayout()
        camLayout.setContentsMargins(10, 10, 10, 10)
        camLayout.setSpacing(10)

        camWidget = QWidget()
        camWidget.setLayout(camLayout)
        camWidget.setStyleSheet("""
            background-color: #222222;
            border-radius: 5px;
            padding: 5px;
        """)


        # Camera Controller
        CameraLabel = QLabel("VIDEO CONTROL")
        CameraLabel.setStyleSheet("""color:white; border-bottom: 1px solid #F95A00; """)


        brightnesSlider = QHBoxLayout() 
        brightnesLabel = QLabel("Brightness")
        brightnesLabel.setStyleSheet("""color:white """)

        bSliderlabel = QLabel()
        bSliderlabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bslider = QSlider(Qt.Orientation.Horizontal)
        bslider.setRange(0,100)
        bslider.setValue(0)
        bslider.valueChanged.connect(self.on_slider_value_changed)


        brightnesSlider.addWidget(brightnesLabel)
        brightnesSlider.addWidget(bSliderlabel)
        brightnesSlider.addWidget(bslider)

        # CONTRAST 
        contrastSlider = QHBoxLayout() 
        contrastLabel = QLabel("Contrast")
        contrastLabel.setStyleSheet("""color:white """)

        cSliderlabel = QLabel()
        cSliderlabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cslider = QSlider(Qt.Orientation.Horizontal)
        cslider.setRange(0,100)
        cslider.setValue(0)
        cslider.valueChanged.connect(self.contrast_on_slider_value_changed)


        contrastSlider.addWidget(contrastLabel)
        contrastSlider.addWidget(cSliderlabel)
        contrastSlider.addWidget(cslider)
    # 

        # BOOST GAIN 
        gainSlider = QHBoxLayout() 
        gainLabel = QLabel("Contrast")
        gainLabel.setStyleSheet("""color:white """)

        gSliderlabel = QLabel()
        gSliderlabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        gslider = QSlider(Qt.Orientation.Horizontal)
        gslider.setRange(0,100)
        gslider.setValue(0)
        gslider.valueChanged.connect(self.gain_on_slider_value_changed)


        gainSlider.addWidget(gainLabel)
        gainSlider.addWidget(gSliderlabel)
        gainSlider.addWidget(gslider)
    # 


        camLayout.addWidget(CameraLabel)
        camLayout.addLayout(brightnesSlider)
        camLayout.addLayout(contrastSlider)
        camLayout.addLayout(gainSlider)


    # Camera on Off code
        camOnOffLayout = QVBoxLayout()
        camOnOffLayout.setContentsMargins(10, 10, 10, 10)
        camOnOffLayout.setSpacing(10)
        camOnOffWidget = QWidget()
        camOnOffWidget.setLayout(camOnOffLayout)
        camOnOffWidget.setStyleSheet("""
            background-color: #222222;
        border-radius: 5px;
            padding: 5px;c

        """)

        CameraOnLabel = QLabel("CAMERAS")
        CameraOnLabel.setStyleSheet("""border-bottom: 1px solid #F95A00;""")


        CamLayout1 = QHBoxLayout()
        cam1label = QLabel("Camera 01")
        cam1Button = QPushButton("Turn On")
        cam1Button.setStyleSheet("""
        background-color: #474747;
        width: 90px;
        padding: 5px;
        border-radius:5px;
        color:white;
        font-size:10px;
        position: relative;
        left: 40px; 
        """)

        CamLayout2 = QHBoxLayout()
        cam2label = QLabel("Camera 02")
        cam2Button = QPushButton("Turn On")
        cam2Button.setStyleSheet("""
        background-color: #474747;
        width: 90px;
        padding: 5px;
        border-radius:5px;
        color:white;
        font-size:10px;
        position: relative;
        left: 40px; 
        """)

        CamLayout3 = QHBoxLayout()
        cam3label = QLabel("Camera 03")
        cam3Button = QPushButton("Turn On")
        cam3Button.setStyleSheet("""
        background-color: #474747;
        width: 90px;
        padding: 5px;
        border-radius:5px;
        color:white;
        font-size:10px;
        position: relative;
        left: 40px; 
        """)

        CamLayout4 = QHBoxLayout()
        cam4label = QLabel("Camera 04")
        cam4Button = QPushButton("Turn On")
        cam4Button.setStyleSheet("""
        background-color: #474747;
        width: 90px;
        padding: 5px;
        border-radius:5px;
        color:white;
        font-size:10px;
        position: relative;
        left: 40px; 
        """)

        CamLayout5 = QHBoxLayout()
        cam5label = QLabel("Camera 05")
        cam5Button = QPushButton("Turn On")
        cam5Button.setStyleSheet("""
        background-color: #474747;
        width: 90px;
        padding: 5px;
        border-radius:5px;
        color:white;
        font-size:10px;
        position: relative;
        left: 40px; 
        """)



        CamLayout1.addWidget(cam1label)
        CamLayout1.addWidget(cam1Button)
        CamLayout2.addWidget(cam2label)
        CamLayout2.addWidget(cam2Button)
        CamLayout3.addWidget(cam3label)
        CamLayout3.addWidget(cam3Button)
        CamLayout4.addWidget(cam4label)
        CamLayout4.addWidget(cam4Button)
        CamLayout5.addWidget(cam5label)
        CamLayout5.addWidget(cam5Button)


        camOnOffLayout.addWidget(CameraOnLabel)
        camOnOffLayout.addLayout(CamLayout1)
        camOnOffLayout.addLayout(CamLayout2)
        camOnOffLayout.addLayout(CamLayout3)
        camOnOffLayout.addLayout(CamLayout4)
        camOnOffLayout.addLayout(CamLayout5)



        # Task Setup

        TaskLayout = QVBoxLayout()
        TaskLayout.setContentsMargins(10, 10, 10, 10)
        TaskLayout.setSpacing(10)
        TaskWidget = QWidget()
        TaskWidget.setLayout(TaskLayout)
        TaskWidget.setStyleSheet("""
            background-color: #222222;
            border-radius: 5px;
            padding: 5px;
            
        """)
        taskLabel = QLabel("TASK SETUP")
        taskLabel.setStyleSheet("""border-bottom: 1px solid #F95A00;""")


        coralReafLayout = QHBoxLayout()
        coralLabel = QLabel("Coral Reaf Health")
        coralButton = QPushButton("Turn On")
        coralButton.setStyleSheet("""
        background-color: #F95A00;
        width: 90px;
        padding: 5px;
        border-radius:5px;
        color:white;
        font-size:10px;
        position: relative;
        left: 40px;                 
        """)

        objDetectionLayout = QHBoxLayout()
        objectLabel = QLabel("Object Detection")
        objectButton = QPushButton("Turn On")
        objectButton.setStyleSheet("""
        background-color: #F95A00;
        width: 90px;
        padding: 5px;
        border-radius:5px;
        color:white;
        font-size:10px;
        position: relative;
        left: 40px;                 
        """)
        coralReafLayout.addWidget(coralLabel)
        coralReafLayout.addWidget(coralButton)
        objDetectionLayout.addWidget(objectLabel)
        objDetectionLayout.addWidget(objectButton)

        TaskLayout.addWidget(taskLabel)
        TaskLayout.addLayout(coralReafLayout)
        TaskLayout.addLayout(objDetectionLayout) 



        Third_Col.addWidget(camWidget)
        Third_Col.addWidget(camOnOffWidget)
        Third_Col.addWidget(TaskWidget)
        # Third_Col.addStretch()

        # Maiin Layout Setup

        main_layout.addLayout(First_Col)
        main_layout.addLayout(second_col)
        main_layout.addLayout(Third_Col)
        # main_layout.addStretch()
        self.setLayout(main_layout)

        # camera1 = Camera(camera_id=1)
        # camera1.frameCaptured.connect(lambda image: self.update_camera_image(camera_label1, image))
        # camera1.start()

        # camera2 = Camera(camera_id=2)
        # camera2.frameCaptured.connect(lambda image: self.update_camera_image(camera_label2, image))
        # camera2.start()

        # camera3 = Camera(camera_id=3)
        # camera3.frameCaptured.connect(lambda image: self.update_camera_image(camera_label3, image))
        # camera3.start()

        # camera4 = Camera(camera_id=4)
        # camera4.frameCaptured.connect(lambda image: self.update_camera_image(camera_label4, image))
        # camera4.start() 

        # camera5 = Camera(camera_id=5)
        # camera5.frameCaptured.connect(lambda image: self.update_camera_image(camera_label5, image))
        # camera5.start()

        # cam1Button.clicked.connect(self.camera1_toggle)
        # cam2Button.clicked.connect(self.camera2_toggle)
        # cam3Button.clicked.connect(self.camera3_toggle) 
        # cam4Button.clicked.connect(self.camera4_toggle) 
        # cam5Button.clicked.connect(self.camera5_toggle) 

        # Video Quality Sliders
        bslider.valueChanged.connect(self.adjust_camera_settings)
        cslider.valueChanged.connect(self.adjust_camera_settings)
        gslider.valueChanged.connect(self.adjust_camera_settings)

        # camera1.stop()
        # camera2.stop()
        # camera3.stop()
        # camera4.stop()
        # camera5.stop()