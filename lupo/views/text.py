from ..core.view import View
from ..core.style import Style
import sys

if sys.platform == "darwin":
    from Cocoa import NSTextField

class Text(View):
    text: str = ""

    def __init__(self, text: str, style: Style = None):
        super().__init__(style=style)
        self.text = text

    def get_osx_render(self, parent=None, superview = None):
        parent: View

        t = NSTextField.alloc().initWithFrame_(((0, 0), (0, 0)))
        t.setStringValue_(self.text)
        t.setBackgroundColor_(None)
        t.setBezeled_(False)
        t.setEditable_(False)
        t.sizeToFit()

        return t