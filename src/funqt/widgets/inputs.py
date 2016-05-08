from functools import partial
from funqt import QtGui, QtCore
from funqt import qcreate, VBoxLayout, HBoxLayout
from funqt.widgets import GenericWidget

Qt = QtCore.Qt


class InputMixin(QtCore.QObject):
    valueEdited = QtCore.Signal(unicode)

    def getValue(self):
        return None

    def setValue(self, value):
        pass

    def emitValueEdited(self, value=None):
        self.valueEdited.emit(value)


class LabelledInput(GenericWidget, InputMixin):
    def __init__(self, *args, **kwargs):
        layout = kwargs.pop("layout","horizontal")
        label = kwargs.pop("label","")
        parent = kwargs.pop("parent",None)

        super(LabelledInput, self).__init__(parent)

        if layout == "horizontal":
            self._layout = HBoxLayout(self)
        elif layout == "vertical":
            self._layout = VBoxLayout(self)

        with self._layout:
            label = label or ""

            if layout == "horizontal":
                self._label = qcreate(QtGui.QLabel,label)
                self._inputWidget = qcreate(self.inputClass,*args,**kwargs)
            elif layout == "vertical":
                self._inputWidget = qcreate(self.inputClass,*args,**kwargs)
                self._label = qcreate(QtGui.QLabel,label)
                self._label.setAlignment(Qt.AlignHCenter)
        #
        # for attr in (name for name in dir(self) if not name.startswith('_')):
        #     if hasattr(self._inputWidget,attr):
        #         iattr = getattr(self._inputWidget,attr)
        #         # setattr(self,attr,iattr)

        self._connectSignals()
        self._additionalSetup()

    @property
    def input(self):
        return self._inputWidget

    @property
    def inputClass(self):
        return QtGui.QLineEdit

    def __getattr__(self, item):
        return getattr(self.input, item)

    def _additionalSetup(self):
        pass

class ComboBox(LabelledInput):
    valueEdited = QtCore.Signal(int)
    @property
    def inputClass(self):
        return QtGui.QComboBox

    def __init__(self, *args, **kwargs):
        width = kwargs.pop("width",None)
        super(ComboBox, self).__init__(*args, **kwargs)

        if width:
            self.input.setMinimumWidth(width)

    def _connectSignals(self):
        self.input.currentIndexChanged.connect(self.emitValueEdited)

    def emitValueEdited(self,idx):
        self.valueEdited.emit(idx)

    def setItems(self, items, data=None):
        data = data or [None]*len(items)
        while self.input.count() > 0:
            for idx in range(self.input.count()):
                self.input.removeItem(idx)

        for item,dt in zip(items,data):
            self.input.addItem(item, data)

    def addItem(self, item, data=None):
        self.input.addItem(unicode(item))
        idx = self.count() - 1
        data = data if data is not None else item
        self.setItemData(idx, data)

    def getValue(self):
        return self.input.currentText()

    def getData(self, index=None):
        index = index or self.input.count() - 1
        return self.input.itemData(index)

    def setIndex(self, index):
        self.input.setCurrentIndex(index)
        self.valueEdited.emit(index)

    def setValue(self, value):
        idx = self.input.findText(value)
        if idx >= 0:
            self.input.setCurrentIndex(idx)
        else:
            raise ValueError("wrong or nonexistent value provided.")
        self.valueEdited.emit(idx)


class StringField(LabelledInput):
    valueEdited = QtCore.Signal(str)

    @property
    def inputClass(self):
        return QtGui.QLineEdit

    def _connectSignals(self):
        self.input.editingFinished.connect(self.emitValueEdited)

    def emitValueEdited(self, value=None):
        value = value or self.input.text()
        self.valueEdited.emit(value)

    def getValue(self):
        return unicode(self.input.text())

    def setValue(self, val):
        self.input.setText(val)


class NumericField(LabelledInput):
    def __init__(self,*args, **kwargs):
        minimum = kwargs.pop("minimum", None)
        maximum = kwargs.pop("maximum", None)

        super(NumericField, self).__init__(*args, **kwargs)
        self._validator = None

        if minimum is not None:
            self.min = minimum
            self.validator.setBottom(minimum)
            self.setValue(minimum)
        else:
            self.setValue(0)

        if maximum is not None:
            self.max = maximum
            self.validator.setTop(maximum)

        self.input.setValidator(self.validator)

    def _connectSignals(self):
        self.editingFinished.connect(self.emitEditingFinished)

    def emitEditingFinished(self):
        pass

    @property
    def validator(self):
        raise NotImplemented("must implement validator")

    def getValue(self):
        raise NotImplemented("must implement getValue")

    def setValue(self, value):
        raise NotImplemented("must implement setValue")


class IntField(NumericField):
    valueEdited = QtCore.Signal(int)

    def emitEditingFinished(self):
        val = int(self.input.text())
        self.valueEdited.emit(val)

    @property
    def validator(self):
        if not self._validator:
            self._validator = QtGui.QIntValidator()
        return self._validator

    def getValue(self):
        text = self.input.text()
        return int(text)

    def setValue(self, value):
        if value is None:
            value = 0
        try:
            int(value)
        except (ValueError, TypeError):
            raise ValueError("input type is not a numeric value.")
        else:
            self.input.setText(unicode(value))
            self.valueEdited.emit(value)


class FloatField(NumericField):
    valueEdited = QtCore.Signal(float)

    def emitEditingFinished(self):
        val = float(self.input.text())
        self.valueEdited.emit(val)

    @property
    def validator(self):
        if not self._validator:
            self._validator = QtGui.QDoubleValidator()
        return self._validator

    def getValue(self):
        text = self.input.text()
        return float(text)

    def setValue(self, value):
        if value is None:
            value = 0
        try:
            float(value)
        except (ValueError, TypeError):
            raise ValueError("input type is not a numeric value.")
        else:
            self.input.setText(unicode(value))
            self.valueEdited.emit(value)


class ColorInput(LabelledInput):
    valueEdited = QtCore.Signal(QtGui.QColor)

    @property
    def inputClass(self):
        return ColorWidget

    def _connectSignals(self):
        self.input.valueEdited.connect(self.emitValueEdited)


class ColorWidget(QtGui.QPushButton):
    valueEdited = QtCore.Signal(QtGui.QColor)
    defaultColor = QtGui.QColor(198, 128, 128)
    sizePol = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)

    def __init__(self, parent=None):
        super(ColorWidget, self).__init__(parent)
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


class Checkbox(LabelledInput):
    valueEdited = QtCore.Signal(bool)

    @property
    def inputClass(self):
        return QtGui.QCheckBox

    def _connectSignals(self):
        self.input.stateChanged.connect(self.emitValueEdited)

    def getValue(self):
        return self.input.isChecked()

    def setValue(self,val):
        self.input.setChecked(val)
#
# class IntSlider(LabelledInput):
#
#     @property
#     def inputClass(self):
#         return IntSliderField
#
#
# class IntSliderField(QtGui.QWidget):
#
#
# class IntSliderWidget(QtGui.QSlider):
#     editStarted = QtCore.Signal()
#     editEnded = QtCore.Signal()
#
#     def __init__(self,*args,**kwargs):
#         super(IntSliderWidget, self).__init__(*args, **kwargs)
#
#     def mousePressEvent(self, event):
#         QtGui.QSlider.mousePressEvent(self, event)
#         self.editStarted.emit()
#
#     def mouseReleaseEvent(self, event):
#         QtGui.QSlider.mouseReleaseEvent(self, event)
#         self.editEnded.emit()



class FloatSlider(LabelledInput):
    @property
    def inputClass(self):
        return FloatSliderField

    def _connectSignals(self):
        self.input.valueEdited.connect(self.emitValueEdited)


class FloatSliderField(QtGui.QWidget, InputMixin):

    valueEdited = QtCore.Signal(float)
    def __init__(self, parent=None, minVal =0.0, maxVal=1.0):
        super(FloatSliderField, self).__init__(parent)
        self.MIN_VAL = minVal
        self.MAX_VAL = maxVal
        self.MIN_INT = int(minVal * 100)
        self.MAX_INT = int(maxVal * 100)

        self.layout = QtGui.QHBoxLayout()
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        self.field = FloatField()
        self.field.setMaximumWidth(100)

        self.layout.addWidget(self.field)

        self.minBtn = QtGui.QPushButton()
        self.minBtn.setFixedWidth(8)
        self.minBtn.setFixedHeight(8)
        self.layout.addWidget(self.minBtn)

        self.slider = Slider()
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setMinimum(self.MIN_INT)
        self.slider.setMaximum(self.MAX_INT)
        self.slider.setContentsMargins(0,0,0,0)
        self.layout.addWidget(self.slider)

        self.maxBtn = QtGui.QPushButton()
        self.maxBtn.setFixedWidth(8)
        self.maxBtn.setFixedHeight(8)
        self.layout.addWidget(self.maxBtn)

        self._connectSignals()
        self.updateField()

    def setMinimum(self, val):
        self.MIN_VAL = val
        self.MIN_INT = int(val * 100)
        self.slider.setMinimum(self.MIN_INT)

    def setMaximum(self, val):
        self.MAX_VAL = val
        self.MAX_INT = int(val * 100)
        self.slider.setMaximum(self.MAX_INT)

    def _connectSignals(self):
        self.slider.sliderPressed.connect(self.updateField)
        self.slider.sliderMoved.connect(self.updateField)
        self.field.textChanged.connect(self.fieldUpdated)
        self.minBtn.clicked.connect(partial(self.updateField,self.MIN_INT))
        self.maxBtn.clicked.connect(partial(self.updateField,self.MAX_INT))

    def updateField(self,val=None):
        if val is not None:
            self.slider.setValue(val)
        val = val or self.slider.value()

        newVal = (1.0*(val - self.MIN_INT) / (self.MAX_INT - self.MIN_INT)) * (self.MAX_VAL - self.MIN_VAL) + self.MIN_VAL

        self.field.setText(unicode(newVal))
        self.valueEdited.emit(newVal)

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


class Slider(QtGui.QSlider):
    editStarted = QtCore.Signal()
    editEnded = QtCore.Signal()

    def __init__(self,*args,**kwargs):
        super(Slider, self).__init__(*args, **kwargs)


    def mousePressEvent(self, event):
        QtGui.QSlider.mousePressEvent(self, event)
        self.editStarted.emit()

    def mouseReleaseEvent(self, event):
        QtGui.QSlider.mouseReleaseEvent(self, event)
        self.editEnded.emit()





# class RadioButtonGrp(LabelledInput):
#
#
#     def __init__(self, parent=None):
#         super(RadioButtonGrp, self).__init__(parent=parent)
#
#     def addOption(self,label, data=None):
#         rb = QtGui.QRadioButton(text=label)
#         rb.data = None
#         rb.label = label
#         self._btnGrp.addButton(rb)
#
#     def setCurrentByIndex(self,idx):
#         pass
#
#     def setCurrentByLabel(self, label):
#         pass
#
#     def getCurrentIndex(self):
#         return self._btnGrp.checkedId()
#
#     def getCurrentLabel(self):
#         return self.currentWidget.label
#
#     @property
#     def currentWidget(self):
#         return self._btnGrp.checkedButton()
#
#     def getCurrentData(self):
#         return self.currentWidget.data
#
#
# class RadioButtonGrpWidget()


class IconButton(LabelledInput):
    def __init__(self,*args,**kwargs):
        self._icon = kwargs.pop('icon',None)
        self._width = kwargs.pop('width',30)
        self._height = kwargs.pop('height',30)
        kwargs['layout'] = "vertical"
        super(IconButton, self).__init__(*args,**kwargs)

    @property
    def inputClass(self):
        return Button

    def _additionalSetup(self):
        w, h = self._width, self._height
        if w:
            self.input.setFixedWidth(w)

        if h:
            self.input.setFixedHeight(h)
        icon = QtGui.QIcon(self._icon)
        self.input.setIcon(icon)
        if w and h:
            self.input.setIconSize(QtCore.QSize(w,h))

        font = self._label.font()
        fm = QtGui.QFontMetrics(font)
        tw = fm.width(self._label.text())
        self._label.setFixedWidth(tw)


    def _connectSignals(self):
        pass


class OptionGroup(LabelledInput):
    valueEdited = QtCore.Signal(str)
    def __init__(self,parent=None):
        super(OptionGroup, self).__init__(parent)
        self._btnGrp = QtGui.QButtonGroup()
        self._btnGrp.setExclusive(True)
        self.layout = HBoxLayout(self)
        self._btnGrp.buttonClicked.connect(self.emitValueEdited)

    def emitValueEdited(self, value=None):
        self.valueEdited.emit(self.getCurrentLabel())

    def getCurrentLabel(self):
        return ""


class RadioButtonGroup(OptionGroup):
    def __init__(self, parent=None):
        super(RadioButtonGroup, self).__init__(parent)

    def addButton(self, label, data=None):
        rb = QtGui.QRadioButton(text=label)
        rb.data = data
        rb.label = label
        self._btnGrp.addButton(rb)
        self.layout.addWidget(rb)

    def setCurrentByIndex(self,idx):
        if self._btnGrp.buttons():
            self._btnGrp.buttons()[idx].setChecked(True)

    def setCurrentByLabel(self,label):
        for btn in self._btnGrp.buttons():
            if btn.text() == label:
                btn.setChecked(True)
                return

    def getCurrentIndex(self):
        for idx, btn in enumerate(self._btnGrp.buttons()):
            if btn.isChecked():
                return idx

    def getCurrentLabel(self):
        return self.curentWidget.label

    @property
    def currentWidget(self):
        return self._btnGrp.checkedButton()

    def getCurrentData(self):
        return self.currentWidget.data

    def getValue(self):
        return self.checkedButton().text()

class Button(QtGui.QPushButton):
    pass