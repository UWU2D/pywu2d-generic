
class IRenderService:

    @property
    def resolution(self):
        raise NotImplementedError("IRenderer.post needs to be implemented")

    def initialize(self):
        raise NotImplementedError(
            "IRenderService.initialize needs to be implemented")

    def stop(self):
        raise NotImplementedError(
            "IRenderService.stop needs to be implemented")

    def pre(self):
        raise NotImplementedError("IRenderer.pre needs to be implemented")

    def render(self, drawables):
        raise NotImplementedError("IRenderer.render needs to be implemented")

    def post(self):
        raise NotImplementedError("IRenderer.post needs to be implemented")
