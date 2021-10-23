
from public.screenservice import IScreenService


class ScreenService(IScreenService):

    def __init__(self, screen, size):
        self.screen = screen
        self.size = size

    @property
    def size(self):
        return self.size

    @property
    def x_size(self):
        return self.size[0]

    @property
    def y_size(self):
        return self.size[1]
