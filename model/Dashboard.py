from view import DashboardView

class Dasboard(object):
    def __init__(self) -> None:
        
        self.window = None
        
    def get_window(self):
        
        self.window = DashboardView.DashboardView()
        return self.window