from model import GlobalLog
import view.LogWidgetView

class LogWidget(object):
    def __init__(self) -> None:
        
        self.log = []
        self.window = None
        
        
        self.window = None
        
    def get_window(self):
        
        self.log = GlobalLog.log
        return view.LogWidgetView.LogWidgetView(self)
    
    
        
    