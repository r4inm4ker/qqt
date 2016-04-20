from functools import  partial
from PySide import QtGui, QtCore
from PySide.QtCore import Qt

class Spacer(QtGui.QSpacerItem):
    def __init__(self,mode="horizontal"):
        args = [None,None,None,None]
        if mode == "horizontal":

            args[0] = 20
            args[1] = 10
            args[2] = QtGui.QSizePolicy.Expanding
            args[3] = QtGui.QSizePolicy.Minimum
        elif mode == "vertical":
            args[0] = 20
            args[1] = 10
            args[2] = QtGui.QSizePolicy.Minimum
            args[3] = QtGui.QSizePolicy.Expanding

        super(Spacer, self).__init__(*args)


class SeparatorLine(QtGui.QFrame):
    def __init__(self, mode="horizontal"):
        super(SeparatorLine, self).__init__()
        if mode == 'horizontal':
            self.setFrameShape(QtGui.QFrame.HLine)
        elif mode == 'vertical':
            self.setFrameShape(QtGui.QFrame.VLine)
        self.setFrameShadow(QtGui.QFrame.Sunken)