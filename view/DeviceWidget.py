from __future__ import annotations
import threading

from PySide6.QtWidgets import QWidget, QTableWidget, QMenu, QPushButton, QLabel, QVBoxLayout, QSizePolicy, QHBoxLayout, QSpacerItem
from PySide6.QtGui import QCursor, QPen, QBrush, QAction, QLinearGradient, Qt, QFont, QMouseEvent
from PySide6.QtCore import Signal

from model.Overview import Overview
from view.DeviceLogView import DeviceLogView

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.DeviceModel import DeviceModel


class DeviceWidget(QWidget):
    
    clearLog = Signal()
    
    def __init__(self, model:DeviceModel):
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
        
        self.title = QLabel(self.model.deviceInfo["name"])
        self.title.setFont(titleFont)
        self.title.setAlignment(Qt.AlignCenter)   

        self.fancyName = QLabel(self.model.deviceInfo["fancyName"])
        self.fancyName.setFont(secondFont)
        self.fancyName.setAlignment(Qt.AlignCenter)   
        
        self.description = QLabel(self.model.deviceInfo["description"])
        self.description.setFont(descriptionFont)
        self.description.setAlignment(Qt.AlignCenter)   
        self.description.setWordWrap(True)   
        
        self.name = self.model.deviceInfo["description"]
        
        self.main_layout.addWidget(self.title, alignment=Qt.AlignTop)
        self.main_layout.addWidget(self.fancyName, alignment=Qt.AlignTop)
        self.main_layout.addWidget(self.description, alignment=Qt.AlignTop)
        # self.main_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        
        self.main_layout.addItem(QSpacerItem(1,1, QSizePolicy.MinimumExpanding, QSizePolicy.Expanding))
        
        
        
        # Connected to Label
        
        self.last_update_lbl = QLabel()
        # self.last_update_lbl.setText(self.model.seconds_since_last_action)
        self.main_layout.addWidget(self.last_update_lbl)
        
        self.connectionLabel = QLabel()
        self.set_connecton_label()
        self.main_layout.addWidget(self.connectionLabel)
        
                
        # Button Overview
        self.overview_btn = QPushButton("Overview")
        self.overview_btn.setMinimumHeight(30)
        self.overview_btn.clicked.connect(self.overview_btn_clicked)

        self.main_layout.addWidget(self.overview_btn)
        
        # Button Layout 2
        self.pause_btn = QPushButton("Pause Transfer")
        self.pause_btn.setMinimumHeight(30)
        self.pause_btn.setCheckable(True)
        self.pause_btn.clicked.connect(self.pause_btn_clicked)

        self.main_layout.addWidget(self.pause_btn)
        

        
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
        self.logButton.clicked.connect(self.log_btn_clicked)
        
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
                            
                        QPushButton:checked{
                            background-color: #5e5e5e;
                        }
                        
                        QPushButton:checked:selected {
                            background-color: #60798B;
                        }
                            
                            """)
        
        self.update_card_labels()
        
    def pause_btn_clicked(self, sender):
        
        print(sender)
        
    def overview_btn_clicked(self, sender):
        
        self.overview = Overview(self.model)
        self.overview.get_window()

    def log_btn_clicked(self, sender):
        
        self.logview = DeviceLogView(self.model)
        self.logview.show()
        self.logview.clearLog.connect(lambda: self.clearLog.emit())
        print(threading.current_thread())
        
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
        

    

    
    def update_card_labels(self):
        
        self.title.setText(self.model.deviceInfo["name"])
        self.fancyName.setText(self.model.deviceInfo["fancyName"])
        self.description.setText(self.model.deviceInfo["description"])
        self.set_connecton_label()        
        self.last_update_lbl.setText("Time since last Update {}s".format(self.model.seconds_since_last_action))
        