import pygame
import pygame_gui
from public.uiservice import IUIService


class UI(IUIService):
    def __init__(self):
        self.ui_manager = None
        self.on_user_input = None

    def initialize(self, render_service, event_service):
        self.ui_manager = pygame_gui.UIManager(render_service.resolution)
        event_service.register_for_all(self.on_event)
        self.setup_server_window(event_service)

    def stop(self):
        return

    def pre(self):
        return

    def draw(self, render_service):
        self.ui_manager.draw_ui(render_service.screen)

    def post(self):
        return

    def maintain(self, dt):
        self.ui_manager.update(dt)

    def on_event(self, event):
        self.ui_manager.process_events(event)

    def setup_server_window(self, event_service):
        self.server_window = pygame_gui.elements.UIWindow(
            pygame.Rect(0, 0, 400, 300), self.ui_manager
        )

        self.server_url = pygame_gui.elements.UITextEntryLine(
            pygame.Rect(25, 50, 100, 300),
            self.ui_manager,
            self.server_window,
        )
        self.server_url.text = "ws://localhost:41234"

        self.connect_button = pygame_gui.elements.UIButton(
            pygame.Rect(100, 200, 100, 300),
            text="Click",
            manager=self.ui_manager,
            container=self.server_window,
        )

        event_service.register_event(
            pygame.USEREVENT, self.on_server_data_entry
        )

    def on_server_data_entry(self, event):
        if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.connect_button:
                self.on_user_input(self.server_url.text)

    def hide(self):
        self.server_window.kill()

    def show(self):
        self.server_window.show()
