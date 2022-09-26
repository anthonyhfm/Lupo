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

        text_element = NSTextField.alloc().initWithFrame_(((0, 0), (0, 0)))
        text_element.setStringValue_(self.text)
        text_element.setBackgroundColor_(None)
        text_element.setBezeled_(False)
        text_element.setEditable_(False)
        text_element.sizeToFit()

        return text_element