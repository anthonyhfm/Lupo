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
    from Cocoa import NSTextField

from ..styling.applier import *


class TextInput(View):
    options: list[str]
    _placeholder: str

    def __init__(self, placeholder: str = None, style: Style = None):
        super().__init__(style=style)
        self._placeholder = placeholder

    @property
    def placeholder(self):
        return self._placeholder

    @placeholder.setter
    def placeholder(self, value):
        self._placeholder = value
        self._ns_textfield.setPlaceholderString_(value)

    def get_osx_render(self, parent=None, superview=None):
        self._ns_textfield = NSTextField.alloc().initWithFrame_(((0, 0), (0, 0)))
        self._ns_textfield.sizeToFit()

        apply_osx_view_style(self._ns_textfield, self.style)

        textfield_frame = self._ns_textfield.frame()
        textfield_frame.size.width = self.style.width if self.style.width is not None else 120
        textfield_frame.size.height = self.style.height if self.style.height is not None else textfield_frame.size.height
        self._ns_textfield.setFrame_(textfield_frame)

        if self.placeholder is not None:
            self._ns_textfield.setPlaceholderString_(self._placeholder)

        return self._ns_textfield
