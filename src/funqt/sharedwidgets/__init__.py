from PySide import QtGui, QtCore

class SeparatorLine(QtGui.QFrame):
    def __init__(self, mode):
        super(SeparatorLine, self).__init__()
        if mode == 'horizontal':
            self.setFrameShape(QtGui.QFrame.HLine)
        elif mode == 'vertical':
            self.setFrameShape(QtGui.QFrame.VLine)
        self.setFrameShadow(QtGui.QFrame.Sunken)
