import ctypes
from ctypes import *
from ctypes.wintypes import *
import sys

WNDPROCTYPE = WINFUNCTYPE(c_int, HWND, c_uint, WPARAM, LPARAM)

WS_EX_APPWINDOW = 0x40000
WS_OVERLAPPEDWINDOW = 0xcf0000
WS_CAPTION = 0xc00000
WS_CHILD = 1073741824
WS_TABSTOP = 65536
WS_VISIBLE = 0x10000000

GWL_EXSTYLE = -20,
GWLP_HINSTANCE = -6,
GWLP_HWNDPARENT = -8,
GWL_ID = -12,
GWL_STYLE = -16,
GWL_USERDATA = -21,
GWL_WNDPROC = -4,
DWLP_USER = 0x8,
DWLP_MSGRESULT = 0x0,
DWLP_DLGPROC = 0x4

BS_DEFPUSHBUTTON = 1

SW_SHOWNORMAL = 1
SW_SHOW = 5

CS_HREDRAW = 2
CS_VREDRAW = 1

CW_USEDEFAULT = 0x80000000

WM_DESTROY = 2
WM_SETFONT = 0x0030

WHITE_BRUSH = 0


class WNDCLASSEX(Structure):
    _fields_ = [("cbSize", c_uint),
                ("style", c_uint),
                ("lpfnWndProc", WNDPROCTYPE),
                ("cbClsExtra", c_int),
                ("cbWndExtra", c_int),
                ("hInstance", HANDLE),
                ("hIcon", HANDLE),
                ("hCursor", HANDLE),
                ("hBrush", HANDLE),
                ("lpszMenuName", LPCWSTR),
                ("lpszClassName", LPCWSTR),
                ("hIconSm", HANDLE)]
