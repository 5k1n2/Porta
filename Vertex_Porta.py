from PySide6.QtWidgets import QApplication
from model.PortaMain import PortaMain
import sys


class VertexEmulator(object):
    def __init__(self):
        
        app = QApplication(sys.argv)
        
        self.model = PortaMain()        
        

        app.exec_()
        sys.exit(0)

VertexEmulator()