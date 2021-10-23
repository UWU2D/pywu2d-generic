from .maintainable import IMaintainable


class IGameService(IMaintainable):

    def initialize(self, event_service, input_service, render_service, ui_service):
        raise NotImplementedError(
            "IGameService.initialize must be implemented")

    def stop(self):
        raise NotImplementedError("IGameService.stop must be implemented")

    @property
    def width(self):
        raise NotImplementedError("IGameService.width must be implemented")

    @property
    def height(self):
        raise NotImplementedError("IGameService.height must be implemented")

    @property
    def resolution(self):
        raise NotImplementedError("IGameService.width must be implemented")

    @property
    def height(self):
        raise NotImplementedError("IGameService.height must be implemented")

    @property
    def exit(self):
        raise NotImplementedError("IGameService.exit must be implemented")

    @property
    def sprites(self):
        raise NotImplementedError(
            "IGameService.get_drawables must be implemented")
