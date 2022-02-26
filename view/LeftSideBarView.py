from __future__ import annotations

import PySide6
from PySide6.QtWidgets import QWidget, QPlainTextEdit, QPushButton, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy
from PySide6.QtGui import Qt, QPixmap
from PySide6 import QtSvgWidgets, QtSvg
from view.Tab import Tab

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.LeftSideBar import Button, LeftSideBar


class LeftSideBarView(QWidget):
    def __init__(self, parent, model: LeftSideBar):
        super().__init__()
        
        self.parent = parent
        self.model = model
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
        
        self.mainLayout.setContentsMargins(0,0,0,0)
        
        self.setStyleSheet("""
                        QWidget{ 
                        
                            background-color: #35363b;
                            border-radius: 10px;
                            
                            }""")
    
    def add_button(self, btn: Button):
        
        tab = Tab(btn.name)       
        self.buttons.append(tab)
        tab.button.clicked.connect(lambda: self.button_clicked(btn, tab))
        
        self.button_layout.addWidget(tab)
        
        
    def button_clicked(self, btn: Button, tab: Tab):
        self.deactivate_button(tab)
        self.set_content(btn)
        
            
    def deactivate_button(self, button: Tab):
        k: Tab
        for k in self.buttons:
            k.setEnabledButton(True)
        
            
        button.setEnabledButton(False)
        
        
    def set_content(self, btn: Button):

        if(self.current_widget is not None):
            self.content_layout.removeWidget(self.current_widget)
            # self.current_widget.deleteLater()

        self.current_widget = btn.widget(btn.name)
        self.content_layout.addWidget(self.current_widget)