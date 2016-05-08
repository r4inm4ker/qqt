from funqt import QtGui, QtCore
import sys
from funqt.widgets.inputs import *

from funqt import qcreate, HBoxLayout, VBoxLayout


class WidgetTester(QtGui.QWidget):
    def __init__(self, parent=None):
        super(WidgetTester, self).__init__(parent=parent)
        self._initUI()

    def _initUI(self):
        pass
        self.layout = VBoxLayout(self)
        with self.layout:
            self.cb = qcreate(ComboBox, label="combobox")
            items = ["linear", "smooth", "spline"]
            data = [0, 1, 2]
            self.cb.setItems(items, data)

            self.color = qcreate(ColorWidget)

            self.ccb = qcreate(Checkbox, label="hoho")

            self.iss = qcreate(FloatSlider, label="float slider", minVal=-1.0)



class ComboBoxTester(object):
    def __init__(self):
        self.ui = None

    def run(self):
        self.ui = ComboBox(label="haha", layout="vertical")
        self.ui.show()
        items = ["linear","smooth","spline"]
        data = [0,1,2]
        self.ui.setItems(items,data)

        self.ui.valueEdited.connect(self.callback)

        return self.ui

    def callback(self, idx):
        print idx


class StringFieldTester(object):
    def __init__(self):
        self.ui = None

    def run(self):
        self.ui = StringField(label="mylabel")
        self.ui.show()
        # items = ["linear","smooth","spline"]
        # data = [0,1,2]
        # self.ui.setItems(items,data)

        self.ui.valueEdited.connect(self.callback)

        return self.ui

    def callback(self, val=""):
        print "val:", val


class CheckBoxTester(object):
    def run(self):
        self.ui = Checkbox(label="mylabel")
        self.ui.show()
        # items = ["linear","smooth","spline"]
        # data = [0,1,2]
        # self.ui.setItems(items,data)

        self.ui.valueEdited.connect(self.callback)

        return self.ui

    def callback(self, val=""):
        print "val:", val


class ColorInputTester(object):
    def run(self):
        self.ui = ColorInput(label="mylabel")

        self.ui.valueEdited.connect(self.callback)

        return self.ui

    def callback(self, val=""):
        print "val:", val

if __name__ == '__main__':
    app = QtGui.QApplication([])
    ui = WidgetTester()
    ui.show()
    sys.exit(app.exec_())