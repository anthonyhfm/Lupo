from enum import Enum


class NSWindowStyleMask(Enum):
    NSWindowStyleMaskBorderless = 0
    NSWindowStyleMaskTitled = 1 << 0
    NSWindowStyleMaskClosable = 1 << 1
    NSWindowStyleMaskMiniaturizable = 1 << 2
    NSWindowStyleMaskResizable = 1 << 3