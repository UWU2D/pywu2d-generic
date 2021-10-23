class IDrawable:

    def draw(self, render_service, sprite):
        raise NotImplementedError("IDrawable.draw needs to be implemented")
