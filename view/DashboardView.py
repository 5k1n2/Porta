from __future__ import annotations

from PySide6.QtWidgets import QWidget, QPushButton, QScrollArea
from PySide6.QtGui import Qt
from view.VertexFlowLayout import VertexFlowLayout
from view.DeviceWidget import DeviceWidget
from model.DeviceModel import DeviceModel

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Dashboard import Dasboard

class DashboardView(QScrollArea):
    def __init__(self, model:Dasboard) -> None:
        super().__init__()

        self.model = model
        self.device_area = VertexFlowLayout()
        self.device_area_widget = QWidget()
        self.device_area_widget.setLayout(self.device_area)



        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setWidget(self.device_area_widget)
        
        self.device_area.spaceX = 20
        self.device_area.spaceY = 20
        
        for device in self.model.model.devices:
            self.add_device(device.get_device_widget())
        
    def add_device(self, deviceCard):
        self.device_area.addWidget(deviceCard)
        print("add device")
        

