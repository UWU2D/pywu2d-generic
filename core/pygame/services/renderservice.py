import pygame
from public.renderservice import IRenderService


class RenderService(IRenderService):

    @property
    def resolution(self):
        return self.__resolution

    @property
    def screen(self):
        return pygame.display.get_surface()

    def initialize(self, resolution):
        self.__resolution = resolution
        pygame.init()
        pygame.font.init()

        pygame.display.set_mode(resolution)

    def stop(self):
        pygame.display.quit()

    def pre(self):
        pygame.display.get_surface().fill((0, 0, 0))

    def render(self, sprites):
        for sprite in sprites:
            if sprite.drawable is not None:
                sprite.drawable.draw(pygame.display.get_surface(), sprite)

    def post(self):
        pygame.display.flip()
