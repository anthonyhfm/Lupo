import sys

if sys.platform == "darwin":
    from Cocoa import NSButton


class LupoNSButton(NSButton):
    onclick = None