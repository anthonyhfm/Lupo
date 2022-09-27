from ..core.view import View
from lupo.styling.style import Style
import sys

if sys.platform == "win32":
    from ..core.win32.win32_structs import *
    from ctypes import *
    from ctypes.wintypes import *

if sys.platform == "darwin":
    from ..core.osx.osx_override import LupoNSButton

from ..styling.applier import *


class Button(View):
    text: str
    onclick = None

    def __init__(self, text: str, style: Style=None, onclick=None):
        super().__init__(style=style)
        self.text = text
        self.onclick = onclick

    def get_win32_render(self, hwnd, hinst):
        view_hwnd = windll.user32.CreateWindowExW(
            0,
            "Button",
            self.text,
            WS_TABSTOP | WS_VISIBLE | WS_CHILD | BS_DEFPUSHBUTTON,  # BS_GROUPBOX would prob. be the right element style
            0, 0,
            self.style.width, self.style.height,
            hwnd,
            0,
            windll.user32.GetWindowLongPtrA(hwnd, hinst),
            0
        )

        return view_hwnd

    def get_osx_render(self, parent=None, superview = None):
        ns_button = LupoNSButton.alloc().initWithFrame_(((0, 0), (0, 0)))
        ns_button.setBezelStyle_(4)
        ns_button.setTitle_(self.text)
        ns_button.sizeToFit()

        apply_osx_view_style(ns_button, self.style)

        if self.onclick is not None:
            ns_button.setTarget_(self.parent_window.osx_window.app.delegate())
            ns_button.setAction_("buttonpress:")
            ns_button.onclick = self.onclick

        btn_frame = ns_button.frame()
        btn_frame.size.width = self.style.width if self.style.width is not None else btn_frame.size.width
        btn_frame.size.height = self.style.height if self.style.height is not None else btn_frame.size.height
        ns_button.setFrame_(btn_frame)

        return ns_button
