import pygame

from core.vector2d import Vector2D
from public.sprite import ISprite


class Sprite(ISprite):
    def __init__(self, id, position=None, color="red", *args, **kwargs):
        self.id = id

        self.velocity = Vector2D(0, 0)
        self.acceleration = Vector2D(0, 0)

        if color is not None and isinstance(color, str):
            color = pygame.Color(color)
        self.color = pygame.Color(color)

    def sync(self, data):

        data = data["data"]

        if "rgba" in data:
            rgba = data["rgba"]
            self.color = pygame.color.Color(
                rgba[0], rgba[1], rgba[2], rgba[3] * 255)
        elif "color" in data:
            self.color = data["color"]

        self.velocity.x = data.get("xVelocity", self.velocity.x)
        self.velocity.y = data.get("yVelocity", self.velocity.y)
        self.acceleration.x = data.get("yAcceleration", self.acceleration.x)
        self.acceleration.y = data.get("xAcceleration", self.acceleration.y)
