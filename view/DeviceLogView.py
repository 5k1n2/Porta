from __future__ import annotations
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPlainTextEdit, QPushButton
from PySide6.QtGui import Qt, QFont

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.DeviceModel import DeviceModel

class DeviceLogView(QWidget):
    
    def __init__(self, model:DeviceModel):
        super().__init__()
        
        self.device = model

        
        with open("view/stylesheet.qss", "r") as k:
            self.setStyleSheet(k.read())
        
        # Layout Setup
        self.main_layout = QVBoxLayout()    
        
        
        
        titleFont = QFont("Serif", 18, QFont.Bold)        
        self.titleLabel = QLabel("{} Logs".format(self.device.deviceInfo["fancyName"]))
        self.titleLabel.setAlignment(Qt.AlignHCenter)
        self.titleLabel.setFont(titleFont)
        
        self.main_layout.addWidget(self.titleLabel)   

        self.colored_widget = QWidget()
        self.colored_widget.setLayout(self.main_layout)
        self.colored_widget_layout = QVBoxLayout()
        self.colored_widget_layout.addWidget(self.colored_widget)
        self.setLayout(self.colored_widget_layout)
        
        
        
        self.contentLayout = QHBoxLayout()
        

        self.logWidget = QPlainTextEdit()
        self.contentLayout.addWidget(self.logWidget, 1)
        self.logWidget.setReadOnly(True)

        # self.update_log()

        
        
        # Buttonrow
        
        self.buttonRow = QHBoxLayout()
        
        self.logButton = QPushButton("Clear Log")
        self.logButton.setFixedSize(150, 40)
        self.logButton.clicked.connect(self.clear_log)
        
        self.cancelButton = QPushButton("Close")
        self.cancelButton.setFixedSize(150, 40)
        self.cancelButton.clicked.connect(self.close_window)

        self.buttonRow.addWidget(self.logButton)
        self.buttonRow.addWidget(self.cancelButton)
        self.buttonRow.setAlignment(Qt.AlignRight)
                
        self.main_layout.addLayout(self.contentLayout)
        self.main_layout.addLayout(self.buttonRow)

        self.resize(self.sizeHint())
        
        self.device.subscribe_log_update(self.update_log_view)
        
        self.device.log_update()
        
        self.device.add_to_log("Log opened")
        
        self.show()
        
    def close_window(self):
        self.close()
        
    def clear_log(self):
        self.device.log.clear()
        self.device.log_update()
        
    def update_log_view(self):
        self.logWidget.clear()
        for log in self.device.log:
            self.logWidget.appendPlainText(log)
            
        if(len(self.device.log) == 0):
            self.logButton.setEnabled(False)
        else:
            self.logButton.setEnabled(True)