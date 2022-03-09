from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from view.VertexFlowLayout import VertexFlowLayout
from view.DeviceWidget import DeviceWidget
from model.DeviceModel import DeviceModel
class DashboardView(QWidget):
    def __init__(self) -> None:
        super().__init__()
        
        self.mainLayout = QHBoxLayout()
        self.setLayout(self.mainLayout)
        self.flowLayout = VertexFlowLayout()
        self.mainLayout.addLayout(self.flowLayout)
        
        device = DeviceModel()
        
        self.flowLayout.addWidget(device.get_device_widget())
        self.flowLayout.addWidget(device.get_device_widget())
        self.flowLayout.addWidget(device.get_device_widget())
        self.flowLayout.addWidget(device.get_device_widget())