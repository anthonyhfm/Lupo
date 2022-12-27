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

        self.style = style if style is not None else Style()

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
