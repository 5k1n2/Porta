from PySide6 import QtWidgets


class PortaMainView(QtWidgets.QWidget):
    
    def __init__(self) -> None:
        super().__init__()
        
        self.set_stylesheet()
        self.setWindowTitle("Vertex Porta")
        self.resize(1300, 800)
        
        self.horizontal_main_layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.horizontal_main_layout)
        
        self.window_layout = QtWidgets.QVBoxLayout()
        self.horizontal_main_layout.addLayout(self.window_layout)
        
        self.content_widget = QtWidgets.QWidget()
        self.horizontal_main_layout.addWidget(self.content_widget)

            
    def set_stylesheet(self):
        with open("view/stylesheet.qss", "r") as k:
            self.setStyleSheet(k.read())
            
            