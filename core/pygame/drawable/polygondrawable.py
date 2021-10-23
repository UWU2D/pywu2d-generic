import pygame
from public.drawable import IDrawable


class PolygonDrawable(IDrawable):
    def draw(self, screen, sprite):
        pygame.draw.polygon(screen, sprite.color, sprite.points)
