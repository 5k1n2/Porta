from view.DeviceWidget import DeviceWidget
from model.DeviceInfo import DeviceInfo

class DeviceModel(object):
    
    def __init__(self) -> None:
        
        self.window = None
        self.deviceInfo = DeviceInfo()
        self.connected_Host = "test"
        self.connected_Port = "Port"
        self.inputs = []
        self.active_status = False
        self.data = None
        
        
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
        