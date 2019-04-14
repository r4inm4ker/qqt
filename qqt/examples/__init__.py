from .. import QtGui, qcreate
from ..gui import VBoxLayout
from ..lib import createToolBtn

def openFolder():
    pass

mainWidget = QtGui.QWidget()

layout = VBoxLayout(mainWidget)
with layout:
    menuBar = qcreate(QtGui.QMenuBar)
    menu = menuBar.addMenu("file")
    action = menu.addAction("open folder")
    action.triggered.connect(openFolder)


toolbar = qcreate(QtGui.QToolBar)

#===hide layout option
hideAction = createToolBtn("&Toggle hide", parent=toolbar,
                           slot = openFolder, shortcut="Ctrl+H", icon=":/open_folder.png",
                           toolTip="Toggle hide layout", checkable=False, )
