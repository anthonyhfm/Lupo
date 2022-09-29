import os
from .osx.osx_window_manager import OSX_OBJC_WINDOW
from .win32.win32_window_manager import WIN32_WINDOW
from .view import View
import sys


class Window:
    __title = "Lupo Window"
    body = View()
    __size = (300, 300)

    def __init__(self):
        if sys.platform == "darwin":
            self.osx_window = OSX_OBJC_WINDOW()
        elif sys.platform == "win32":
            self.win32_window = WIN32_WINDOW()

    def set_size(self, width: int, height: int):
        self.__size = (width, height)
        if sys.platform == "darwin":
            self.osx_window.set_size(self.__size[0], self.__size[1])
        elif sys.platform == "win32":
            self.win32_window.set_size(self.__size[0], self.__size[1])

    def get_size(self):
        return self.__size

    def set_resizable(self, resizeable):
        if sys.platform == "darwin":
            self.osx_window.set_resizable(resizeable)

    def set_title(self, title: str):
        self.__title = title

        if sys.platform == "darwin":
            self.osx_window.set_title(self.__title)
        elif sys.platform == "win32":
            self.win32_window.set_title(self.__title)

    def open(self):
        self.body.style.width = self.__size[0]
        self.body.style.height = self.__size[1]
        self.body.parent_window = self

        if sys.platform == "darwin":
            self.osx_window.set_body(self.body.get_osx_render(superview=self.osx_window.win.contentView()))
            self.osx_window.set_title(self.__title)
            self.osx_window.display_window()

        elif sys.platform == "win32":
            window_hwnd = self.win32_window.get_hwnd()
            window_hinst = self.win32_window.get_hinst()
            self.body.get_win32_render(window_hwnd, window_hinst)
            self.body.show_win32_view()
            self.win32_window.display_window()