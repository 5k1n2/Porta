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
        
        self.main_Layout.addWidget(self.logList)
        
        self.main_Layout.setContentsMargins(0,0,0,0)
        

    def add_to_log_list(self, log):
        
        self.logList.appendPlainText(log)
        
    def deleteLater(self) -> None:
        super().deleteLater()
        self.model.LogEventHandler.log_unsubscribe(self.add_to_log_list)