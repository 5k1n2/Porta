from model.DeviceInfo import DeviceInfo
from PySide6.QtCore import Signal, QObject
from view.GamehostView import GamehostView
import datetime


class GamehostModel(QObject):
    
    updateElement = Signal(dict)
    def __init__(self) -> None:
        super().__init__()
        
        self.deviceInfo = DeviceInfo(self)
        self.window = None
        self.connected_Host = "test"
        self.connected_Port = "Port"
        
        self.active_status = False
        self.data = None
        self.seconds_since_last_action = None
        self.last_datetime = datetime.datetime.now()
        # self.set_update_timer()
        
        
    def get_device_widget(self):
        
        if(self.window is None):
            self.window = GamehostView(self)
            self.window.clearLog.connect(lambda: self.clearAllLogs.emit())
        return self.window