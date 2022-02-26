import model.GlobalLog
import view.LogWidgetView

class LogWidget(object):
    def __init__(self) -> None:
        
        self.log = []
        self.window = None
        model.GlobalLog.subscribe_to_log(self.update_log)
        model.GlobalLog.add_to_log("New Log Window added")
        
        self.window = self.get_window()
        
    def get_window(self):
        
        return view.LogWidgetView.LogWidgetView(self)
    
    def update_log(self, msg):
        self.log.append(msg)