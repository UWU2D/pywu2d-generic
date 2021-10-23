class IInputService:
    def __init__(self):
        pass

    def initialize(self, event_service):
        raise NotImplementedError(
            "IInputService.initialize needs to be implemented")

    def register_key_event(self, key_code, callback):
        raise NotImplementedError(
            "IInputService.register_key_event needs to be implemented")

    def register_mouse_motion(self, callback):
        raise NotImplementedError(
            "IInputService.register_mouse_motion needs to be implemented")

    def register_mouse_click(self, callback):
        raise NotImplementedError(
            "IInputService.register_mouse_click needs to be implemented")
