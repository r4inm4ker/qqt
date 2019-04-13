from Qt import QtCore, QtGui, QtWidgets
from Qt.QtCore import QMetaObject
from Qt import QtCompat


glob_current_active_parent = None


def qcreate(uiClass, *args, **kwargs):
    from .widgets.base import LabelMixin

    global glob_current_active_parent
    layoutType = kwargs.pop("layoutType", None)
    parent = kwargs.pop("parent",None)

    if parent and issubclass(uiClass, QtWidgets.QLayout):
        newObject = uiClass(parent,*args,**kwargs)
    else:
        newObject = uiClass(*args,**kwargs)

        tmpObject = None
        if isinstance(newObject,LabelMixin):
            tmpObject = newObject
            if newObject.parentWidget:
                newObject = newObject.parentWidget

        if not isinstance(newObject, QtWidgets.QLayout):
            if layoutType:
                lay = layoutType()
                newObject.setLayout(lay)


        par = glob_current_active_parent
        if par:
            if isinstance(newObject, QtWidgets.QSpacerItem):
                par.addSpacerItem(newObject)
            elif isinstance(newObject, QtWidgets.QWidget):
                par.addWidget(newObject)
            elif isinstance(newObject, QtWidgets.QLayout):
                par.addLayout(newObject)

        if tmpObject:
            newObject = tmpObject

    return newObject