from __future__ import annotations

import PySide6
from PySide6.QtWidgets import QWidget, QPlainTextEdit, QPushButton, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy
from PySide6.QtGui import Qt, QPixmap
from PySide6 import QtSvgWidgets, QtSvg
from view.Tab import Tab
from model import GlobalLog, ActiveEvent

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.LeftSideBar import Button, LeftSideBar


class LeftSideBarView(QWidget):
    def __init__(self, parent, model: LeftSideBar):
        super().__init__()
        
        self.parent = parent
        self.model = model
        self.main_model = model.model
        self.setFixedWidth(200)
        self.buttons = []
        self.current_widget = None
        
        self.mainLayout = QVBoxLayout()
                
        self.coloredWidget = QWidget()
        self.coloredWidgetLayout = QVBoxLayout()
        self.coloredWidget.setLayout(self.coloredWidgetLayout)
        self.mainLayout.addWidget(self.coloredWidget)
        
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(0,0,0,0)
        
        self.model.content_widget.setLayout(self.content_layout)
        
        
        # Vertex Logo
        
        self.logo = QLabel()
        pixmap = QPixmap("ui/icons/vertexVR_logo_emulator.png")
        self.logo.setPixmap(pixmap.scaledToHeight(140, Qt.TransformationMode.SmoothTransformation))
        
        self.button_layout = QVBoxLayout()
        
        self.coloredWidgetLayout.addWidget(self.logo)
        self.coloredWidgetLayout.addItem(QSpacerItem(100,80, QSizePolicy.Maximum, QSizePolicy.Maximum))
        self.coloredWidgetLayout.addLayout(self.button_layout)
        self.coloredWidgetLayout.addItem(QSpacerItem(1,1, QSizePolicy.MinimumExpanding, QSizePolicy.Expanding))
        
        
        self.setLayout(self.mainLayout)


        # add gamehost

        self.addGamehost = Tab("Add Gamehost")
        self.coloredWidgetLayout.addWidget(self.addGamehost)
        self.addGamehost.button.clicked.connect(self.main_model.add_gamehost)


        # Add start stop Button

        self.startButton = Tab("Start")
        self.stopButton = Tab("Stop")
        self.stopButton.setEnabled(False)
        
        self.coloredWidgetLayout.addWidget(self.startButton)
        self.coloredWidgetLayout.addWidget(self.stopButton)
        
        self.startButton.button.clicked.connect(self.main_model.start_server)
        self.stopButton.button.clicked.connect(self.main_model.stop_server)

        ActiveEvent.subscribe_to_activechange(self.update_startButtons)
        
        self.lbl_active = QLabel("None")
        self.coloredWidgetLayout.addWidget(self.lbl_active, alignment=Qt.AlignCenter)
        
        ActiveEvent.update_active(False)

        
        
        
        self.mainLayout.setContentsMargins(0,0,0,0)
        
        self.setStyleSheet("""
                        QWidget{ 
                        
                            background-color: #35363b;
                            border-radius: 10px;
                            
                            }""")


    
    def add_button(self, btn: Button):
        
        tab = Tab(btn.name)
        btn.tab = tab
        self.buttons.append(btn)
        tab.button.clicked.connect(lambda: self.button_clicked(btn))

        self.button_layout.addWidget(tab)

        if self.current_widget is None:
            self.deactivate_button(self.buttons[0])
            self.set_content(btn)
        
        
    def button_clicked(self, btn: Button):
        self.deactivate_button(btn)
        self.set_content(btn)
        
            
    def deactivate_button(self, button: Button):
        k: Tab
        for k in self.buttons:
            k.tab.setEnabledButton(True)
        
            
        button.tab.setEnabledButton(False)
        
        
    def set_content(self, btn: Button):

        if(self.current_widget is not None):
            self.content_layout.removeWidget(self.current_widget)
            # self.current_widget.deleteLater()
            btn.widget.window = None
            

        self.current_widget = btn.widget.get_window()
        self.content_layout.addWidget(self.current_widget)
        GlobalLog.add_to_log("{} Site opened".format(btn.name))
        

    def update_startButtons(self, active):
        if(active):
            self.startButton.setEnabled(False)
            self.stopButton.setEnabled(True)
            self.lbl_active.setText("Server Online")
            
            
        else:
            self.startButton.setEnabled(True)
            self.stopButton.setEnabled(False)
            self.lbl_active.setText("Server Offline")
            