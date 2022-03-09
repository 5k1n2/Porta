from view.DeviceWidget import DeviceWidget
from model.DeviceInfo import DeviceInfo

class DeviceModel(object):
    
    def __init__(self) -> None:
        
        self.window = None
        self.deviceInfo = DeviceInfo("tset")
        self.connected_Host = "test"
        self.connected_Port = "Port"
        self.inputs = []
        self.active_status = False
        
        
    def get_device_widget(self):
        
        self.window = DeviceWidget(self)
        return self.window
    
    def open_log(self):
        print("open log")