from .maintainable import IMaintainable


class ISprite(IMaintainable):

    @property
    def drawable(self):
        raise NotImplementedError(
            "ISprite.get_drawable needs to be implemented")

    def sync(self, json_data):
        raise NotImplementedError(
            "ISprite.sync needs to be implemented")
