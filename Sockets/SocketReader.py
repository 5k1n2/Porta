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
import threading
from model import GlobalLog
from model.DeviceInfo import DeviceInfo
from model.GamehostModel import GamehostModel

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.PortaMain import PortaMain


class SocketReader(QThread):
    
    newDevice = Signal(DeviceModel)
    
    def __init__(self, model: PortaMain) -> None:
        super().__init__() 
        
        self.model = model
        self.host = ""
        self.port = 1456
        self.active = False
        self.threads = []
        self.isGamehost = False

    


    def run(self):
        import pydevd;pydevd.settrace(suspend=False)
        self.active = True
        print("run")
        print(socket.gethostbyname(socket.gethostname()))
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.settimeout(1)
            GlobalLog.add_to_log("Socket Listener Started")

            s.listen(2)
            while self.active:
                try:
                    conn, addr = s.accept()

                    # thread = threading.Thread(target=self.accept, args=([conn]))
                    # thread.start()
                    
                    self.thread = SocketReaderInstance(conn)
                    self.thread.newDevice.connect(self.newDeviceEmit)
                    
                    
                    self.thread.start()
                    self.threads.append(self.thread)
                    
                except socket.timeout:
                    pass
                
            self.stop()
            
    def newDeviceEmit(self, x):
        self.newDevice.emit(x)
     
    
    def stop(self):
        self.active = False
        



class SocketReaderInstance(QThread):
    
    newDevice = Signal(DeviceModel)
    
    def __init__(self, conn: socket):
        
        super().__init__() 
        self.socket = conn
    
    def run(self):  
        import pydevd;pydevd.settrace(suspend=False)
        
        
        print("emit")
        

        datastring = b""
        finaldata = b""
        remaining = None

        i = 0
        while True:
            data:bytes
            data = self.socket.recv(4)
            if data == b"":
                self.device.set_connection_status(False)
                break
            remaining = int.from_bytes(data, "little")
            while remaining >= 0:

                finaldata += self.socket.recv(min(remaining, 1024))
                remaining = remaining - 1024

            decoded = finaldata.decode("utf-8")

            tmp = json.loads(decoded)
            
            if(tmp["kind"] == 0):
                
                
                self.device = DeviceModel()
                # self.model.add_device(self.device)
                self.device.set_connection_status(True)
                self.device.connected_Host, self.device.connected_Port = self.socket.getsockname()
            
                self.newDevice.emit(self.device)
                print("new device added")
                GlobalLog.add_to_log("New Device Added")

                self.device.update_log(tmp)
                self.device.deviceInfo.update_dict(tmp)
                device_name = self.device.deviceInfo["name"]
                
                if(self.device.window is not None):
                    self.device.window.update_card_labels()
                
            elif(tmp["kind"] == 1):
                
                self.device = GamehostModel()
                print("gamehost added")
                GlobalLog.add_to_log("New Gamehost Added")

                self.device.deviceInfo.update_dict(tmp)
                self.newDevice.emit(self.device)
                
                

            finaldata = b""
            # text = data.decode()
            


            time.sleep(0.001)
            
    def sendUpdate(self, update_msg):
        
        message = """{"name" : "deviceWeapon","inputs" :{"input1" :{"name" : "trigger1","fancyName" : "Trigger","description" : "Das ist der Trigger der Waffe","value" : "float","default" : 0,"hidden" : false}}}"""
        
        
        length = len(message).to_bytes(4, "little")

        self.socket.sendall(length + message.encode("utf-8"))