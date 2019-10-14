from functools import wraps

from .base import QtCore, QtGui, QtWidgets, QMetaObject, QtCompat

# for python2 & 3 cross compatibility
try:
    basestring
except NameError:
    basestring = str

try:
    from shiboken import wrapInstance
except:
    from shiboken2 import wrapInstance


class classproperty(object):
    """http://stackoverflow.com/questions/5189699/how-can-i-make-a-class-property-in-python
    """

    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        return self.f(owner)

loadUi = QtCompat.loadUi


def pixmap(image, w=None, h=None, aspectRatioMode=QtCore.Qt.KeepAspectRatio):
    if isinstance(image, basestring):
        pic = QtGui.QPixmap(image)
    elif isinstance(image, QtGui.QPixmap):
        pic = image
    else:
        raise ValueError("image either need to be in filePath or pixmap")

    currW, currH = pic.width(), pic.height()

    if currW <= 0 or currH <= 0:
        return pic

    if w and not h:
        newW = w
        newH = float(w) / currW * currH

    elif h and not w:
        newH = h
        newW = float(h) / currH * currW

    elif w and h:
        if aspectRatioMode == QtCore.Qt.IgnoreAspectRatio:
            newW, newH = w, h
        else:
            if currW > currH:
                newH = 1.0 * w / currW * currH
                newW = w
            else:
                newW = 1.0 * h / currH * currW
                newH = h
    else:
        newW, newH = currW, currH

    return pic.scaled(newW, newH)


def createToolBtn(text, parent=None, slot=None, shortcut=None, icon=None,
                  toolTip=None, checkable=False, size=32):
    action = QtWidgets.QAction(text, parent)
    if icon is not None:
        pix = QtGui.QPixmap(icon)
        pix.scaled(size, size)
        action.setIcon(QtGui.QIcon(pix))
    if shortcut is not None:
        action.setShortcut(shortcut)
    if toolTip is not None:
        action.setToolTip(toolTip)
        action.setStatusTip(toolTip)
    if slot is not None:
        action.triggered.connect(slot)
    if checkable:
        action.setCheckable(True)

    if parent:
        parent.addAction(action)

    return action


def busyCursor(func):
    """put busy cursor while processing """

    @wraps(func)
    def _func(*args, **kwargs):
        try:
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            return func(*args, **kwargs)
        finally:
            QtWidgets.QApplication.restoreOverrideCursor()

    return _func
