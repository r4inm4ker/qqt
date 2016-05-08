from collections import OrderedDict
from functools import partial
import maya.cmds as mc
import maya.mel as mm
from funqt import QtGui, QtCore
from funqt.widgets.maya.lib import convertMayaControl
from funqt.widgets.inputs import LComboBox, LFloatField
from funqt import VBoxLayout, HBoxLayout, qcreate
from collections import OrderedDict


class RampPoint(object):
    class InterpType(object):
        None_ = 0
        Linear = 1
        Smooth = 2
        Spline = 3

        @classmethod
        def asDict(cls):
            return OrderedDict((("None", cls.None_),
                                ("Linear", cls.Linear),
                                ("Smooth", cls.Smooth),
                                ("Spline", cls.Spline)))

    def __init__(self, val, pos, interp):
        self.pos = float(pos)
        self.value = float(val)
        self.interp = int(interp)

    def asString(self):
        return ",".join([str(each) for each in self.value, self.pos, self.interp])


class RampWidget(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(RampWidget, self).__init__(*args, **kwargs)
        self._rampPoints = (RampPoint(1, 0, RampPoint.InterpType.Smooth), RampPoint(0, 1, RampPoint.InterpType.Smooth))
        self._initUI()
        self._connectSignals()
        self._initDefault()

    def _initDefault(self):
        self.setValue(self._rampPoints, asString=False)

    def _initMayaGradientCtrl(self):
        mc.window()
        mc.columnLayout()
        rampCtrl = mc.gradientControlNoAttr(h=90, changeCommand=self.rampWidgetEditedCallback)
        self.rampWidget = convertMayaControl(rampCtrl)
        self.rampCtrlName = rampCtrl

    def _initUI(self):
        self.layout = VBoxLayout(self)

        self._initMayaGradientCtrl()
        self.layout.addWidget(self.rampWidget)

        with self.layout:
            hori = qcreate(HBoxLayout)
            with hori:
                self.interpCB = qcreate(LComboBox, label="interpolation")
                for name, idx in RampPoint.InterpType.asDict().iteritems():
                    self.interpCB.addItem(name, data=idx)

                self.posField = qcreate(LFloatField, label="pos")
                self.valueField = qcreate(LFloatField, label="val")

    def _connectSignals(self):
        self.interpCB.valueEdited.connect(partial(self.updateCurrentRampPoint, "interp"))
        self.valueField.editingFinished.connect(partial(self.updateCurrentRampPoint, "value"))
        self.posField.editingFinished.connect(partial(self.updateCurrentRampPoint, "pos"))

    def rampWidgetEditedCallback(self, valueStr):
        self._rampPoints = self.asRampPoints(valueStr)
        self.updateFields()

    def updateFields(self):
        self.updateInterpField()
        self.updateValueField()
        self.updatePosField()

    def updateInterpField(self):
        interp = mc.gradientControlNoAttr(self.rampCtrlName, q=1, currentKeyInterpValue=1)
        self.interpCB.setCurrentIndex(interp)

    def updateValueField(self):
        currValue = round(mc.gradientControlNoAttr(self.rampCtrlName, q=1, currentKeyCurveValue=1), 4)
        self.valueField.setValue(currValue)

    def updatePosField(self):
        currKey = mc.gradientControlNoAttr(self.rampCtrlName, q=1, currentKey=1)
        pos = self._rampPoints[currKey].pos
        self.posField.setValue(pos)

    def updateCurrentRampPoint(self, mode):
        key = mc.gradientControlNoAttr(self.rampCtrlName, q=1, currentKey=1)
        if mode == "value":
            self._rampPoints[key].value = self.valueField.getValue()
        elif mode == "pos":
            self._rampPoints[key].pos = self.posField.getValue()
        elif mode == "interp":
            self._rampPoints[key].interp = self.interpCB.getData()

        self.setValue(self._rampPoints, asString=False)

    def setValue(self, rampPoints, asString=True):
        if asString:
            strVals = rampPoints
            rampPoints = self.asRampPoints(strVals)
        else:
            strVals = ",".join([each.asString() for each in rampPoints])

        mc.gradientControlNoAttr(self.rampCtrlName, e=1, asString=strVals)
        self._rampPoints = rampPoints

    def getValue(self, asString=True):
        if asString:
            return ",".join([each.asString() for each in self._rampPoints])
        else:
            return self._rampPoints

    @classmethod
    def asRampPoints(cls, strVal):
        return [RampPoint(*each) for each in cls.slice(strVal.split(','))]

    @staticmethod
    def slice(chunks, n=3):
        """Yield successive n-sized chunks from l."""
        for i in xrange(0, len(chunks), n):
            yield chunks[i:i + n]

    @classmethod
    def launch(cls):
        ui = cls()
        ui.show()
        return ui
