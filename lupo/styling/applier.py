import sys
from .style import *
from .color import *

if sys.platform == "darwin":
    from Cocoa import NSView, NSColor


def apply_osx_view_style(ns_view: NSView, style: Style):
    if style.background_color is not None:
        view_color = style.background_color.get_rgb_value()
        ns_view.setBackgroundColor_(
            NSColor.colorWithRed_green_blue_alpha_(view_color[0] / 255, view_color[1] / 255, view_color[2] / 255, 1.0))