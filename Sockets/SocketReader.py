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

    def accept(self, conn):
        
        self.device = DeviceModel()
        # self.model.add_device(self.device)
        self.newDevice.emit(self.device)
        
        GlobalLog.add_to_log("New Device Added")
        datastring = b""
        finaldata = b""
        remaining = None

        i = 0
        while True:

            data = conn.recv(4)
            remaining = struct.unpack(">I", data)[0]
            while remaining >= 0:

                finaldata += conn.recv(min(remaining, 1024))
                remaining = remaining - 1024

            decoded = finaldata.decode("utf-8")

            tmp = json.loads(decoded)
            print(tmp)
            finaldata = b""
            # text = data.decode()


            time.sleep(0.001)


    def run(self):
        
        self.active = True
        print(socket.gethostbyname(socket.gethostname()))
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.settimeout(1)
            GlobalLog.add_to_log("Socket Listener Started")

            s.listen(2)
            while self.active:
                try:
                    conn, addr = s.accept()

                    thread = threading.Thread(target=self.accept, args=([conn]))
                    thread.start()
                    
                except socket.timeout:
                    pass
                
            self.stop()
    def stop(self):
        self.active = False
