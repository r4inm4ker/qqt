from qqt import QtCore, QtGui, QtWidgets
from qqt.gui import qcreate, HBoxLayout, VBoxLayout, Button
import sys



class MainWidget(QtWidgets.QListWidget):
    def __init__(self,*args,**kwargs):
        super(MainWidget, self).__init__(*args, **kwargs)
        self._initUI()
        self._connectSignals()

    def _initUI(self):
        layout = VBoxLayout(self)
        with layout:
            self.printBtn = qcreate(Button,"print")
            self.errorBtn = qcreate(Button, "error")
            self.log = qcreate(OutputWidget)

    def _connectSignals(self):
        self.printBtn.clicked.connect(self.printCallback)
        self.errorBtn.clicked.connect(self.errorCallback)

    def printCallback(self):
        import maya.cmds as mc
        mc.warning('eee')
        print("ZZZZ")
        print("PRINTING STDOUT")

    def errorCallback(self):
        int("eer")


class EmittingStream(QtCore.QObject):
    textWritten = QtCore.Signal(str)

    def write(self, text):
        self.textWritten.emit(text)


class OutputWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(OutputWidget, self).__init__(parent=parent)

        self.ori_stdout = sys.__stdout__
        self.ori_stderr = sys.__stderr__

        print(self.ori_stdout)
        print(self.ori_stderr)

        # Install the custom output stream
        sys.stdout = EmittingStream()
        sys.stdout.textWritten.connect(self.normalOutputWritten)
        sys.stderr = EmittingStream()
        sys.stderr.textWritten.connect(self.normalOutputWritten)
        # self.rout = sys.stdout

        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.textEdit = QtWidgets.QTextEdit()
        self.textEdit.setMinimumHeight(120)
        layout.addWidget(self.textEdit)


    def __del__(self):
        # Restore sys.stdout & stderr
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def normalOutputWritten(self, text):
        self.ori_stdout.write(text)
        self.ori_stderr.write(text)

        """Append text to the QTextEdit."""
        # Maybe QTextEdit.append() works as well, but this is how I do it:
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textEdit.setTextCursor(cursor)
        self.textEdit.ensureCursorVisible()

