from PySide6.QtWidgets import QWidget, QSlider, QLabel, QPushButton, QHBoxLayout
from PySide6.QtGui import QFont, Qt
from PySide6.QtCore import Signal, Slot

class BoolButton(QWidget):

    clickedButton = Signal(QWidget)

    def __init__(self, fancyName, name) -> None:
        super().__init__()

        self.value = None
        self.type = "bool"
        self.fancyName = fancyName
        self.name = name
        
        self.fireButton = QPushButton("Fire")
        self.fireButton.setMinimumHeight(30)
        
        secondFont = QFont("Serif", 12)
        self.fancyNamelbl = QLabel(fancyName)
        self.fancyNamelbl.setFont(secondFont)
        
        self.mainLayout = QHBoxLayout()        
        self.mainLayout.addWidget(self.fancyNamelbl)
        self.mainLayout.addWidget(self.fireButton)
        
        self.setLayout(self.mainLayout)

        self.fireButton.pressed.connect(self.clicked)
        self.fireButton.released.connect(self.released)

    def clicked(self):
        self.value = True
        self.clickedButton.emit(self)
        
    def released(self):
        self.value = False
        self.clickedButton.emit(self)


        
class FloatSlider(QWidget):

    valueChanged = Signal(QWidget)

    def __init__(self, fancyName, name) -> None:
        super().__init__()

        self.value = None
        self.type = "float"
        self.fancyName = fancyName
        self.name = name
        
        secondFont = QFont("Serif", 12)
                
        self.count = QLabel()
        self.count.setFont(secondFont)
        
        self.slider = QSlider()
        self.slider.setMinimumHeight(30)
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.valueChanged.connect(self.count.setNum)
        
        self.fancyNamelbl = QLabel(fancyName)
        self.fancyNamelbl.setFont(secondFont)
        
        self.mainLayout = QHBoxLayout()        
        self.mainLayout.addWidget(self.fancyNamelbl, 2)
        self.mainLayout.addWidget(self.slider, 5)
        self.mainLayout.addWidget(self.count, 1)
        
        self.count.setNum(self.slider.value())

        self.slider.sliderReleased.connect(self.get_value)        
        
        self.setLayout(self.mainLayout)

    def get_value(self):
        self.value = self.slider.value()
        self.valueChanged.emit(self)

    def set_value(self, text):
        self.slider.setValue(text)