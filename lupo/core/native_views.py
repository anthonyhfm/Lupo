from .view import View
import sys

if sys.platform == "darwin":
    from Cocoa import NSView
    from Cocoa import NSButton


class Button(View):
    text: str

    def __init__(self, text: str):
        super().__init__()
        self.text = text

    def get_osx_render(self, parent=None, superview: NSView = None):
        b = NSButton.alloc().initWithFrame_(((0, 0), (0, 0)))
        b.setBezelStyle_(4)
        b.setTitle_(self.text)
        b.sizeToFit()
        return b
