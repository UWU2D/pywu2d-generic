from core.pygame.drawable.polygondrawable import PolygonDrawable
from core.pygame.sprite.sprite import Sprite

import pygame


class PolygonSprite2D(Sprite):
    def __init__(self, id, points=None, color="red", *args, **kwargs):
        super().__init__(id, color, *args, **kwargs)

        if points is None:
            points = []

        self.points = list(points)

    def maintain(self, dt):
        for i in range(len(self.points)):
            self.points[i] = (
                self.points[i][0] + self.velocity.x * dt,
                self.points[i][1] + self.velocity.y * dt,
            )

    def sync(self, data):
        super().sync(data)

        points = data["data"].get("points", [])
        self.points[:] = [(p["x"], p["y"]) for p in points]

    @property
    def drawable(self):
        return PolygonDrawable()
