from PySide import QtGui, QtCore
import pymel.core as pm
import maya.OpenMaya as om

from funqt.sharedwidgets.inputs import FloatSlider, FloatField
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin as DockMixin


class MayaAttrInput(QtCore.QObject):
    '''
    def attrChangedCallback(self, msg, plug, otherplug, *clientData):
    '''
    def _init(self, attrNode):
        attrNode = pm.Attribute(attrNode)
        self._node = attrNode.node()
        self._attr =attrNode
        self._isCallback = False

        currSel = pm.ls(sl=1)
        pm.select(cl=1)

        sel =om.MSelectionList()
        sel.add(attrNode.node().name())
        obj =om.MObject()
        sel.getDependNode(0, obj)

        self._obj = obj

        if sel:
            pm.select(currSel,r=1)
        else:
            pm.select(cl=1)

        self._connectAttr()

    def _connectAttr(self):
        self._callbackId = om.MNodeMessage.addAttributeChangedCallback(self._obj, self.attrChangedCallback)

    def attrChangedCallback(self, msg, plug, otherplug, *clientData):
        pass

    def deleteEvent(self):
        if self._callbackId:
            om.MMessage.removeCallback(self._callbackId)
            self._callbackId = None




class FloatAttrField(FloatField, MayaAttrInput):
    def __init__(self, attr):
        super(FloatField, self).__init__()
        self._init(attr)
        self.editingFinished.connect(self.setAttrVal)

    def attrChangedCallback(self, *args, **kwargs):
        if not self._isCallback:
            self._isCallback = True
            self.setValue(self._attr.get())

        # if self._attr:
        #     currVal = self._attr.get()
        # self.setValue(currVal)

    def closeEvent(self, *args, **kwargs):
        self.deleteEvent()
        super(FloatAttrField, self).closeEvent(*args, **kwargs)

    def hideEvent(self, *args, **kwargs):
        self.deleteEvent()
        super(FloatAttrField, self).hideEvent(*args, **kwargs)

    def setAttrVal(self):
        val = self.getValue()
        print self._isCallback
        print "EHEHEHEHE"
        if not self._isCallback:
            self._attr.set(val)

    def setValue(self, value):
        super(FloatAttrField, self).setValue(value)

        if self._isCallback:
            self._isCallback = False


