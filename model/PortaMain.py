from view.PortaMainView import PortaMainView
from model.LeftSideBar import LeftSideBar
from model.LogWidget import LogWidget

from PySide6.QtWidgets import QPushButton


class PortaMain(object):
    def __init__(self) -> None:
        
        self.window = self.get_window()
        

        
        
        self.log_widget = None
        self.left_side_bar = LeftSideBar(self.window.content_widget)
        
        
        self.left_side_bar.add_new_button("Dashboard", QPushButton)
        self.left_side_bar.add_new_button("Devices", QPushButton)
        self.left_side_bar.add_new_button("Gamehosts", QPushButton)
        self.left_side_bar.add_new_button("Settings", QPushButton)
        self.left_side_bar.add_new_button("Performance", QPushButton)
        # self.left_side_bar.add_new_button("Log", self.log_widget.window)
        
        
        self.window.show()
        
        self.window.window_layout.addWidget(self.left_side_bar.left_side_bar)
        
    def get_window(self):
        return PortaMainView()