from __future__ import annotations

from PySide6.QtWidgets import QWidget, QTableWidget, QMenu, QPushButton, QLabel, QVBoxLayout, QSizePolicy, QHBoxLayout, QSpacerItem
from PySide6.QtGui import QCursor, QPen, QBrush, QAction, QLinearGradient, Qt, QFont, QMouseEvent


from typing import TYPE_CHECKING



class DeviceWidget(QWidget):
    def __init__(self, model):
        super().__init__()

        self.model = model
        self.setFixedSize(215,350)

        # Layout Setup
        self.main_layout = QVBoxLayout()        

        self.colored_widget = QWidget()
        self.colored_widget.setLayout(self.main_layout)
        self.colored_widget_layout = QVBoxLayout()
        self.colored_widget_layout.addWidget(self.colored_widget)
        self.setLayout(self.colored_widget_layout)
        
        # Remove Margins
        self.main_layout.setContentsMargins(15,15,15,15)
        self.colored_widget_layout.setContentsMargins(0,0,0,0)
        
        titleFont = QFont("Serif", 18, QFont.Bold)
        secondFont = QFont("Verdana", 13)
        descriptionFont = QFont("Verdana", 9)
        
        self.title = QLabel(self.model.deviceInfo.title)
        self.title.setFont(titleFont)
        self.title.setAlignment(Qt.AlignCenter)   

        self.fancyName = QLabel(self.model.deviceInfo.fancyName)
        self.fancyName.setFont(secondFont)
        self.fancyName.setAlignment(Qt.AlignCenter)   
        
        self.description = QLabel(self.model.deviceInfo.description)
        self.description.setFont(descriptionFont)
        self.description.setAlignment(Qt.AlignCenter)   
        self.description.setWordWrap(True)   
        
        self.name = self.model.deviceInfo.description
        
        self.main_layout.addWidget(self.title, alignment=Qt.AlignTop)
        self.main_layout.addWidget(self.fancyName, alignment=Qt.AlignTop)
        self.main_layout.addWidget(self.description, alignment=Qt.AlignTop)
        # self.main_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        
        self.main_layout.addItem(QSpacerItem(1,1, QSizePolicy.MinimumExpanding, QSizePolicy.Expanding))
        
        
        
        # Connected to Label
        
        self.connectionLabel = QLabel()
        self.set_connecton_label()
        self.main_layout.addWidget(self.connectionLabel)
        
        
        
        # Button Layout 2
        self.buttonLayout2 = QHBoxLayout()
        
        self.startButton = QPushButton("Start")
        self.startButton.setMinimumHeight(30)
        self.startButton.clicked.connect(self.start_button_clicked)
        
        self.stopButton = QPushButton("Stop")
        self.stopButton.setMinimumHeight(30)
        self.stopButton.setEnabled(False)
        self.stopButton.clicked.connect(self.stop_button_clicked)
        
        self.buttonLayout2.addWidget(self.stopButton, alignment=Qt.AlignBottom)
        self.buttonLayout2.addWidget(self.startButton, alignment=Qt.AlignBottom)

        self.main_layout.addLayout(self.buttonLayout2)
        
        # Handle mouse click event to show menu
        self.mousePressEvent = self.mouseclick
        # self.rightclicked.connect(lambda x: print("widget rightclicked"))        
        
        # Button Layout 1
        self.buttonLayout = QHBoxLayout()
        
        self.settingButton = QPushButton("Settings")
        self.settingButton.setMinimumHeight(30)
        self.settingButton.clicked.connect(self.settings_button_clicked)
        
        self.logButton = QPushButton("Log")
        self.logButton.setMinimumHeight(30)
        self.logButton.clicked.connect(self.model.open_log)
        
        self.buttonLayout.addWidget(self.settingButton, alignment=Qt.AlignBottom)
        self.buttonLayout.addWidget(self.logButton, alignment=Qt.AlignBottom)

        self.main_layout.addLayout(self.buttonLayout)
        
        self.colored_widget.setProperty("active_status", self.model.active_status)
        
        self.set_border_color()
        
        


        # Color Widget
        self.setStyleSheet("""
                        QWidget{ 
                        
                            background-color: grey;
                            border-radius: 5px;

                            
                        }
                        
                        QWidget[active_status="green"]{ 
                            border-style: solid;
                            border-color: #a0ff99;
                            border-width: 3px;
                            
                            }
                            
                        QWidget[active_status="yellow"]{ 
                            border-style: solid;
                            border-color: #dcff7d;
                            border-width: 3px;
                            
                            }
                            
                        QWidget[active_status="red"]{ 
                            border-style: solid;
                            border-color: #ff8a7d;
                            border-width: 3px;
                            
                            }
                            
                        QPushButton{
                            background-color: #81ade3;
                        }
                        
                        QPushButton:hover{
                            background-color: #318bf7;
                        }

                        QPushButton:pressed{
                            background-color: #e1eaf5;
                        }
                            
                            
                            """)
    def start_button_clicked(self):
        rslt = self.model.enable_device()
        self.colored_widget.setProperty("active_status", "green")
        self.set_border_color()
        if(rslt):
            self.startButton.setEnabled(False)
            self.stopButton.setEnabled(True)
    
    def stop_button_clicked(self):
        rslt = self.model.disable_device()
        self.colored_widget.setProperty("active_status", "red")
        self.set_border_color()
        if(rslt):
            self.startButton.setEnabled(True)
            self.stopButton.setEnabled(False)
        
    def settings_button_clicked(self):
        self.model.open_settings()       

        
    def set_border_color(self):
        if(self.model.active_status == True):
            self.colored_widget.setProperty("active_status", "green")
        else:
            self.colored_widget.setProperty("active_status", "red")
            
        self.colored_widget.style().unpolish(self.colored_widget)
        self.colored_widget.style().polish(self.colored_widget)
        self.set_connecton_label()
    
    
    
    def mouseclick(self, sender: QMouseEvent):
        if(sender.button() == Qt.MouseButton.RightButton):
            self.open_menu(sender)
        

    def open_menu(self, sender: QMouseEvent):
        menu = QMenu(self)      

        closeAction = QAction("Close", self)
        closeAction.triggered.connect(self.model.remove_device)
        
        duplicateAction = QAction("Duplicate", self)
        duplicateAction.triggered.connect(self.model.duplicate_device)
        
        menu.addActions([duplicateAction, closeAction])
        menu.popup(sender.globalPosition().toPoint())
        
    def set_connecton_label(self):
        self.connection_lbl = "Connected to: {}:{}".format(self.model.connected_Host, self.model.connected_Port)
        if self.model.connected_Host is None:
            self.connectionLabel.setText("")
        else:
            self.connectionLabel.setText(self.connection_lbl)
        
    
        
