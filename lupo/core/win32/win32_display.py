import ctypes

def get_display_size():
    user32 = ctypes.windll.user32
    width, height = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)

    return {
        "width": width,
        "height": height
    }
