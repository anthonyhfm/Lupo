import ctypes
from ctypes import *
from ctypes.wintypes import *
import sys

if sys.platform == "win32":
    from .win32_structs import *
    from .win32_display import get_display_size


class WIN32_WINDOW:
    title = "Lupo Window"
    window_x = 0
    window_y = 0
    window_width = 250
    window_height = 250

    def py_wnd_procedure(self, hWnd, Msg, wParam, lParam):
        if Msg == WM_DESTROY:
            self.user32.PostQuitMessage(0)
            return 0
        return self.user32.DefWindowProcW(hWnd, Msg, wParam, lParam)

    def __init__(self):
        self.user32 = ctypes.WinDLL('user32', use_last_error=True)
        self.user32.DefWindowProcW.argtypes = [HWND, c_uint, WPARAM, LPARAM]

        self.WndProc = WNDPROCTYPE(self.py_wnd_procedure)
        self.hInst = windll.kernel32.GetModuleHandleW(0)
        self.wndClass = WNDCLASSEX()
        self.wndClass.cbSize = sizeof(WNDCLASSEX)
        self.wndClass.style = CS_HREDRAW | CS_VREDRAW
        self.wndClass.lpfnWndProc = self.WndProc
        self.wndClass.cbClsExtra = 0
        self.wndClass.cbWndExtra = 0
        self.wndClass.hInstance = self.hInst
        self.wndClass.hIcon = 0
        self.wndClass.hCursor = 0
        self.wndClass.hBrush = windll.gdi32.GetStockObject(WHITE_BRUSH)
        self.wndClass.lpszMenuName = 0
        self.wndClass.lpszClassName = self.title
        self.wndClass.hIconSm = 0

        self.regRes = windll.user32.RegisterClassExW(byref(self.wndClass))

        display_size = get_display_size()

        self.hWnd = windll.user32.CreateWindowExW(
            0,
            self.title,
            self.title,
            WS_OVERLAPPEDWINDOW | WS_CAPTION,
            int(display_size["width"] / 2 - self.window_width / 2),
            int(display_size["height"] / 2 - self.window_height / 2),
            self.window_width, self.window_height,
            0,
            0,
            self.hInst,
            0
        )

    def get_hwnd(self):
        return self.hWnd

    def get_hinst(self):
        return self.hInst

    def set_size(self, width, height):
        rect = RECT()
        windll.user32.GetWindowRect(self.hWnd, pointer(rect))
        self.window_width = width
        self.window_height = height

        windll.user32.MoveWindow(self.hWnd, rect.left, rect.top, width, height, 0)

        rect_client = RECT()
        windll.user32.GetClientRect(self.hWnd, pointer(rect_client))

        diffX = width - (rect_client.right - rect_client.left)
        diffY = height - (rect_client.bottom - rect_client.top)
        windll.user32.MoveWindow(self.hWnd, rect.left, rect.top, width + diffX, height + diffY, 0)

    def set_title(self, title):
        self.title = title
        windll.user32.SetWindowTextW(self.hWnd, self.title)

    def display_window(self):
        if not self.hWnd:
            print('Failed to create window')
            exit(0)

        windll.user32.ShowWindow(self.hWnd, SW_SHOW)
        windll.user32.UpdateWindow(self.hWnd)

        msg = MSG()
        lpmsg = pointer(msg)

        while windll.user32.GetMessageA(lpmsg, 0, 0, 0) != 0:
            windll.user32.TranslateMessage(lpmsg)
            windll.user32.DispatchMessageA(lpmsg)