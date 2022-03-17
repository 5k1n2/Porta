from __future__ import annotations

from view.OverviewView import OverviewView
from PySide6.QtCore import QObject, Signal

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.DeviceModel import DeviceModel


class Overview(QObject):


    def __init__(self, device_model:DeviceModel) -> None:
        
        self.device_model = device_model
        self.window = None

        self.device_inputs = self.device_model.deviceInfo["inputs"]


        for input in self.device_inputs:
            print(self.device_inputs[input])


    def get_window(self):

        self.window = OverviewView(self)
        return self.window

        