from __future__ import annotations
from PySide6.QtCore import QThread
import json
import socket, time
import struct
from model.DeviceModel import DeviceModel
from PySide6.QtCore import Signal
import json
import socket, time
import struct
from model import GlobalLog

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.PortaMain import PortaMain

class SocketReaderInstance(QThread):
    
    newDevice = Signal(DeviceModel)
    
    def __init__(self, conn: socket):
        
        super().__init__() 
        self.socket = conn
        self.device = DeviceModel()
        # self.model.add_device(self.device)
        self.newDevice.emit(self.device)
        self.device.set_connection_status(True)
        self.device.connected_Host, self.device.connected_Port = conn.getpeername()
    
    def run(self):  
        print("new device added")
        GlobalLog.add_to_log("New Device Added")
        datastring = b""
        finaldata = b""
        remaining = None

        i = 0
        while True:

            data = self.socket.recv(4)
            if data == b"":
                self.device.set_connection_status(False)
                break
            remaining = struct.unpack(">I", data)[0]
            while remaining >= 0:

                finaldata += self.socket.recv(min(remaining, 1024))
                remaining = remaining - 1024

            decoded = finaldata.decode("utf-8")

            tmp = json.loads(decoded)
            

            self.device.deviceInfo.update(tmp)
            device_name = self.device.deviceInfo["name"]
            print(self)
            print(device_name)
            print(tmp)
            finaldata = b""
            # text = data.decode()
            
            if(self.device.window is not None):
                self.device.window.update_card_labels()


            time.sleep(0.001)