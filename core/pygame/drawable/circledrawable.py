import pygame
from public.drawable import IDrawable


class CircleDrawable(IDrawable):
    def draw(self, screen, sprite):
        center_point = (int(sprite.position.x), int(sprite.position.y))
        pygame.draw.circle(screen, sprite.color, center_point, sprite.radius)
