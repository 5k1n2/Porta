from __future__ import annotations

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PySide6.QtGui import Qt
from view.DebugElements import FloatSlider, BoolButton

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Overview import Overview

class OverviewView(QWidget):


    def __init__(self, model:Overview) -> None:
        super().__init__()

        self.model = model
        self.device_model = model.device_model
        self.elements = {}

        self.device_model.updateElement.connect(self.update_element)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Stylesheet
        with open("view/stylesheet.qss", "r") as k:
            self.setStyleSheet(k.read())

        # Signal Layout

        self.signal_layout = QVBoxLayout()

        self.main_layout.addLayout(self.signal_layout)

        # Buttonrow        
        self.buttonRow = QHBoxLayout()
        
        self.cancelButton = QPushButton("Close")
        self.cancelButton.setFixedSize(150, 40)
        self.cancelButton.clicked.connect(self.close_window)

        self.buttonRow.addWidget(self.cancelButton)
        self.buttonRow.setAlignment(Qt.AlignRight)
                
        self.main_layout.addLayout(self.buttonRow)

        self.resize(self.sizeHint().width() *4, self.sizeHint().height() *2)

        
        # self.device.add_to_log("Log opened")
        
        self.build_inputs()

        self.init_elements()

        self.show()

    def close_window(self):
        self.close()

    def init_elements(self):
        for element in self.elements:
            for input in self.model.device_inputs:
                if(self.model.device_inputs[input]["name"] == element):
                    
                    if("currentvalue" in self.model.device_inputs[input]):
                        last_value = self.model.device_inputs[input]["currentvalue"]

                        self.elements[element].set_value(last_value)

                    break
            



    def update_element(self, sender):
        print(sender)
        
        for element in sender["inputs"]:
            single_element = sender["inputs"][element]
            control_element = self.elements[sender["inputs"][element]["name"]]
            control_element.set_value(single_element["currentvalue"])

    def build_inputs(self):
        
        for input in self.model.device_inputs:
            inputFancyName = self.model.device_inputs[input]["fancyName"]
            debugType = self.model.device_inputs[input]["value"]
            name = self.model.device_inputs[input]["name"]

            
            if(debugType == "float"):
                element = FloatSlider(inputFancyName, name)
                self.signal_layout.addWidget(element)

                # slider.valueChanged.connect(self.update_signal)


            
            elif(debugType == "bool"):
                element = BoolButton(inputFancyName, name)
                self.signal_layout.addWidget(element)
                
                
            self.elements[name] = element

                # button.clickedButton.connect(self.update_signal)