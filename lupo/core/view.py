import sys
from .style import Style

if sys.platform == "darwin":
    from Cocoa import NSView


class View:
    children: list = []
    style = Style()

    def __init__(self, children: list = None, style: Style = None):
        self.children = children

        if style is not None:
            self.style = style

    def get_osx_render(self, parent=None, superview: NSView = None):
        view_width = 0
        view_height = 0

        if self.style.width is not None:
            view_width = self.style.width
        else:
            view_width = superview.frame().size.width

        if self.style.height is not None:
            view_height = self.style.height
        else:
            view_height = superview.frame().size.height

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
