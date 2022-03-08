from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton

class DashboardView(QWidget):
    def __init__(self) -> None:
        super().__init__()
        
        self.mainLayout = QHBoxLayout()
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(QPushButton("test"))