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


    def get_win32_render(self, hwnd, hinst):
        view_height = self.style.height if self.style.height is not None else 0
        view_width = self.style.width if self.style.width is not None else 0
        print(self.style)

        view_hwnd = windll.user32.CreateWindowExW(
            0,
            "Static",
            self.text,
            WS_CHILD | win32con.SS_CENTER,
            0, 0,
            view_width, view_height,
            hwnd,
            0,
            windll.user32.GetWindowLongPtrA(hwnd, hinst),
            0
        )

        self._hwnd = view_hwnd
        self._hinst = hinst

        ep = win32gui.GetTextExtentPoint32(win32gui.GetDC(view_hwnd), self.text)

        windll.user32.SetWindowPos(
            self._hwnd,
            0,
            0, 0,
            ep[0] if self.style.width is None else self.style.width, 
            ep[1] if self.style.height is None else self.style.height,
            0
        )

        apply_win32_hwnd_style(self._hwnd, self.style)

        return view_hwnd

    
    def show_win32_view(self):
        style = win32api.GetWindowLong(self._hwnd, win32con.GWL_STYLE)
        win32gui.SetWindowLong(self._hwnd, win32con.GWL_STYLE, (style | win32con.WS_VISIBLE))


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