from ..core.view import View
import sys

if sys.platform == "darwin":
    from Cocoa import NSView, NSColor

if sys.platform == "win32":
    from ..core.win32.win32_structs import *
    from ctypes import *
    from ctypes.wintypes import *
    import win32api
    import win32con
    import win32gui

from ..styling.applier import *

class Column(View):
    def get_win32_render(self, hwnd, hinst):
        for child in self.children:
            child.parent_window = self.parent_window

        rect = RECT()
        windll.user32.GetWindowRect(hwnd, pointer(rect))

        self._view_width = self.style.width if self.style.width is not None else rect.right - rect.left
        self._view_height = self.style.height if self.style.height is not None else rect.bottom - rect.top

        view_hwnd = windll.user32.CreateWindowExW(
            0,
            "Static",
            "",
            WS_CHILD,
            0, 0,
            self._view_width, self._view_height,
            hwnd,
            0,
            windll.user32.GetWindowLongPtrA(hwnd, hinst),
            0
        )

        self._hwnd = view_hwnd
        self._hinst = hinst

        self._child_hwnds = [child.get_win32_render(self._hwnd, self._hinst) for child in self.children]

        calculated_height = 0
        for hwnd in self._child_hwnds:
            rect = RECT()
            windll.user32.GetWindowRect(hwnd, pointer(rect))
            calculated_height += rect.bottom - rect.top

        calculated_height += self.style.gap * (len(self.children) - 1) if self.style.gap is not None else 0

        self._view_height = calculated_height if self.style.height is None else self._view_height

        if self.style.height is None:
            windll.user32.SetWindowPos(
                self._hwnd,
                0,
                0, 0,
                self._view_width, self._view_height,
                0
            )

        apply_win32_hwnd_style(self._hwnd, self.style)

        return view_hwnd


    def show_win32_view(self):
        view_rect = RECT()
        windll.user32.GetWindowRect(self._hwnd, pointer(view_rect))

        calculated_height = 0
        for hwnd in self._child_hwnds:
            rect = RECT()
            windll.user32.GetWindowRect(hwnd, pointer(rect))
            calculated_height += rect.bottom - rect.top

        calculated_height += self.style.gap * (len(self.children) - 1) if self.style.gap is not None else 0

        for child in self.children:
            child_hwnd = child.get_win32_render(self._hwnd, self._hinst)
            c_index = self.children.index(child)

            # Get Child Size to calculate new x and y position inside of this element
            c_rect = RECT()
            windll.user32.GetWindowRect(child_hwnd, pointer(c_rect))
            c_width = c_rect.right - c_rect.left
            c_height = c_rect.bottom - c_rect.top

            c_pos_x = int(self._view_width / 2 - c_width / 2)
            c_pos_y = int(self._view_height / 2 - calculated_height / 2 + (c_index * c_height + c_index * self.style.gap))

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
        parent: View = parent
        self.children.reverse()
        for child in self.children:
            child.parent_window = self.parent_window

        ns_view = NSView.alloc().initWithFrame_(((0, 0), (0, 0)))

        apply_osx_view_style(ns_view, self.style)

        children_osx_renders = [child.get_osx_render(parent=self, superview=ns_view) for child in self.children]

        def max_width_key(key):
            return key.frame().size.width

        width = self.style.width if self.style.width is not None else max(children_osx_renders, key=max_width_key).frame().size.width
        height = 0

        for child_object in children_osx_renders:
            height += child_object.frame().size.height

        height += self.style.gap * (len(self.children) - 1) if self.style.gap is not None else 0

        ns_view_frame = ns_view.frame()
        ns_view_frame.size.height = height
        ns_view_frame.size.width = width

        for child_object in self.children:
            ns_child = child_object.get_osx_render(parent=self, superview=ns_view)
            child_frame = ns_child.frame()
            point_y = 0

            index = self.children.index(child_object)
            for i in range(index):
                point_y += self.children[i].get_osx_render(parent=self, superview=ns_view).frame().size.height

            point_y += self.style.gap * index
            child_frame.origin.y = point_y
            child_frame.origin.x = ns_view_frame.size.width / 2 - child_frame.size.width / 2

            ns_child.setFrame_(child_frame)
            ns_view.addSubview_(ns_child)

        ns_view.setFrame_(ns_view_frame)
        return ns_view