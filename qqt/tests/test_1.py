import sys
from qqt import QtGui, QtCore, qcreate, QtWidgets
from qqt.gui import *

from qqt.resources.icon import IconManager

class WidgetTester(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(WidgetTester, self).__init__(parent=parent)
        self._initUI()
        self._connectSignals()

    def _initUI(self):
        self.layout = VBoxLayout(self)
        with self.layout:
            with qcreate(HBoxLayout):
                iconPath = IconManager.get_icon("github.png", type="path")
                self.iconBtn = qcreate(IconButton,icon=iconPath, label="test label", w=40,h=40)

                iconPath = IconManager.get_icon("share.png", type="path")
                self.iconBtn = qcreate(IconButton,icon=iconPath, label="this is a very long label", w=40,h=40)


            qcreate(StringField, label="string label here")

            with qcreate(HBoxLayout):
                qcreate(Checkbox,label="x")
                qcreate(Checkbox, label="y")

    def _connectSignals(self):
        self.iconBtn.clicked.connect(self.button_callback)


    def button_callback(self):
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    ui = WidgetTester()
    ui.show()
    sys.exit(app.exec_())
