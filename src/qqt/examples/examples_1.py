import sys
from qqt import QtWidgets, QtCore, QtGui, qcreate
from qqt.gui import VBoxLayout, HBoxLayout, StringField, FloatField, SeparatorLine, FrameWidget, ContextMenu


class Widget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(Widget, self).__init__(*args, **kwargs)

        self.setWindowTitle("qqt example 1")

        layout = VBoxLayout(self)
        with layout:
            label = qcreate(QtWidgets.QLabel, "Title")
            label.setAlignment(QtCore.Qt.AlignHCenter)
            qcreate(SeparatorLine)
            with qcreate(HBoxLayout):
                self.stringInput = qcreate(StringField, label="string input")
                self.floatInput = qcreate(FloatField, label="float input")
            qcreate(SeparatorLine)
            self.runBtn = qcreate(QtWidgets.QPushButton, "run")
            self.runBtn.clicked.connect(self.runCallback)
            qcreate(SeparatorLine)
            frameWidget = qcreate(FrameWidget, title="Output")
            with frameWidget.contentLayout:
                self.outputField = qcreate(QtWidgets.QTextEdit)
                contextMenu = ContextMenu(self.outputField)
                contextMenu.addCommand("clear", self.clearOutputField)

    def runCallback(self):
        stringValue = self.stringInput.getValue()
        floatValue = self.floatInput.getValue()

        outputStr = "string: {0}. float: {1}".format(stringValue, floatValue)
        self.outputField.setText(outputStr)

    def clearOutputField(self):
        self.outputField.clear()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    ui = Widget()
    ui.show()
    sys.exit(app.exec_())
