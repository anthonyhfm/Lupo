from ..core.view import View
from lupo.styling.style import Style
import sys

if sys.platform == "win32":
    from ..core.win32.win32_structs import *
    from ctypes import *
    from ctypes.wintypes import *
    import win32api
    import win32con
    import win32gui

if sys.platform == "darwin":
    from ..core.osx.osx_override import LupoNSComboBox

from ..styling.applier import *


class Select(View):
    options: list[str]
    placeholder: str

    def __init__(self, options: list[str], placeholder: str = None, style: Style = None):
        super().__init__(style=style)
        self.placeholder = placeholder
        self.options = options

    def add_option(self, option: str):
        self.options.append(option)
        self.reload_options()

    def reload_options(self):
        if sys.platform == "darwin":
            self._ns_combobox.removeAllItems_()
            for option in self.options:
                self._ns_combobox.addItemWithObjectValue_(option)

    def remove_option(self, option: str):
        self.options.remove(option)
        self.reload_options()

    def get_osx_render(self, parent=None, superview=None):
        self._ns_combobox = LupoNSComboBox.alloc().initWithFrame_(((0, 0), (0, 0)))
        self._ns_combobox.sizeToFit()

        apply_osx_view_style(self._ns_combobox, self.style)

        combobox_frame = self._ns_combobox.frame()
        combobox_frame.size.width = self.style.width if self.style.width is not None else 120
        combobox_frame.size.height = self.style.height if self.style.height is not None else combobox_frame.size.height
        self._ns_combobox.setFrame_(combobox_frame)

        if self.placeholder is not None:
            self._ns_combobox.addItemWithObjectValue_(self.placeholder)
            self._ns_combobox.selectItemWithObjectValue_(self.placeholder)

        for option in self.options:
            self._ns_combobox.addItemWithObjectValue_(option)

        return self._ns_combobox
