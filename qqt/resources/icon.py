import os

try:
    from pathlib import Path
except ImportError:
    from qqt.helper_lib.pathlib import Path

class IconManager(object):
    dirs = []

    @classmethod
    def get(cls, iconName, **kwargs):
        from qqt.base import QtGui, QtCore
        # TODO : to be completed
        itype = kwargs.get("type","icon")
        size = kwargs.get("size",None)

        iconPath = ""
        icon = None

        for eachDir in cls.dirs:
            checkPath = Path(eachDir) / iconName
            if checkPath.exists():
                iconPath = str(checkPath)
                break

        if itype == "icon":
            icon =  QtGui.QIcon(iconPath)

        elif itype == "pixmap":
            icon = QtGui.QPixmap(iconPath)
            if size:
                icon = icon.scaled(size[0],size[1], aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        elif itype == "path":
            icon = iconPath

        return icon


    @classmethod
    def addDir(cls, dirPath):
        cls.dirs.append(dirPath)