from PySide6 import QtWidgets
from model import GlobalLog

class LogWidgetView(QtWidgets.QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model
        
        self.main_Layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_Layout)
        
        self.logList = QtWidgets.QPlainTextEdit()
        self.logList.setReadOnly(True)

        for log in self.model.log:
            self.logList.appendPlainText(log)
        
        self.main_Layout.addWidget(self.logList)
        
        self.main_Layout.setContentsMargins(0,0,0,0)
        
        GlobalLog.subscribe_to_log(self.add_to_log_list)
        

    def add_to_log_list(self, log):
        
        self.logList.appendPlainText(log)
        
    def deleteLater(self) -> None:
        super().deleteLater()
        GlobalLog.unsubscribe_to_log(self.add_to_log_list)