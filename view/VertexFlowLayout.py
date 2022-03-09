import sys
from PySide6 import QtCore, QtGui, QtWidgets
from math import floor


class VertexFlowLayout(QtWidgets.QLayout):
    def __init__(self, parent=None, margin=0, spacing=-1):
        super(VertexFlowLayout, self).__init__(parent)

        if parent is not None:
            self.setContentsMargins(margin, margin, margin, margin)

        self.setSpacing(spacing)
        self.margin = margin
        self.enableAddWidget = False
        self.addLastWidget = None
        
        # spaces between each item
        self.spaceX = 5
        self.spaceY = 5

        self.itemList = []

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        if(self.addLastWidget != None and self.addLastWidget != item.wid):
            self.itemList.insert(len(self.itemList) -1, item)
        else:
            self.itemList.append(item)
            
        self.update()

    def count(self):
        return len(self.itemList)

    def itemAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList[index]

        return None

    def takeAt(self, index):
        if index >= 0 and index < len(self.itemList):
            print("remove", index)
            return self.itemList.pop(index)

        return None

    def expandingDirections(self):
        return QtCore.Qt.Orientations(QtCore.Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self.doLayout(QtCore.QRect(0, 0, width, 0), True)
                    
        return height

    def setGeometry(self, rect):
        super(VertexFlowLayout, self).setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QtCore.QSize()

        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())

        size += QtCore.QSize(2 * self.margin, 2 * self.margin)
        return size
    
    def addAddWidget(self, addWidget):
        
        if(self.addLastWidget != None):
            self.removeAddWidget()
        self.addLastWidget = addWidget
        self.addWidget(self.addLastWidget)
        
    def removeAddWidget(self):
        
        if(self.addLastWidget):
            self.addLastWidget.deleteLater()
            self.addLastWidget = None
        
        self.update()

    def doLayout(self, rect, testOnly):
        x = rect.x()
        y = rect.y()
        lineHeight = 0
            
        
        if(len(self.itemList) > 0):
            self.maxcards = rect.right() / (self.itemList[0].sizeHint().width() + self.spaceX)
            if(self.maxcards<1):
                return
            self.maxcardsint = floor(self.maxcards)
            self.sizepercard = rect.right() / self.maxcardsint
            self.cardheight = self.itemList[0].sizeHint().height() + self.spaceY
            self.cardcount = len(self.itemList) // self.maxcardsint
            self.height = ((self.cardcount + 1) * self.cardheight + self.spaceY)

        else: 
            return 0
        
        count = 0
        for item in self.itemList:
            print(item)
            column = 0
            rowcount = 0
            if(count != 0):           
                column = count // self.maxcardsint
                rowcount = count % self.maxcardsint 
                

            rowcount = rowcount * self.sizepercard + self.spaceX    
            column = column * (self.spaceY + item.sizeHint().height()) + self.spaceY
            item.setGeometry(QtCore.QRect(QtCore.QPoint(rowcount, column), item.sizeHint()))
            count += 1        

        
        return self.height
            
            