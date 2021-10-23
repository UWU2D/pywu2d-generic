from public.servicefactory import IServiceFactory

from core.pygame.services import renderservice, inputservice, eventservice
import uwu2dgeneric.client as client
import ui


class ServiceFactory(IServiceFactory):
    def render_service(self):
        return renderservice.RenderService()

    def ui_service(self):
        return ui.UI()

    def input_service(self):
        return inputservice.InputService()

    def event_service(self):
        return eventservice.EventService()

    def game_service(self):
        return client.Client(1920, 1080)
