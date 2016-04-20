from functools import  partial
from PySide import QtGui, QtCore
from PySide.QtCore import Qt


class BaseInput(QtCore.QObject):
    valueEdited = QtCore.Signal(str)

    def emitFieldChanged(self, value):
        self.valueEdited.emit(value)

class ComboBoxGrp(QtGui.QWidget, BaseInput):
    def __init__(self, label="",width=None, parent=None):
        super(ComboBoxGrp, self).__init__(parent=parent)
        self._label = label
        self._width = width
        self._initUI()
        self._connectSignals()

    def _initUI(self):
        layout = QtGui.QHBoxLayout()
        self.setLayout(layout)

        label = QtGui.QLabel(self._label)
        layout.addWidget(label)

        self.comboBox = ComboBox()
        layout.addWidget(self.comboBox)

        if self._width:
            self.comboBox.setMinimumWidth(self._width)

    def _connectSignals(self):
        self.comboBox.valueEdited.connect(self.emitFieldChanged)

    def __getattr__(self, item):
        return getattr(self.comboBox,item)

class ComboBox(QtGui.QComboBox, BaseInput):
    def __init__(self, parent=None):
        super(ComboBox, self).__init__(parent)
        self._setupSignal()

    def _setupSignal(self):
        self.currentIndexChanged.connect(self.emitFieldChanged)

    def setItems(self, items):
        while self.count() > 0:
            for idx in range(self.count()):
                self.removeItem(idx)
        self.insertItems(0, items)

    def addItem(self, item):
        super(ComboBox, self).addItem(str(item))
        idx = self.count()
        self.setItemData(idx-1,item)


    def getValue(self):
        return self.currentText()

    def setValue(self, value):
        idx = self.findText(value)
        if idx >= 0:
            self.setCurrentIndex(idx)


class LabelField(QtGui.QWidget):
    def __init__(self, label = None,*args, **kwargs):
        super(LabelField, self).__init__(*args, **kwargs)
        self.layout=QtGui.QHBoxLayout()
        self.setLayout(self.layout)

        label = label or ""
        self._label = QtGui.QLabel(label)
        self.layout.addWidget(self._label)

        self._field = QtGui.QLineEdit()
        self.layout.addWidget(self._field)

    @property
    def field(self):
        return self._field

    def __getattr__(self, item):
        return getattr(self._field,item)

class StringField(LabelField, BaseInput):
    def getValue(self):
        return self.field.text()

    def setValue(self, val):
        self.field.setText(val)


class NumericField(LabelField, BaseInput):
    def __init__(self,label=None,min=None,max=None,*args,**kwargs):
        super(NumericField, self).__init__(label=label,*args,**kwargs)
        self._validator = None

        if min is not None:
            self.min=min
            self.validator.setBottom(min)
            self.field.setText(str(min))
        else:
            self.field.setText("0")

        if max is not None:
            self.max=max
            self.validator.setTop(max)

        self.field.setValidator(self.validator)


    @property
    def validator(self):
        raise NotImplemented("must implement validator")

    def getValue(self):
        text = self.field.text()

        try:
            return int(text)
        except ValueError:
            raise ValueError("input type is not a numeric value.")

    def setValue(self, value):
        if value is None:
            value = 0
        try:
            int(value)
        except (ValueError, TypeError):
            raise ValueError("input type is not a numeric value.")
        else:
            self.field.setText(str(value))
            self.valueEdited.emit(value)


class FloatField(NumericField):
    @property
    def validator(self):
        if not self._validator:
            self._validator = QtGui.QDoubleValidator()
        return self._validator

    def getValue(self):
        text = self.field.text()
        try:
            return float(text)
        except ValueError:
            raise ValueError("input type is not a numeric value.")

class IntField(NumericField):
    @property
    def validator(self):
        if not self._validator:
            self._validator = QtGui.QIntValidator()
        return self._validator



class FloatSliderField(QtGui.QWidget, BaseInput):

    valueEdited = QtCore.Signal(float)
    def __init__(self, label="", parent=None, minVal =0.0, maxVal=1.0):
        super(FloatSliderField, self).__init__(parent)
        self.MIN_VAL = minVal
        self.MAX_VAL = maxVal
        self.MIN_INT = int(minVal * 100)
        self.MAX_INT = int(maxVal * 100)

        self.layout = QtGui.QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        self.field = FloatField(label=label)
        self.field.setMaximumWidth(50)

        self.layout.addWidget(self.field)

        self.minBtn = QtGui.QPushButton()
        self.minBtn.setFixedWidth(8)
        self.minBtn.setFixedHeight(8)
        self.layout.addWidget(self.minBtn)

        self.slider = FloatSlider()
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setMinimum(self.MIN_INT)
        self.slider.setMaximum(self.MAX_INT)
        self.slider.setContentsMargins(0,0,0,0)
        self.layout.addWidget(self.slider)

        self.maxBtn = QtGui.QPushButton()
        self.maxBtn.setFixedWidth(8)
        self.maxBtn.setFixedHeight(8)
        self.layout.addWidget(self.maxBtn)

        self.initSignal()
        self.updateField()

    def initSignal(self):
        self.slider.sliderPressed.connect(self.updateField)
        self.slider.sliderMoved.connect(self.updateField)
        self.field.textChanged.connect(self.fieldUpdated)
        self.minBtn.clicked.connect(partial(self.updateField,self.MIN_INT))
        self.maxBtn.clicked.connect(partial(self.updateField,self.MAX_INT))

    def updateField(self,val=None):
        if val is not None:
            self.slider.setValue(val)
        val = val or self.slider.value()
        val = 1.0 * val / (self.MAX_INT - self.MIN_INT)
        self.field.setText(str(val))
        self.valueEdited.emit(val)

    def getValue(self):
        text = self.field.text()
        retVal = 0
        try:
            retVal = float(text)
        except ValueError:
            pass
        return retVal

    def setValue(self, value):
        try:
            float(value)
        except (ValueError, TypeError):
            value = 0
        finally:
            self.field.setText(str(value))

    def fieldUpdated(self, val):
        self.valueEdited.emit(float(val))


class FloatSlider(QtGui.QSlider):
    editStarted = QtCore.Signal()
    editEnded = QtCore.Signal()

    def __init__(self,*args,**kwargs):
        super(FloatSlider, self).__init__(*args, **kwargs)


    def mousePressEvent(self, event):
        QtGui.QSlider.mousePressEvent(self, event)
        self.editStarted.emit()

    def mouseReleaseEvent(self, event):
        QtGui.QSlider.mouseReleaseEvent(self, event)
        self.editEnded.emit()



class ColorInput(QtGui.QPushButton, BaseInput):
    valueEdited = QtCore.Signal(QtGui.QColor)
    defaultColor = QtGui.QColor(198, 128, 128)
    sizePol = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)

    def __init__(self, parent=None):
        super(ColorInput, self).__init__(parent)
        self._color = None
        self.setValue(self.defaultColor)
        self.setSizePolicy(self.sizePol)
        self.clicked.connect(self.summonColorDialog)

    def getValue(self):
        return self._color

    def setValue(self, color):
        self._color = color
        self.setStyleSheet("QPushButton {background-color: rgb(%d,%d,%d)}" % (color.red(), color.green(), color.blue()))

    def summonColorDialog(self):
        colorDialog = QtGui.QColorDialog()
        currColor = self.getValue()
        retColor = colorDialog.getColor(initial=currColor)

        if retColor.isValid():
            self.setValue(retColor)
            self.valueEdited.emit(retColor)


class Checkbox(QtGui.QCheckBox, BaseInput):
    def getValue(self):
        return self.isChecked()

    def setValue(self,val):
        self.setChecked(val)


class OptionGroup(QtGui.QWidget):
    def __init__(self, parent=None):
        super(OptionGroup, self).__init__(parent=parent)
        self._btnGrp = QtGui.QButtonGroup()



class RadioButtonGroup(OptionGroup):
    def __init__(self, parent=None):
        super(RadioButtonGroup, self).__init__(parent=parent)


    def addOption(self,label, data=None):
        rb = QtGui.QRadioButton(text=label)
        rb.data = None
        rb.label = label
        self._btnGrp.addButton(rb)

    def setCurrentByIndex(self,idx):
        pass

    def setCurrentByLabel(self, label):
        pass

    def getCurrentIndex(self):
        return self._btnGrp.checkedId()

    def getCurrentLabel(self):
        return self.currentWidget.label

    @property
    def currentWidget(self):
        return self._btnGrp.checkedButton()

    def getCurrentData(self):
        return self.currentWidget.data



class Button(QtGui.QPushButton):
    pass