
from public.maintainable import IMaintainable


class IUIService(IMaintainable):

    def initialize(self, render_service, event_service):
        raise NotImplementedError(
            "IUIService.initialize needs to be implemented")

    def stop(self):
        raise NotImplementedError(
            "IUIService.stop needs to be implemented")

    def pre(self):
        raise NotImplementedError("IUIService.pre needs to be implemented")

    def draw(self):
        raise NotImplementedError("IUIService.draw needs to be implemented")

    def post(self):
        raise NotImplementedError("IUIService.post needs to be implemented")
