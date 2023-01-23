from __future__ import annotations
import pydevd
from PySide6.QtCore import QThread
import socket
import threading
from model.GamehostModel import GamehostModel
from PySide6.QtCore import Signal
from model import GlobalLog


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.PortaMain import PortaMain

class SocketConnection(QThread):

    newGamehost = Signal(GamehostModel)

    def __init__(self, ip, port, parent) -> None:
        super().__init__()
        self.ip = ip
        self.port = port
        self.parent = parent
        self.parent.relayMsg.connect(self.send_msg)

    def run(self):
        threading.current_thread().name = "Gamehost"

        pydevd.settrace(suspend=False)
        GlobalLog.add_to_log("New Gamehost Created")

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # self.socket.settimeout(1)
            self.socket.connect((self.ip, int(51234)))
            # GlobalLog.add_to_log("Established connection from {} to {}".format(self.device.deviceInfo.fancyName, self.device.ip))
            

            self.device = GamehostModel()
            self.device.deviceInfo["name"] = "Gamehost"
            self.device.deviceInfo["fancyName"] = "Gamehost"
            self.device.deviceInfo["Description"] = "Unreal Engine TCP Server Connection"
            GlobalLog.add_to_log("New Gamehost Added")

            self.newGamehost.emit(self.device)

        except Exception as e:
            # GlobalLog.add_to_log("Can't establish connection from {} to {}".format(self.device.deviceInfo.fancyName, self.device.ip))
            print(e)
            return False

    def send_msg(self, msg):
        self.socket.sendall(msg)
