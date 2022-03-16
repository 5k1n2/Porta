from __future__ import annotations
from view import DashboardView

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.PortaMain import PortaMain

class Dasboard(object):
    def __init__(self, model:PortaMain) -> None:
        
        self.window = None
        self.model = model
        
    def get_window(self):
        
        self.window = DashboardView.DashboardView(self)
        return self.window