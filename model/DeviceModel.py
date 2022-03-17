import string
import threading
from tokenize import String
from view.DeviceWidget import DeviceWidget
from model.DeviceInfo import DeviceInfo
import datetime
from threading import Timer
from multiprocessing import Pool
from PySide6.QtCore import Signal, QObject

class DeviceModel(QObject):
    
    newLog = Signal(str)
    clearAllLogs = Signal()
    updateElement = Signal(dict)

    
    def __init__(self) -> None:
        super().__init__()
        self.window = None
        self.deviceInfo = DeviceInfo(self)
        self.connected_Host = "test"
        self.connected_Port = "Port"
        self.inputs = []
        self.log = []
        self.logevent = []
        
        self.active_status = False
        self.data = None
        self.seconds_since_last_action = None
        self.last_datetime = datetime.datetime.now()
        self.set_update_timer()

        
        
    def get_device_widget(self):
        
        if(self.window is None):
            self.window = DeviceWidget(self)
            self.window.clearLog.connect(lambda: self.clearAllLogs.emit())
        return self.window
    
    def open_log(self):
        print("open log")
        
    def set_connection_status(self, active: bool):
        self.active_status = active
        if(self.window is not None):
            self.window.set_border_color()
            
    def update_log(self, dict):
        
        self.last_datetime = datetime.datetime.now()
        self.add_to_log("New input recieved: {}".format(dict))
            
    def timer_update(self):
        
        
        
        tmp = datetime.datetime.now() - self.last_datetime
        self.seconds_since_last_action = tmp.seconds
        
        if(self.window):
            self.window.update_card_labels()
        
        if(self.active_status):
            self.set_update_timer()
        else:
            self.seconds_since_last_action = "No Connection"
            self.window.update_card_labels()
            
        
    def set_update_timer(self):
        
        self.timer = Timer(1, self.timer_update)
        
        self.timer.start()
        
        
    def subscribe_log_update(self, k):
        if(k not in self.logevent):
            self.logevent.append(k)
            
    def unsubscribe_log_update(self, k):
        if(k in self.logevent):
            self.logevent.remove(k)
            
    def add_to_log(self, msg):
        
        self.log.append(msg)
        
        self.newLog.emit(msg)
            
