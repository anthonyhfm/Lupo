import sys

if sys.platform == "darwin":
    from Cocoa import NSButton, NSComboBox


class LupoNSButton(NSButton):
    onclick = None


class LupoNSComboBox(NSComboBox):
    ...