
class IServiceFactory:

    def render_service(self):
        raise NotImplementedError(
            "IServiceFactory.render_service needs to be implemented")

    def ui_service(self):
        raise NotImplementedError(
            "IServiceFactory.ui_service needs to be implemented")

    def input_service(self):
        raise NotImplementedError(
            "IServiceFactory.input_service needs to be implemented")

    def event_service(self):
        raise NotImplementedError(
            "IServiceFactory.event_service needs to be implemented")

    def game_service(self):
        raise NotImplementedError(
            "IServiceFactory.game_service needs to be implemented")
