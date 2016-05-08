from funqt import QtGui
import maya.OpenMayaUI as omui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from funqt.lib import wrapInstance


def convertMayaControl(ctlName):
    ptr = omui.MQtUtil.findControl(ctlName)
    attrWidget = wrapInstance(ptr, QtGui.QWidget)
    return attrWidget