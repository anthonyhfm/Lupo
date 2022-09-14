import sys
from .style import Style

if sys.platform == "win32":
    from .win32.win32_structs import *
    import ctypes
    from ctypes import *
    from ctypes.wintypes import *

if sys.platform == "darwin":
    from Cocoa import NSView


class View:
    children: list = []
    style = Style()
    parent_window = None

    def __init__(self, children: list = None, style: Style = None):
        self.children = children

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
            WS_CHILD | WS_VISIBLE,  # BS_GROUPBOX would prob. be the right element style
            0, 0,
            view_width, view_height,
            hwnd,
            0,
            windll.user32.GetWindowLongPtrA(hwnd, hinst),
            0
        )

        for child in self.children:
            c_hwnd = child.get_win32_render(view_hwnd, hinst)
            c_rect = RECT()
            windll.user32.GetWindowRect(c_hwnd, pointer(c_rect))
            c_width = c_rect.right - c_rect.left
            c_height = c_rect.bottom - c_rect.top

            windll.user32.SetWindowPos(
                c_hwnd,
                0,
                int(view_width / 2 - c_width / 2),
                int(view_height / 2 - c_height / 2),
                100,
                100,
                1
            )


        return view_hwnd

    def get_osx_render(self, parent=None, superview = None):
        for child in self.children:
            child.parent_window = self.parent_window

        view_width = self.style.width if self.style.width is not None else superview.frame().size.width
        view_height = self.style.height if self.style.height is not None else superview.frame().size.height

        ns_view = NSView.alloc().initWithFrame_(((0, 0), (view_width, view_height)))

        for child_object in self.children:
            ns_child = child_object.get_osx_render(parent=self, superview=ns_view)
            v_frame = ns_view.frame()
            c_frame = ns_child.frame()

            c_frame.origin.x = v_frame.size.width / 2 - c_frame.size.width / 2
            c_frame.origin.y = v_frame.size.height / 2 - c_frame.size.height / 2
            ns_child.setFrame_(c_frame)

            ns_view.addSubview_(ns_child)

        return ns_view
