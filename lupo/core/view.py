class View:
    children: list = []

    def __init__(self, children=None):
        self.children = children

    def get_osx_render(self):
        pass
