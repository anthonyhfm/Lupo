from platform import platform
import sys
from .style import *
from .color import *

if sys.platform == "darwin":
    from Cocoa import NSView, NSColor

if sys.platform == "win32":
    import win32gui
    import win32api
    import win32con


def apply_win32_hwnd_style(hwnd, style: Style):
    s = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, s | win32con.WS_EX_LAYERED)
    win32gui.SetLayeredWindowAttributes(hwnd, 0, int(style.opacity * 255), win32con.LWA_ALPHA)


def apply_osx_view_style(ns_view, style: Style):
    ns_view: NSView
    if style.background_color is not None:
        view_color = style.background_color.get_rgb_value()
        ns_view.setBackgroundColor_(
            NSColor.colorWithRed_green_blue_alpha_(view_color[0] / 255, view_color[1] / 255, view_color[2] / 255, 1.0))