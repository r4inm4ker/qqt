from functools import partial
from .. import QtGui, QtCore, QtWidgets, qcreate
from ..layouts import VBoxLayout, HBoxLayout
from .base import BaseWidget, LabelMixin
from ..lib import pixmap

Qt = QtCore.Qt

class LabelPosition(object):
    left = "left"
    right = "right"
    center = "center"
    centre = "center"
    bottom = "bottom"
    top = "top"

class InputMixin(QtCore.QObject):
    valueEdited = QtCore.Signal(str)

    def getValue(self):
        return None

    def setValue(self, value):
        pass

    def emitValueEdited(self, value):
        self.valueEdited.emit(value)

    def _connectSignals(self):
        pass

class Button(QtWidgets.QPushButton, InputMixin, LabelMixin):
    def __init__(self,*args,**kwargs):
        self._labelPos = kwargs.pop("labelPosition","left")
        self._label = kwargs.pop("label",None)
        super(Button, self).__init__(*args,**kwargs)
        self._initLayout()
        self._connectSignals()

    def _connectSignals(self):
        pass


class ComboBox(QtWidgets.QComboBox, InputMixin, LabelMixin):
    valueEdited = QtCore.Signal(int)

    def __init__(self, *args, **kwargs):
        self._labelPos = kwargs.pop("labelPosition","left")
        self._label = kwargs.pop("label",None)
        width = kwargs.pop("width",None)
        super(ComboBox, self).__init__(*args, **kwargs)
        if width:
            self.setMinimumWidth(width)
        self._initLayout()
        self._connectSignals()

    def _connectSignals(self):
        self.currentIndexChanged.connect(self.emitValueEdited)

    def emitValueEdited(self,index):
        self.valueEdited.emit(index)

    def setItems(self, items, data=None):
        data = data or [None]*len(items)
        while self.count() > 0:
            for idx in range(self.count()):
                self.removeItem(idx)

        for item,dt in zip(items,data):
            self.addItem(item, data)

    def items(self):
        items = []
        for idx in range(self.count()):
            items.append(self.itemText(idx))
        return items

    def addItem(self, item, data=None):
        QtWidgets.QComboBox.addItem(self,str(item))
        idx = self.count() - 1
        data = data if data is not None else item
        self.setItemData(idx, data)

    def getValue(self):
        return self.currentText()

    def getData(self, index=None):
        index = index or self.currentIndex()
        return self.itemData(index)

    def setIndex(self, index):
        self.setCurrentIndex(index)
        self.valueEdited.emit(index)

    def setValue(self, value):
        idx = self.findText(value)
        if idx >= 0:
            self.setCurrentIndex(idx)
        else:
            raise ValueError("wrong or nonexistent value provided.")
        self.valueEdited.emit(idx)

    def setValueFromData(self, data):
        idx = self.findData(data)
        if idx >=0:
            self.setCurrentIndex(idx)
        else:
            raise ValueError("wrong or nonexistent data provided.")

        self.valueEdited.emit(idx)

class StringField(QtWidgets.QLineEdit, InputMixin, LabelMixin):
    valueEdited = QtCore.Signal(str)

    def __init__(self,*args,**kwargs):
        self._labelPos = kwargs.pop("labelPosition","left")
        self._label = kwargs.pop("label",None)
        super(StringField, self).__init__(*args,**kwargs)
        self._initLayout()
        self._connectSignals()

    def _connectSignals(self):
        self.editingFinished.connect(self.emitValueEdited)

    def emitValueEdited(self, value=None):
        value = value or self.text()
        self.valueEdited.emit(value)

    def getValue(self):
        return str(self.text())

    def setValue(self, val):
        if val:
            self.setText(str(val))
        else:
            self.setText("")

class Checkbox( QtWidgets.QCheckBox, InputMixin, LabelMixin):
    valueEdited = QtCore.Signal(bool)

    def __init__(self,*args,**kwargs):
        self._labelPos = kwargs.pop("labelPosition","left")
        self._label = kwargs.pop("label",None)
        default = kwargs.pop("default", True)
        super(Checkbox, self).__init__(*args,**kwargs)
        self._initLayout()

        if self._labelPos == "left":
            self.setLayoutDirection(QtCore.Qt.RightToLeft)

        elif self._labelPos == "right":
            self.setLayoutDirection(QtCore.Qt.LeftToRight)

        self._connectSignals()
        self.setChecked(default)

    def _connectSignals(self):
        self.stateChanged.connect(self.emitValueEdited)

    def getValue(self):
        return self.isChecked()

    def setValue(self,val):
        self.setChecked(val)

class IconButton(QtWidgets.QPushButton, InputMixin, LabelMixin):
    def __init__(self,*args,**kwargs):
        self._icon = kwargs.pop('icon',None)
        self._width = kwargs.pop('w',30)
        self._height = kwargs.pop('h',30)
        self._labelPos = kwargs.pop("labelPosition","bottom")
        self._label = kwargs.pop("label", None)
        super(IconButton, self).__init__(*args,**kwargs)
        self._initLayout()
        self._connectSignals()
        self._additionalSetup()


    def _additionalSetup(self):
        w, h = self._width, self._height
        pix = pixmap(self._icon, w, h)
        self.setFixedWidth(w)
        self.setFixedHeight(h)
        icon = QtGui.QIcon(pix)
        self.setIcon(icon)
        self.setIconSize(QtCore.QSize(w,h))

        if self.labelWidget:
            font = self.labelWidget.font()
            fm = QtGui.QFontMetrics(font)
            tw = fm.width(self.labelWidget.text())
            self.labelWidget.setFixedWidth(tw)

        if self._labelPos in(LabelPosition.bottom, LabelPosition.top):
            from qqt.widgets.displays import Spacer
            hlayout1 = HBoxLayout()
            spacer = Spacer(mode="horizontal")
            hlayout1.addItem(spacer)
            hlayout1.addWidget(self)
            spacer = Spacer(mode="horizontal")
            hlayout1.addItem(spacer)

            hlayout2 = HBoxLayout()
            spacer = Spacer(mode="horizontal")
            hlayout2.addItem(spacer)
            hlayout2.addWidget(self.labelWidget)
            self.labelWidget.setAlignment(QtCore.Qt.AlignCenter)
            spacer = Spacer(mode="horizontal")
            hlayout2.addItem(spacer)

            if self._labelPos == LabelPosition.top:
                self.parentLayout.insertLayout(0, hlayout2)
                self.parentLayout.insertLayout(1, hlayout1)
            elif self._labelPos == LabelPosition.bottom:
                self.parentLayout.insertLayout(0, hlayout1)
                self.parentLayout.insertLayout(1, hlayout2)


            spacer = Spacer(mode="vertical")
            self.parentLayout.addItem(spacer)






    def _connectSignals(self):
        pass


class NumericField(QtWidgets.QLineEdit,InputMixin, LabelMixin):
    def __init__(self,*args, **kwargs):
        minimum = kwargs.pop("minimum", None)
        maximum = kwargs.pop("maximum", None)
        self._width = kwargs.pop("width",None)
        self._defaultValue = kwargs.pop("defaultValue",None)
        self._labelPos = kwargs.pop("labelPosition","left")
        self._label = kwargs.pop("label",None)
        super(NumericField, self).__init__(*args,**kwargs)
        self._initLayout()
        self._connectSignals()
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

        self.setValidator(self.validator)

        if self._defaultValue is not None:
            self.setValue(self._defaultValue)

    def _connectSignals(self):
        self.editingFinished.connect(self.emitValueEdited)

    def emitValueEdited(self):
        val = self.getValue()
        self.valueEdited.emit(val)

    @property
    def validator(self):
        raise NotImplemented("must implement validator")

    def getValue(self):
        raise NotImplemented("must implement getValue")

    def setValue(self, value):
        raise NotImplemented("must implement setValue")


class LabelledInput(BaseWidget, InputMixin):
    def __init__(self, *args, **kwargs):
        layout = kwargs.pop("layout","horizontal")
        label = kwargs.pop("label","")
        parent = kwargs.pop("parent",None)

        super(LabelledInput, self).__init__(parent)

        self._label = None

        if layout == "horizontal":
            self._layout = HBoxLayout(self)
        elif layout == "vertical":
            self._layout = VBoxLayout(self)

        with self._layout:
            label = label or ""

            if layout == "horizontal":
                if label:
                    self._label = qcreate(QtWidgets.QLabel,label)
                self._inputWidget = qcreate(self.inputClass,*args,**kwargs)
            elif layout == "vertical":
                self._inputWidget = qcreate(self.inputClass,*args,**kwargs)
                if label:
                    self._label = qcreate(QtWidgets.QLabel,label)
                    self._label.setAlignment(Qt.AlignHCenter)

        if self._label:
            self._label.setSizePolicy(QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed)

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
        return QtWidgets.QLineEdit

    def __getattr__(self, item):
        return getattr(self.input, item)

    def _additionalSetup(self):
        pass


class IntField(NumericField):
    valueEdited = QtCore.Signal(int)

    def emitEditingFinished(self):
        val = int(self.text())
        self.valueEdited.emit(val)

    @property
    def validator(self):
        if not self._validator:
            self._validator = QtGui.QIntValidator()
        return self._validator

    def getValue(self):
        text = self.text()
        try:
            return int(text)
        except ValueError:
            return None

    def setValue(self, value):
        if value is None:
            value = 0
        try:
            int(value)
        except (ValueError, TypeError):
            raise ValueError("input type is not a numeric value.")
        else:
            self.setText(str(value))
            self.valueEdited.emit(value)


class FloatField(NumericField):
    valueEdited = QtCore.Signal(float)

    def emitEditingFinished(self):
        val = float(self.text())
        self.valueEdited.emit(val)

    @property
    def validator(self):
        if not self._validator:
            self._validator = QtGui.QDoubleValidator()
        return self._validator

    def getValue(self):
        text = self.text()
        try:
            return float(text)
        except ValueError:
            return None

    def setValue(self, value):
        if value is None:
            value = 0
        try:
            float(value)
        except (ValueError, TypeError):
            raise ValueError("input type is not a numeric value.")
        else:
            self.setText(str(value))
            self.valueEdited.emit(value)


class ColorInput(QtWidgets.QPushButton,InputMixin, LabelMixin):
    valueEdited = QtCore.Signal(QtGui.QColor)
    defaultColor = QtGui.QColor(198, 128, 128)
    sizePol = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

    def __init__(self, *args, **kwargs):
        self._labelPos = kwargs.pop("labelPosition","left")
        self._label = kwargs.pop("label",None)
        super(ColorInput, self).__init__(*args,**kwargs)
        self._initLayout()
        self._connectSignals()

        self._color = None
        self.setValue(self.defaultColor)
        self.setSizePolicy(self.sizePol)

        self._connectSignals()

    def _connectSignals(self):
        self.clicked.connect(self.summonColorDialog)

    def getValue(self):
        return self._color

    def setValue(self, color):
        self._color = color
        self.setStyleSheet("QPushButton {background-color: rgb(%d,%d,%d)}" % (color.red(), color.green(), color.blue()))

    def summonColorDialog(self):
        colorDialog = QtWidgets.QColorDialog()
        currColor = self.getValue()
        retColor = colorDialog.getColor(initial=currColor)

        if retColor.isValid():
            self.setValue(retColor)
            self.valueEdited.emit(retColor)


class RadioButtonGroup(QtWidgets.QWidget,InputMixin, LabelMixin):
    valueEdited = QtCore.Signal(str)
    def __init__(self, *args, **kwargs):
        self._labelPos = kwargs.pop("labelPosition","left")
        self._label = kwargs.pop("label",None)
        super(RadioButtonGroup, self).__init__(*args,**kwargs)
        self._initLayout()
        self._connectSignals()
        # self._btnList = []
        self._btnGrp = QtWidgets.QButtonGroup(self)
        self._btnGrp.setExclusive(True)
        self._layout = HBoxLayout(self)
        self._layout.setContentsMargins(0,0,0,0)
        self._layout.setSpacing(2)
        self._btnGrp.buttonClicked.connect(self.emitValueEdited)


    def addOption(self, label, data=None):
        rb = QtWidgets.QRadioButton(text=label)
        rb.setCheckable(True)
        rb.data = data
        rb.label = label
        self._btnGrp.addButton(rb)
        self._layout.addWidget(rb)

        rb.setStyleSheet('''
        QRadioButton{
        font:bold;
        }
        ''')




        # self._btnList.append(rb)

    def setIndex(self,idx):
        if self._btnGrp.buttons():
            self._btnGrp.buttons()[idx].setChecked(True)

    def setValue(self,label):
        for btn in self._btnGrp.buttons():
            if btn.text() == label:
                btn.setChecked(True)
                return

    def getCurrentIndex(self):
        for idx, btn in enumerate(self._btnGrp.buttons()):
            if btn.isChecked():
                return idx

    def getCurrentLabel(self):
        return self.currentOption.label

    @property
    def currentOption(self):
        return self._btnGrp.checkedButton()

    def getData(self):
        return self.currentOption.data

    def getValue(self):
        return self._btnGrp.checkedButton().text()

    def emitValueEdited(self, value=None):
        self.valueEdited.emit(self.getCurrentLabel())


class NumericSliderField(QtWidgets.QWidget, InputMixin, LabelMixin):
    valueEdited = QtCore.Signal(float)

    @property
    def fieldClass(self):
        return FloatField

    def __init__(self, *args,**kwargs):
        self.MIN_VAL = kwargs.pop("minVal",self.DEFAULT_MIN)
        self.MAX_VAL = kwargs.pop("maxVal",self.DEFAULT_MAX)
        self._labelPos = kwargs.pop("labelPosition","left")
        self._label = kwargs.pop("label",None)
        super(NumericSliderField, self).__init__(*args,**kwargs)
        self._initLayout()


        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        self.field = self.fieldClass()
        self.field.setMaximumWidth(100)

        self.layout.addWidget(self.field)

        self.minBtn = QtWidgets.QPushButton()
        self.minBtn.setFixedWidth(3)
        self.minBtn.setFixedHeight(3)
        self.layout.addWidget(self.minBtn)

        self.slider = Slider()
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setContentsMargins(0,0,0,0)
        self.layout.addWidget(self.slider)

        self.maxBtn = QtWidgets.QPushButton()
        self.maxBtn.setFixedWidth(3)
        self.maxBtn.setFixedHeight(3)
        self.layout.addWidget(self.maxBtn)

        self._connectSignals()
        self.updateField()

    def _connectSignals(self):
        self.slider.sliderPressed.connect(self.updateField)
        self.slider.sliderMoved.connect(self.updateField)
        self.field.editingFinished.connect(self.fieldUpdated)
        self.minBtn.clicked.connect(partial(self.updateField,self.MIN_VAL))
        self.maxBtn.clicked.connect(partial(self.updateField,self.MAX_VAL))

    def getValue(self):
        raise NotImplementedError()

    def setValue(self, val):
        raise NotImplementedError()

    def fieldUpdated(self, val):
        raise NotImplementedError()

    def updateField(self, val=None):
        raise NotImplementedError()

class FloatSliderField(NumericSliderField):
    MIN_INT = -100
    MAX_INT = 100
    DEFAULT_MIN = 0.0
    DEFAULT_MAX = 1.0

    def __init__(self,*args,**kwargs):
        super(FloatSliderField, self).__init__(*args,**kwargs)
        self.slider.setMinimum(self.MIN_INT)
        self.slider.setMaximum(self.MAX_INT)
        self.minBtn.clicked.connect(partial(self.updateField,self.MIN_INT))
        self.maxBtn.clicked.connect(partial(self.updateField,self.MAX_INT))

    def updateField(self,val=None):
        if val is not None:
            self.slider.setValue(val)
        val = val or self.slider.value()

        newVal = (1.0*(val - self.MIN_INT) / (self.MAX_INT - self.MIN_INT)) * (self.MAX_VAL - self.MIN_VAL) + self.MIN_VAL

        self.field.setText(str(newVal))
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

    def fieldUpdated(self, *args):
        if len(args)>0:
            val = args[0]
        else:
            val = self.field.getValue()

        self.valueEdited.emit(float(val))


class IntSliderField(NumericSliderField):
    DEFAULT_MIN = 0
    DEFAULT_MAX = 100

    @property
    def fieldClass(self):
        return IntField

    def __init__(self,*args,**kwargs):
        super(IntSliderField, self).__init__(*args,**kwargs)
        self.slider.setMinimum(self.MIN_VAL)
        self.slider.setMaximum(self.MAX_VAL)

    def updateField(self,val=None):
        if val is not None:
            self.slider.setValue(val)
        val = val or self.slider.value()

        self.field.setText(str(val))
        self.valueEdited.emit(val)


    def getValue(self):
        text = self.field.text()
        retVal = 0
        try:
            retVal = int(text)
        except ValueError:
            pass
        return retVal

    def setValue(self, value):
        try:
            int(value)
        except (ValueError, TypeError):
            value = 0
        finally:
            self.field.setText(str(value))

    def fieldUpdated(self, *args):
        if len(args)>0:
            val = args[0]
        else:
            val = self.field.getValue()

        self.valueEdited.emit(int(val))

class Slider(QtWidgets.QSlider):
    editStarted = QtCore.Signal()
    editEnded = QtCore.Signal()

    def __init__(self,*args,**kwargs):
        super(Slider, self).__init__(*args, **kwargs)


    def mousePressEvent(self, event):
        QtWidgets.QSlider.mousePressEvent(self, event)
        self.editStarted.emit()

    def mouseReleaseEvent(self, event):
        QtWidgets.QSlider.mouseReleaseEvent(self, event)
        self.editEnded.emit()






