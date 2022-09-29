import sys
from lupo.styling import *

if sys.platform == "win32":
    from .win32.win32_structs import *
    from ctypes import *
    from ctypes.wintypes import *
    import win32gui
    import win32con
    import win32api

if sys.platform == "darwin":
    from Cocoa import NSView, NSColor

from ..styling.applier import *

class View:
    children: list = []
    style = Style()
    parent_window = None

    def __init__(self, children: list = None, style: Style = None):
        self.children = children if children is not None else self.children

        if style is not None:
            self.style = style

    def get_win32_render(self, hwnd, hinst):
        for child in self.children:
            child.parent_window = self.parent_window

        rect = RECT()
        windll.user32.GetWindowRect(hwnd, pointer(rect))

        view_width = self.style.width if self.style.width is not None else rect.right - rect.left
        view_height = self.style.height if self.style.height is not None else rect.bottom - rect.top

        view_hwnd = windll.user32.CreateWindowExW(
            0,
            "Static",
            "",
            WS_CHILD,
            0, 0,
            view_width, view_height,
            hwnd,
            0,
            windll.user32.GetWindowLongPtrA(hwnd, hinst),
            0
        )

        self._hwnd = view_hwnd
        self._hinst = hinst

        apply_win32_hwnd_style(self._hwnd, self.style)

        return view_hwnd


    def show_win32_view(self):
        view_rect = RECT()
        windll.user32.GetWindowRect(self._hwnd, pointer(view_rect))

        view_width = self.style.width if self.style.width is not None else view_rect.right - view_rect.left
        view_height = self.style.height if self.style.height is not None else view_rect.bottom - view_rect.top

        for child in self.children:
            child_hwnd = child.get_win32_render(self._hwnd, self._hinst)

            c_rect = RECT()
            windll.user32.GetWindowRect(child_hwnd, pointer(c_rect))
            c_width = c_rect.right - c_rect.left
            c_height = c_rect.bottom - c_rect.top
            c_pos_x = int(view_width / 2 - c_width / 2)
            c_pos_y = int(view_height / 2 - c_height / 2)

            windll.user32.SetWindowPos(
                child_hwnd,
                0,
                c_pos_x,
                c_pos_y,
                c_width,
                c_height,
                0
            )

            child.show_win32_view()

        style = win32api.GetWindowLong(self._hwnd, win32con.GWL_STYLE)
        win32gui.SetWindowLong(self._hwnd, win32con.GWL_STYLE, (style | win32con.WS_VISIBLE))


    def get_osx_render(self, parent=None, superview = None):
        for child in self.children:
            child.parent_window = self.parent_window

        view_width = self.style.width if self.style.width is not None else superview.frame().size.width
        view_height = self.style.height if self.style.height is not None else superview.frame().size.height

        ns_view = NSView.alloc().initWithFrame_(((0, 0), (view_width, view_height)))

        apply_osx_view_style(ns_view, self.style)

        for child_object in self.children:
            ns_child = child_object.get_osx_render(parent=self, superview=ns_view)
            v_frame = ns_view.frame()
            c_frame = ns_child.frame()

            c_frame.origin.x = v_frame.size.width / 2 - c_frame.size.width / 2
            c_frame.origin.y = v_frame.size.height / 2 - c_frame.size.height / 2
            ns_child.setFrame_(c_frame)

            ns_view.addSubview_(ns_child)

        return ns_view
