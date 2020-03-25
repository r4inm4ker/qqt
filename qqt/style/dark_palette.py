from qqt import QtGui, QtWidgets, QtCore


class DarkPalette(object):
    @classmethod
    def set(cls):
        base_palette = QtGui.QPalette()

        HIGHLIGHT_COLOR = QtGui.QColor(103, 141, 178)
        BRIGHTNESS_SPREAD = 2.5

        BRIGHT_COLOR = QtGui.QColor(200, 200, 200)
        LIGHT_COLOR = QtGui.QColor(100, 100, 100)
        DARK_COLOR = QtGui.QColor(42, 42, 42)
        MID_COLOR = QtGui.QColor(68, 68, 68)
        MID_LIGHT_COLOR = QtGui.QColor(84, 84, 84)
        SHADOW_COLOR = QtGui.QColor(21, 21, 21)

        BASE_COLOR = MID_COLOR
        TEXT_COLOR = BRIGHT_COLOR
        DISABLED_BUTTON_COLOR = QtGui.QColor(78, 78, 78)
        DISABLED_TEXT_COLOR = QtGui.QColor(128, 128, 128)
        ALTERNATE_BASE_COLOR = QtGui.QColor(46, 46, 46)

        if cls.lightness(BASE_COLOR) > 0.5:
            SPREAD = 100 / BRIGHTNESS_SPREAD
        else:
            SPREAD = 100 * BRIGHTNESS_SPREAD

        if cls.lightness(HIGHLIGHT_COLOR) > 0.6:
            HIGHLIGHTEDTEXT_COLOR = BASE_COLOR.darker(SPREAD * 2)
        else:
            HIGHLIGHTEDTEXT_COLOR = BASE_COLOR.lighter(SPREAD * 2)

        base_palette.setBrush(QtGui.QPalette.Window, QtGui.QBrush(MID_COLOR))
        base_palette.setBrush(QtGui.QPalette.WindowText, QtGui.QBrush(TEXT_COLOR))
        base_palette.setBrush(QtGui.QPalette.Foreground, QtGui.QBrush(BRIGHT_COLOR))
        base_palette.setBrush(QtGui.QPalette.Base, QtGui.QBrush(DARK_COLOR))
        base_palette.setBrush(QtGui.QPalette.AlternateBase, QtGui.QBrush(ALTERNATE_BASE_COLOR))
        base_palette.setBrush(QtGui.QPalette.ToolTipBase, QtGui.QBrush(BASE_COLOR))
        base_palette.setBrush(QtGui.QPalette.ToolTipText, QtGui.QBrush(TEXT_COLOR))

        base_palette.setBrush(QtGui.QPalette.Text, QtGui.QBrush(TEXT_COLOR))
        base_palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, QtGui.QBrush(DISABLED_TEXT_COLOR))

        base_palette.setBrush(QtGui.QPalette.Button, QtGui.QBrush(LIGHT_COLOR))
        base_palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, QtGui.QBrush(DISABLED_BUTTON_COLOR))
        base_palette.setBrush(QtGui.QPalette.ButtonText, QtGui.QBrush(TEXT_COLOR))
        base_palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, QtGui.QBrush(DISABLED_TEXT_COLOR))
        base_palette.setBrush(QtGui.QPalette.BrightText, QtGui.QBrush(TEXT_COLOR))
        base_palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, QtGui.QBrush(DISABLED_TEXT_COLOR))

        base_palette.setBrush(QtGui.QPalette.Light, QtGui.QBrush(LIGHT_COLOR))
        base_palette.setBrush(QtGui.QPalette.Midlight, QtGui.QBrush(MID_LIGHT_COLOR))
        base_palette.setBrush(QtGui.QPalette.Mid, QtGui.QBrush(MID_COLOR))
        base_palette.setBrush(QtGui.QPalette.Dark, QtGui.QBrush(DARK_COLOR))
        base_palette.setBrush(QtGui.QPalette.Shadow, QtGui.QBrush(SHADOW_COLOR))

        base_palette.setBrush(QtGui.QPalette.Highlight, QtGui.QBrush(HIGHLIGHT_COLOR))
        base_palette.setBrush(QtGui.QPalette.HighlightedText, QtGui.QBrush(HIGHLIGHTEDTEXT_COLOR))

        # Setup additional palettes for QTabBar and QTabWidget to look more like
        # maya.
        tab_palette = QtGui.QPalette(base_palette)
        tab_palette.setBrush(QtGui.QPalette.Window, QtGui.QBrush(LIGHT_COLOR))
        tab_palette.setBrush(QtGui.QPalette.Button, QtGui.QBrush(MID_COLOR))

        widget_palettes = {}
        widget_palettes["QTabBar"] = tab_palette
        widget_palettes["QTabWidget"] = tab_palette

        QtWidgets.QApplication.setStyle("Plastique")
        QtWidgets.QApplication.setPalette(base_palette)
        for name, palette in widget_palettes.items():
            QtWidgets.QApplication.setPalette(palette, name)

    @staticmethod
    def lightness(color):
        """Returns simple averaged lightness of a QColor
        Newer Qt Versions implement this as part of QColor
        Reimplemented for backwards-compatibility
        """
        hsv = color.toHsv()
        return hsv.valueF()
