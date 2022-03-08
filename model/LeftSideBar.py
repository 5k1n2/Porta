from __future__ import annotations

from view.LeftSideBarView import LeftSideBarView 

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.PortaMain import PortaMain
    

class LeftSideBar(object):
    def __init__(self, content_widget, model: PortaMain) -> None:
        
        self.model = model
        self.buttons = []
        self.content_widget = content_widget
        self.left_side_bar = self.get_window()    
        
        
        
    def get_window(self):
        return LeftSideBarView(self, self)
    
    def add_new_button(self, name, widget):
        
        new_btn = Button(name, widget)
        self.buttons.append(new_btn)
        self.left_side_bar.add_button(new_btn)
        
        
class Button(object):
    def __init__(self, name, widget) -> None:
        
        self.name = name
        self.widget = widget
        self.tab = None