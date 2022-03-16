from view.DeviceWidget import DeviceWidget
from model.DeviceInfo import DeviceInfo
import datetime
from threading import Timer
from multiprocessing import Pool

class DeviceModel(object):
    
    def __init__(self) -> None:
        
        self.window = None
        self.deviceInfo = DeviceInfo(self)
        self.connected_Host = "test"
        self.connected_Port = "Port"
        self.inputs = []
        self.active_status = False
        self.data = None
        self.seconds_since_last_action = None
        self.last_datetime = datetime.datetime.now()
        self.set_update_timer()

        
        
    def get_device_widget(self):
        
        if(self.window is None):
            self.window = DeviceWidget(self)
        return self.window
    
    def open_log(self):
        print("open log")
        
    def set_connection_status(self, active: bool):
        self.active_status = active
        if(self.window is not None):
            self.window.set_border_color()
            
    def update_log(self):
        
        self.last_datetime = datetime.datetime.now()
            
    def timer_update(self):
        
        tmp = datetime.datetime.now() - self.last_datetime
        self.seconds_since_last_action = tmp.seconds
        
        if(self.window):
            self.window.update_card_labels()
        
        self.set_update_timer()
        
    def set_update_timer(self):
        
        self.timer = Timer(1, self.timer_update)
        self.timer.start()
        