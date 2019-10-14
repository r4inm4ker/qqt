from ..base import QtWidgets, QtCore, QtGui, qcreate
from ..layouts import VBoxLayout
from .inputs import StringField

# for python2 & 3 cross compatibility
try:
    basestring
except NameError:
    basestring = str


class BaseList(QtWidgets.QWidget):
    itemSelectionChanged = QtCore.Signal(list)
    itemSelected = QtCore.Signal()

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.view = None
        self.selModel = None
        self._filterModel = None
        self._model = None
        self._initView()
        self._connectMV()
        self._initUI()
        self._connectSignals()

    @property
    def model(self):
        if not self._model:
            self._model = QtGui.QStandardItemModel()
        return self._model

    def _initView(self):
        raise NotImplementedError('')

    @property
    def filterClass(self):
        return SimpleFilter

    @property
    def filterModel(self):
        if self._filterModel is None:
            self._filterModel = self.filterClass(self)
        return self._filterModel

    def _connectMV(self):
        # self.view.setModel(self.model)
        # self.selModel = self.view.selectionModel()
        self.filterModel.setSourceModel(self.model)
        self.filterModel.setDynamicSortFilter(True)
        self.view.setModel(self.filterModel)
        self.selModel = self.view.selectionModel()

    def _initUI(self):
        self._layout = VBoxLayout(self)
        with self._layout:
            self.filterField = qcreate(StringField)
        self._layout.addWidget(self.view)
        self._layout.setContentsMargins(0, 0, 0, 0)

    def refreshData(self):
        raise NotImplementedError('')

    def addItem(self, item, data=None):
        raise NotImplementedError('')

    def _connectSignals(self):
        self.selModel.selectionChanged.connect(self.selectionChangedCallback)
        # self.filterField.valueEdited.connect(self.updateFilter)
        self.filterField.textEdited.connect(self.updateFilter)

    def selectionChangedCallback(self):
        pass

    def selectedItems(self):
        indexes = self.selModel.selectedIndexes()
        indexes = [self.filterModel.mapToSource(idx) for idx in indexes]
        items = [self.model.itemFromIndex(idx) for idx in indexes if idx.column() == 0]
        return items

    def showFilterField(self, mode):
        if mode == True:
            self.filterField.setHidden(False)
            self.filterField.setFixedHeight(40)
        else:
            self.filterField.setHidden(True)
            self.filterField.setFixedHeight(0)

    def selectAll(self):
        self.view.selectAll()

    def clear(self):
        self.model.clear()

    def items(self):
        items = []
        for idx in range(self.model.rowCount()):
            try:
                item = self.model.item(idx, 0)
            except AttributeError:
                continue
            if item:
                items.append(item)

        return items

    def clearSelection(self):
        self.view.clearSelection()

    def selectItem(self, item, selectionMode=QtCore.QItemSelectionModel.ClearAndSelect):
        qi = self.model.indexFromItem(item)
        qi = self.filterModel.mapFromSource(qi)
        self.selModel.select(qi, selectionMode)

    def deleteItem(self, item, *args):
        for idx in range(self.model.rowCount()):
            midx = self.model.index(idx, 0)
            mitem = self.model.itemFromIndex(midx)

            if isinstance(item, QtGui.QStandardItem):
                if mitem is item:
                    self.model.takeRow(idx)
                    return

            elif isinstance(item, basestring):
                if mitem.text() == item:
                    self.model.takeRow(idx)
                    return

    def deleteItemFromSelected(self):
        for selIndex in self.selModel.selectedRows():
            row = selIndex.row()
            self.model.removeRow(row)

    def updateFilter(self):
        val = self.filterField.getValue()
        # self.filterModel.setFilter(val)
        self.filterModel.setFilterRegExp(val)
        self.filterModel.submit()


class ItemDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self):
        super(ItemDelegate, self).__init__()

    def createEditor(self, parent, option, index):
        editor = QtWidgets.QLineEdit(parent)
        return editor

    def setEditorData(self, editor, index):
        model = index.model()
        role = QtCore.Qt.DisplayRole
        value = model.data(index, role)
        # editor.setText(value)

    def setModelData(self, editor, model, index):
        value = editor.text()
        # item = model.itemFromIndex(index)
        model.setData(index, value)

    def updateEditorGeometry(self, editor, option, index):
        option.rect.setHeight(30)
        editor.setGeometry(option.rect)


class TextList(BaseList):
    def _initView(self):
        self.view = QtWidgets.QTreeView(self)
        self.view.setModel(self.model)
        self.view.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.itemDelegate = ItemDelegate()
        self.view.setItemDelegate(self.itemDelegate)

    def initData(self, data):
        self.model.clear()
        for eachData in data:
            self.addItem(eachData)
        self.selModel.clear()

    def addItem(self, item, data=None):
        if not isinstance(item, TextItem):
            newItem = TextItem(item, data=data)
            self.model.appendRow(newItem)
        else:
            self.model.appendRow(item)


class TextItem(QtGui.QStandardItem):

    def __init__(self, text, *args, **kwargs):
        self._text = kwargs.pop("data", None)
        super(TextItem, self).__init__(text, *args, **kwargs)


class SimpleFilter(QtCore.QSortFilterProxyModel):
    def __init__(self, *args, **kwargs):
        super(SimpleFilter, self).__init__(*args, **kwargs)
        self._filter = ''

    def setFilter(self, text):
        self._filter = text

    def filter(self):
        return self._filter

    def setCaseSensitive(self, val):
        cs = QtCore.Qt.CaseSensitive if val else QtCore.Qt.CaseInsensitive
        self.setFilterCaseSensitivity(cs)


class FileBrowser(BaseList):
    def __init__(self, *args, **kwargs):
        super(FileBrowser, self).__init__(*args, **kwargs)

        self._additionalSetup()

    def _initView(self):
        self.view = QtWidgets.QTreeView(self)
        self.view.setModel(self.model)
        self.view.setRootIndex(self.model.index(r"E:\testdelete"))
        self.view.selectionModel()
        self.itemDelegate = ItemDelegate()
        self.view.setItemDelegate(self.itemDelegate)

    @property
    def model(self):
        if not self._model:
            self._model = QtWidgets.QFileSystemModel()
            self._model.setRootPath(r"e:\reference")
        return self._model

    @property
    def filterClass(self):
        return FileTreeFilter

    def _additionalSetup(self):
        pass

    def updateFilter(self):
        val = self.filterField.getValue()

        self.filterModel.setFilterRegExp(val)
        self.filterModel.setFilterKeyColumn(0)
        self.filterModel.submit()


class FileTreeFilter(SimpleFilter):

    def filterAcceptsRow(self, *args, **kwargs):
        return False
        # return super(FileTreeFilter, self).filterAcceptsRow(*args, **kwargs)
