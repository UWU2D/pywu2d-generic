
from public.maintainable import IMaintainable


class IEventService(IMaintainable):
    def register(self, event, callback):
        raise NotImplementedError(
            "IEventService.register needs to be implemented")

    def register_for_all(self, callback):
        raise NotImplementedError(
            "IEventService.register_for_all needs to be implemented")

    def register_quit(self, callback):
        raise NotImplementedError(
            "IEventService.register_quit needs to be implemented")
