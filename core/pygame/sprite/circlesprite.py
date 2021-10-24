import pygame

from core.vector2d import Vector2D
from core.pygame.sprite.sprite import Sprite
from core.pygame.drawable.circledrawable import CircleDrawable


class CircleSprite(Sprite):
    def __init__(self, id, position=None, radius=1, color="red", *args, **kwargs):
        super().__init__(id, color, *args, **kwargs)

        if position is None:
            position = Vector2D(0, 0)

        self.position = position

        self.radius = radius

    def maintain(self, dt):
        self.position.x += self.velocity.x * dt
        self.position.y += self.velocity.y * dt

    def set_radius(self, radius):
        self.radius = radius
        self.dirty = True

    def sync(self, message):
        super().sync(message)

        self.position.x = message.get("x", self.position.x)
        self.position.y = message.get("y", self.position.y)

        data = message["data"]
        self.radius = data.get("radius", self.radius)

    @ property
    def drawable(self):
        return CircleDrawable()
