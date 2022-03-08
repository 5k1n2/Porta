from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton

class Tab(QWidget):
    
    def __init__(self, name) -> None:
        super().__init__()
        
        self.mainLayout = QHBoxLayout()
        self.setLayout(self.mainLayout)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0,0,0,0)       
        
        
        self.button = QPushButton(name)
        self.button.setMinimumHeight(40)
        
        self.mainLayout.addWidget(self.button)
        
        self.setStyleSheet("""
                        
                        QPushButton{
                            background-color: #64656e;
                        }

                            
                        QPushButton:hover{
                            background-color: #DADADA;
                        }
                        
                        QPushButton:pressed{
                            background-color: #333333;
                        }
                        
                        QPushButton:disabled{
                            background-color: #1d2126;
                        }
                            """)
        
    def setEnabledButton(self, bool):
        self.button.setEnabled(bool)
        