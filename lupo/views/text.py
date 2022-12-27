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


class Text(View):
    text: str = ""

    def __init__(self, text: str, style: Style = None):
        super().__init__(style=style)
        self.text = text

    def get_osx_render(self, parent=None, superview = None):
        parent: View

        text_element = NSTextField.alloc().initWithFrame_(((0, 0), (0, 0)))
        text_element.setStringValue_(self.text)
        text_element.setBackgroundColor_(None)
        text_element.setBezeled_(False)
        text_element.setEditable_(False)
        text_element.sizeToFit()

        apply_osx_view_style(text_element, self.style)

        return text_element