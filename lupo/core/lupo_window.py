import os
import platform
from .osx.osx_window_manager import OSX_OBJC_WINDOW
from .view import View

class Window:
    __title = "Lupo Window"
    body: View

    def __init__(self):
        ...

    def open(self):
        if platform.system() == "Darwin":
            osx_window = OSX_OBJC_WINDOW(self.body)
            osx_window.set_title(self.__title)
            osx_window.display_window()