from .. import QtCore, QtGui, qcreate, QtWidgets
from ..layouts import LayoutMixin, HBoxLayout, VBoxLayout
from ..lib import pixmap


class Image(QtWidgets.QLabel):
    clicked = QtCore.Signal()

    def __init__(self, image, parent=None, w=None, h=None, fixed=False):
        super(Image, self).__init__(parent)
        self.w = w
        self.h = h

        pic = self.setImage(image, w=w, h=h)
        if fixed:
            self.setFixedWidth(pic.width())
            self.setFixedHeight(pic.height())

    def mousePressEvent(self, *args, **kwargs):
        super(Image, self).mousePressEvent(*args, **kwargs)
        self.clicked.emit()

    def setImage(self, img, w=None, h=None):
        pic = pixmap(img, w=w, h=h)
        self.setPixmap(pic)
        return pic


class Spacer(QtWidgets.QSpacerItem):
    def __init__(self, mode="horizontal"):
        args = [None, None, None, None]
        if mode == "horizontal":

            args[0] = 20
            args[1] = 10
            args[2] = QtWidgets.QSizePolicy.Expanding
            args[3] = QtWidgets.QSizePolicy.Minimum
        elif mode == "vertical":
            args[0] = 20
            args[1] = 10
            args[2] = QtWidgets.QSizePolicy.Minimum
            args[3] = QtWidgets.QSizePolicy.Expanding

        super(Spacer, self).__init__(*args)


class SeparatorLine(QtWidgets.QFrame):
    def __init__(self, mode="horizontal"):
        super(SeparatorLine, self).__init__()
        if mode == 'horizontal':
            self.setFrameShape(QtWidgets.QFrame.HLine)
        elif mode == 'vertical':
            self.setFrameShape(QtWidgets.QFrame.VLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)


class Splitter(QtWidgets.QSplitter, LayoutMixin):
    def __init__(self, mode="horizontal"):
        if mode == "horizontal":
            orient = QtCore.Qt.Horizontal
        elif mode == "vertical":
            orient = QtCore.Qt.Vertical
        else:
            orient = QtCore.Qt.Horizontal

        super(Splitter, self).__init__(orient)

        # self.setStyleSheet('''QSplitter::handle:horizontal{border: 1px outset darkgrey;};QSplitter::handle:vertical{border: 1px outset darkgrey;}''')


class TabLayout(QtWidgets.QTabWidget, LayoutMixin):
    def addWidget(self, widget):
        self.addTab(widget, widget.title)


class TabWidget(QtWidgets.QWidget):
    def __init__(self, title=""):
        super(TabWidget, self).__init__()
        self.title = title


class SimpleFrameWidget(QtWidgets.QFrame):
    def __init__(self):
        super(SimpleFrameWidget, self).__init__()
        self._initUI()

    def _initUI(self):
        self.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.setFrameStyle(QtWidgets.QFrame.StyledPanel)
        layout = VBoxLayout(self)

    def _connectSignals(self):
        pass


class FrameWidget(QtWidgets.QFrame):
    collapsed = QtCore.Signal()
    expanded = QtCore.Signal()
    toggled = QtCore.Signal()

    def __init__(self, parent=None, title=None):
        self._titleText = title
        super(FrameWidget, self).__init__(parent)
        self._isCollapsed = False
        self._titleFrame = None
        self._fillTitleBg = True
        self._contentWidget = None
        self.contentLayout = None

        self._initUI()
        self._connectSignals()

    def _initUI(self):
        self.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.setFrameStyle(QtWidgets.QFrame.StyledPanel)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(4)
        self._titleFrame = qcreate(self.TitleWidget, title=self._titleText, collapsed=self._isCollapsed)
        layout.addWidget(self._titleFrame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setStretchFactor(self._titleFrame, 0)

        self._contentWidget = QtWidgets.QWidget()
        layout.addWidget(self._contentWidget)
        self.contentLayout = VBoxLayout(self._contentWidget)
        self.contentLayout.setContentsMargins(3, 2, 3, 2)
        layout.setStretchFactor(self._contentWidget, 1)

        if self._fillTitleBg:
            self._titleFrame.fillBackground()

    def _connectSignals(self):
        self._titleFrame.clicked.connect(self.toggleCollapsed)

    def toggleCollapsed(self):
        self._contentWidget.setVisible(self._isCollapsed)
        self._isCollapsed = not self._isCollapsed
        self._titleFrame.arrow.setArrow(int(self._isCollapsed))
        self.adjustSize()

        if self._isCollapsed:
            self.collapsed.emit()
            self.toggled.emit()
            height = self.sizeHint().height()
            self.setMaximumHeight(height)
        else:
            self.expanded.emit()
            self.toggled.emit()
            self.setMaximumHeight(10000000)

    class TitleWidget(QtWidgets.QWidget):
        clicked = QtCore.Signal()

        def __init__(self, parent=None, title="", collapsed=False):
            self._titleText = title
            super(FrameWidget.TitleWidget, self).__init__(parent)

            self._isCollapsed = collapsed
            self.arrow = None
            self._initUI()

        def _initUI(self):
            self.setFixedHeight(19)

            layout = HBoxLayout(self)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
            with layout:
                self.arrow = qcreate(FrameWidget.Arrow, collapsed=self._isCollapsed)
                self.arrow.setContentsMargins(0, 0, 0, 0)

                self.title = qcreate(QtWidgets.QLabel, self._titleText)
                self.title.setAlignment(QtCore.Qt.AlignVCenter)
                self.title.setContentsMargins(4, 0, 0, 0)

        def mousePressEvent(self, event):
            self.clicked.emit()
            return super(FrameWidget.TitleWidget, self).mousePressEvent(event)

        def fillBackground(self):
            bgColor = (110, 110, 110)
            titleColor = (200, 200, 200)
            self.title.setStyleSheet("QLabel {{font-weight:bold; color:rgb({0},{1},{2}); }}".format(*titleColor))
            self.setStyleSheet("QWidget {{background-color: rgb({0},{1},{2});}}".format(*bgColor))

    class Arrow(QtWidgets.QWidget):
        def __init__(self, parent=None, collapsed=False):
            super(FrameWidget.Arrow, self).__init__(parent)
            self._collapsed = collapsed
            self._arrow = None
            self._initUI()

        def _initUI(self):
            self.setMaximumWidth(24)
            # expanded == 0
            self._arrow_expanded = (QtCore.QPointF(7.0, 6.0), QtCore.QPointF(17.0, 6.0), QtCore.QPointF(12.0, 11.0))
            # vertical == 1
            self._arrow_collapsed = (QtCore.QPointF(8.0, 4.0), QtCore.QPointF(13.0, 9.0), QtCore.QPointF(8.0, 14.0))
            # arrow
            self._arrow = None
            self.setArrow(int(self._collapsed))

        def setArrow(self, arrow_dir):
            if arrow_dir == 1:
                self._arrow = self._arrow_collapsed
            else:
                self._arrow = self._arrow_expanded
            self.update()

        def paintEvent(self, event):
            painter = QtGui.QPainter()
            painter.begin(self)
            painter.fillRect(self.rect(), QtGui.QColor(110, 110, 110))
            painter.setBrush(QtGui.QColor(192, 192, 192))
            painter.setPen(QtGui.QColor(64, 64, 64))
            painter.drawPolygon(self._arrow)
            painter.end()
