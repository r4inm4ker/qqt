from funqt import QtGui, QtCore

glob_current_active_parent = None
glob_previous_active_parent = None

def createUI(uiClass, *args, **kwargs):
    layoutType = kwargs.pop("layoutType", None)
    newObject = uiClass(*args,**kwargs)

    if not isinstance(newObject, QtGui.QLayout):
        if layoutType:
            lay = layoutType()
            newObject.setLayout(lay)
            newObject.layout = lay

    global glob_current_active_parent
    par = glob_current_active_parent
    if par:
        if isinstance(newObject, QtGui.QSpacerItem):
            par.addSpacerItem(newObject)
        elif isinstance(newObject, QtGui.QWidget):
            par.addWidget(newObject)
        elif isinstance(newObject, QtGui.QLayout):
            par.addLayout(newObject)

    return newObject


class LayoutMixin(object):
    def __enter__(self):
        global glob_current_active_parent, glob_previous_active_parent
        glob_previous_active_parent, glob_current_active_parent = glob_current_active_parent, self

    def __exit__(self, exc_type, exc_val, exc_tb):
        global glob_current_active_parent, glob_previous_active_parent
        glob_current_active_parent = glob_previous_active_parent

class VBoxLayout(QtGui.QVBoxLayout, LayoutMixin):
    pass

class HBoxLayout(QtGui.QHBoxLayout, LayoutMixin):
    pass