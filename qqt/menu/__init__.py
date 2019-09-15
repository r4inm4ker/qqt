from functools import partial
from .. import QtCore, QtGui, QtWidgets

def setContextMenu(widget, menu):
    widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    func = partial(summonMenu,widget,menu)
    widget.customContextMenuRequested.connect(func)

def summonMenu(widget, menu, pos):
    try:
        menu.exec_(widget.viewport().mapToGlobal(pos))
    except AttributeError:
        menu.exec_(widget.mapToGlobal(pos))

class ContextMenu(QtWidgets.QMenu):
    def __init__(self,parent):
        super(ContextMenu, self).__init__()
        self._parent = parent
        setContextMenu(parent, self)

    def addCommand(self,label,func, icon=None):
        action = QtWidgets.QAction(self._parent)
        action.setText(label)

        if icon:
            if isinstance(icon, str):
                icon = QtGui.QIcon(icon)
            action.setIcon(icon)

        if func:
            action.triggered.connect(func)
        self.addAction(action)
