from drawable.polygondrawable import PolygonDrawable
import sprite.sprite as sprite

import pygame


class PolygonSprite2D(sprite.Sprite):
    def __init__(self, id, points=None, color="red", *args, **kwargs):

        if color is not None and isinstance(color, str):
            color = pygame.Color(color)

        if points is None:
            points = []

        self.color = color

        self.points = list(points)

        super().__init__(id, *args, **kwargs)

    def tick(self, dt):
        super().tick(dt)

        for i in range(len(self.points)):
            self.points[i] = (
                self.points[i][0] + self.x_velocity * dt,
                self.points[i][1] + self.y_velocity * dt,
            )

    def get_drawable(self):
        return PolygonDrawable()

    def sync(self, info):
        super().sync(info)

        points = info["data"].get("points", [])
        self.points[:] = [(p["x"], p["y"]) for p in points]
