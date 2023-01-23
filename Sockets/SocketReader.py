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
    
    sendMsg = Signal(bytearray)
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
                    
                    self.thread = SocketReaderInstance(conn, self.model)
                    self.thread.newDevice.connect(self.newDeviceEmit)
                    self.thread.sendMsg.connect(self.sendMsgEmit)
                    
                    
                    self.thread.start()
                    self.threads.append(self.thread)
                    
                except socket.timeout:
                    pass
                
            self.stop()
            
    def newDeviceEmit(self, x):
        self.newDevice.emit(x)

    def sendMsgEmit(self, x):
        self.sendMsg.emit(x)
     
    
    def stop(self):
        self.active = False
        


class SocketReaderInstance(QThread):
    
    newDevice = Signal(DeviceModel)
    sendMsg = Signal(bytearray)
    
    def __init__(self, conn: socket, model):
        
        super().__init__() 
        self.model = model
        self.socket = conn
    
    def run(self):  
        import pydevd;pydevd.settrace(suspend=False)
        
        
        print("Start of socket")
        

        datastring = b""
        finaldata = b""
        remaining = None

        i = 0
        while True:
            # recieve length of config byte array
            expected = self.read_expected_length()
            
            # read data from socket
            finaldata = self.read_from_socket(expected)

            decoded = finaldata.decode("utf-8")

            try:
                tmp = json.loads(decoded)
            except json.decoder.JSONDecodeError as e:
                GlobalLog.add_to_log(f"ERROR: JSON config not valid: {decoded}, {e.msg}")
                break
            
            
            if(tmp["kind"] == 0):
                
                
                self.device = DeviceModel()
                # self.model.add_device(self.device)
                self.device.set_connection_status(True)
                self.device.connected_Host, self.device.connected_Port = self.socket.getsockname()
        

                self.device.update_log(tmp)
                self.device.deviceInfo.update_dict(tmp)
                device_name = self.device.deviceInfo["name"]
                
                self.newDevice.emit(self.device)
                print("new device added")
                GlobalLog.add_to_log(f"New Device Added: {device_name}")
                
                if(self.device.window is not None):
                    self.device.window.update_card_labels()
                    
                while(True):
                    # recieve length of config byte array
                    expected = self.read_expected_length()
                    if expected == 0:
                        break
                    # read data from socket
                    finaldata = self.read_from_socket(expected)
                    print(finaldata)
                    self.device.add_to_log(finaldata.decode())
                    self.sendMsg.emit(finaldata)
                    
                
            elif(tmp["kind"] == 1):
                
                self.device = GamehostModel()
                print("gamehost added")
                GlobalLog.add_to_log("New Gamehost Added")

                self.device.deviceInfo.update_dict(tmp)
                self.newDevice.emit(self.device)
                
            else:
                GlobalLog(f"Kind of Device not found for Device: {self.socket.gethostbyname(self.socket.gethostname())}")
                

            finaldata = b""
            # text = data.decode()
            


            time.sleep(0.001)
            
    def read_expected_length(self):
        
        # recieve length of config byte array
        data:bytes
        try:
            data = self.socket.recv(4)
        except:
            GlobalLog.add_to_log(f"New Device Config Length recieved not expected input for Device: {self.socket.getsockname()}")
            return 0
        if data == b"":
            self.device.set_connection_status(False)
            return 0
        expected = int.from_bytes(data, "little")
        if(expected < 1):
            GlobalLog.add_to_log(f"New Device Config Length is lower than expected (< 1) for Device: {self.socket.getsockname()}")
            
        return expected
    
    def read_from_socket(self, expected, warning_length = 10, finaldata = b""):
        

            reamining = expected
            
            try:
                # read socket data               
                
                while reamining > 0:

                    finaldata += self.socket.recv(min(reamining, 1024))
                    reamining -= 1024
                
                # check if all expected data was recieved. If not continue reading. Usually requiered for very slow clients
                length = len(finaldata)
                if (len(finaldata) < expected):
                    warning_length =- 1
                    if(warning_length == 0):
                        GlobalLog.add_to_log(f"Unusual many attempts to recieve full Data of Socket for Device: {self.socket.getsockname()}")
                    finaldata = self.read_from_socket(expected - len(finaldata), warning_length=warning_length, finaldata=finaldata)
            except Exception as e:
                GlobalLog.add_to_log(f"Socket returned an Error for Device: {self.socket.getsockname()}, {e}")
                
            
            return finaldata
            
    def sendUpdate(self, update_msg):
        
        message = """{"name" : "deviceWeapon","inputs" :{"input1" :{"name" : "trigger1","fancyName" : "Trigger","description" : "Das ist der Trigger der Waffe","value" : "float","default" : 0,"hidden" : false}}}"""
        
        
        length = len(message).to_bytes(4, "little")

        self.socket.sendall(length + message.encode("utf-8"))