from view.PortaMainView import PortaMainView
from model.LeftSideBar import LeftSideBar
from model.LogWidget import LogWidget
from model.Dashboard import Dasboard
from model import ActiveEvent



class PortaMain(object):
    def __init__(self) -> None:
        
        self.window = self.get_window()
        

        self.active = False
        
        self.log_widget = LogWidget()
        self.left_side_bar = LeftSideBar(self.window.content_widget, self)
        
        self.dasboard = Dasboard()
        
        
        self.left_side_bar.add_new_button("Dashboard", self.dasboard)
        self.left_side_bar.add_new_button("Devices", self.dasboard)
        self.left_side_bar.add_new_button("Gamehosts", self.log_widget)
        self.left_side_bar.add_new_button("Settings", self.log_widget)
        self.left_side_bar.add_new_button("Performance", self.log_widget)
        self.left_side_bar.add_new_button("Log", self.log_widget)
        
        
        self.window.show()
        
        self.window.window_layout.addWidget(self.left_side_bar.left_side_bar)
        
    def get_window(self):
        return PortaMainView()
    
    
    def start_server(self):
        self.active = True
        ActiveEvent.update_active(True)
        
    def stop_server(self):
        self.active = False
        ActiveEvent.update_active(False)
        
        
