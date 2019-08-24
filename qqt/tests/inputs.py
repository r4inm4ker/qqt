import sys
from qqt import QtGui, QtCore, qcreate
from qqt.gui import *




class WidgetTester(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(WidgetTester, self).__init__(parent=parent)
        self._initUI()
        self._connectSignals()

    def _initUI(self):
        pass
        self.layout = VBoxLayout(self)
        with self.layout:
            self.cb = qcreate(ComboBox, label="combobox")
            items = ["linear", "smooth", "spline"]
            data = [0, 1, 2]
            self.cb.setItems(items, data)

            self.tcb = qcreate(ComboBox, label="tiggered combobox")
            items = ["linear", "smooth", "spline"]
            data = [0, 1, 2]
            self.tcb.setItems(items, data)

            self.color = qcreate(ColorInput)

            self.ccb = qcreate(Checkbox, label="hoho")

            self.iss = qcreate(FloatSliderField, label="float slider", minVal=-0.1, maxVal = 100.0)
            self.iss = qcreate(IntSliderField, label="int slider", minVal=-200, maxVal = 150)

            bg = qcreate(RadioButtonGroup, label="radio button grp")
            bg.addOption("here")
            bg.addOption("there")


            self.iss = qcreate(FloatSliderField, label="float slider", minVal=-0.1, maxVal = 100.0)

            self.rbg = qcreate(RadioButtonGroup)

            self.rbg.addOption("1")
            self.rbg.addOption("2")
            self.rbg.addOption("3")

            testList = qcreate(TextList)
            testList.view.setHeaderHidden(True)
            testList.addItem("aa")
            testList.addItem("bb")


    def _connectSignals(self):
        self.cb.valueEdited.connect(self.syncComboBox)
        self.rbg.valueEdited.connect(self.radioBtnGrpCallback)

    def syncComboBox(self):
        val = self.cb.getValue()
        self.tcb.setValue(val)

    def radioBtnGrpCallback(self):
        print self.rbg.getValue()

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