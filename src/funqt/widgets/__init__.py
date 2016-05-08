from funqt import QtGui, QtCore, HBoxLayout, VBoxLayout

class GenericWidget(QtGui.QWidget):
    @classmethod
    def launch(cls,*args,**kwargs):
        ui = cls()
        ui.show()
        return ui