from .color import Color

class px(int):  # px type from CSS but instead of writing 100px you use px(100)
    value: int

    def __init__(self, number):
        self.value = number

    def __int__(self) -> int:
        return self.value


class Style:
    width: int = None
    height: int = None
    gap: int = None
    background_color: Color = None

    def __init__(
            self,
            width: int = None,
            height: int = None,
            gap: int = None,
            background_color: Color = None
    ):
        self.width = width if not None else self.width
        self.height = height if not None else self.height
        self.gap = gap if not None else self.gap
        self.background_color = background_color if not None else self.background_color
