from PySide6.QtWidgets import QWidget, QPushButton, QScrollArea
from PySide6.QtGui import Qt
from view.VertexFlowLayout import VertexFlowLayout
from view.DeviceWidget import DeviceWidget
from model.DeviceModel import DeviceModel

class DashboardView(QScrollArea):
    def __init__(self) -> None:
        super().__init__()

        
        self.device_area = VertexFlowLayout()
        self.device_area_widget = QWidget()
        self.device_area_widget.setLayout(self.device_area)

        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setWidget(self.device_area_widget)
        
        self.device_area.spaceX = 20
        self.device_area.spaceY = 20
        

        
    def add_device(self, deviceCard):
        self.device_area.addWidget(deviceCard)
        print("add device")

