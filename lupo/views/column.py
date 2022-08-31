from ..core.view import View
import sys
from ..core.style import Style

if sys.platform == "darwin":
    from Cocoa import NSView


class Column(View):
    def get_osx_render(self, parent=None, superview: NSView = None):
        parent: View = parent
        self.children.reverse()

        height = 0
        for child_object in self.children:
            ns_child = child_object.get_osx_render()
            height += ns_child.frame().size.height

        if self.style.gap is not None:
            height += self.style.gap * (len(self.children) - 1)

        ns_view = NSView.alloc().initWithFrame_(((0, 0), (superview.frame().size.width, height)))

        ns_view_frame = ns_view.frame()

        for child_object in self.children:
            ns_child = child_object.get_osx_render()
            child_frame = ns_child.frame()
            point_y = 0

            index = self.children.index(child_object)
            for i in range(index):
                point_y += self.children[i].get_osx_render().frame().size.height

            point_y += self.style.gap * index
            child_frame.origin.y = point_y
            child_frame.origin.x = ns_view_frame.size.width / 2 - child_frame.size.width / 2

            ns_child.setFrame_(child_frame)
            ns_view.addSubview_(ns_child)

        return ns_view