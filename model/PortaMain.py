from __future__ import annotations

from view.PortaMainView import PortaMainView
from model.LeftSideBar import LeftSideBar
from model.LogWidget import LogWidget
from model.Dashboard import Dasboard
from model.DeviceInfo import DeviceInfo
from model.GamehostModel import GamehostModel
from model import ActiveEvent
from Sockets.SocketReader import SocketReader
from Sockets.SocketConnection import SocketConnection

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.DeviceModel import DeviceModel

class PortaMain(object):
    def __init__(self) -> None:
        
        self.window = self.get_window()
        
        self.socketReader = None
        self.devices: list[DeviceModel] = []
        self.gamehosts = []
        self.active = False
        
        self.log_widget = LogWidget()
        self.left_side_bar = LeftSideBar(self.window.content_widget, self)
        
        self.dasboard = Dasboard(self)
        
        
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
        self.socketReader = SocketReader(self)
        self.socketReader.setObjectName("SocketReaderThread")
        self.socketReader.newDevice.connect(self.add_device)
        self.socketReader.start()
        
    def stop_server(self):
        self.active = False
        ActiveEvent.update_active(False)
        self.socketReader.stop()
        self.socketReader.join()
        
        self.socketReader = None
        
    def add_device(self, device: DeviceModel):
        if(device.deviceInfo["kind"] == 0):
            
            for singleDevice in self.devices:
                if(singleDevice.connected_Host == device.connected_Host):
                    self.remove_device(singleDevice)
            
            self.dasboard.window.add_device(device.get_device_widget())
            self.devices.append(device)
        else:
            self.dasboard.window.add_device(device.get_device_widget())
            self.gamehosts.append(device)
            
    def remove_device(self, device: DeviceModel):
        self.devices.remove(device)
        self.dasboard.window.remove_device(device.get_device_widget())

    def add_gamehost(self):
        self.gamehost = SocketConnection("172.30.253.25", 1457)
        self.gamehost.newGamehost.connect(self.add_gamehost_card)

        self.gamehost.start()

    def add_gamehost_card(self, gamehost: GamehostModel):
 
        self.dasboard.window.add_device(gamehost.get_device_widget())
        self.gamehosts.append(gamehost)