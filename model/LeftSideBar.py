from view.LeftSideBarView import LeftSideBarView 

class LeftSideBar(object):
    def __init__(self, content_widget) -> None:
        
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