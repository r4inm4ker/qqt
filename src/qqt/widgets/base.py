from ..base import QtGui, QtWidgets
from ..layouts import HBoxLayout, VBoxLayout


class BaseWidget(QtWidgets.QWidget):
    @classmethod
    def launch(cls, *args, **kwargs):
        ui = cls()
        ui.show()
        return ui


class GenericWidget(BaseWidget):
    def __init__(self, *args, **kwargs):
        super(GenericWidget, self).__init__(*args, **kwargs)
        self._initUI()
        self._connectSignals()

    def _initUI(self):
        pass

    def _connectSignals(self):
        pass


class LabelMixin(object):
    class Position(object):
        Left = "left"
        Right = "right"
        Top = "top"
        Bottom = "bottom"

    def _initLayout(self, **kwargs):
        self.labelWidget = None
        self.parentWidget = None
        self.parentLayout = None
        if self._label is not None:

            self.parentWidget = QtWidgets.QWidget()

            if self._labelPos in (self.Position.Left, self.Position.Right):
                self.parentLayout = QtWidgets.QHBoxLayout(self)
            elif self._labelPos in (self.Position.Top, self.Position.Bottom):
                self.parentLayout = QtWidgets.QVBoxLayout(self)

            self.parentWidget.setLayout(self.parentLayout)

            self.labelWidget = QtWidgets.QLabel(self._label)
            self.labelWidget.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

            if self._labelPos in (self.Position.Left or self.Position.Top):
                w1, w2 = self.labelWidget, self
            else:
                w1, w2 = self, self.labelWidget

            if w1:
                self.parentLayout.addWidget(w1)
            if w2:
                self.parentLayout.addWidget(w2)

            try:
                if self._width is not None:
                    self.setFixedWidth(self._width)
            except AttributeError:
                pass

            self.parentLayout.setContentsMargins(0, 0, 0, 0)
