import pygame
import pygame_gui
from public.uiservice import IUIService


class UI(IUIService):
    def __init__(self):
        self.ui_manager = None
        self.on_user_input = None

    def initialize(self, render_service, event_service):
        self.render_service = render_service
        self.event_service = event_service

        self.ui_manager = pygame_gui.UIManager(render_service.resolution)
        event_service.register_for_all(self.on_event)
        self.setup_server_window()

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

    def setup_server_window(self):
        width, height = self.render_service.resolution

        window_width = 400
        window_height = 300

        self.server_window = pygame_gui.elements.UIWindow(
            pygame.Rect(width/2 - window_width/2, height/2-window_height/2, window_width, window_height), self.ui_manager, window_display_title="Server Connection", visible=True
        )

        box_height = 50
        self.server_url = pygame_gui.elements.UITextEntryLine(
            pygame.Rect(0, window_height/2-box_height /
                        2, window_width, box_height),
            self.ui_manager,
            self.server_window,
        )
        self.server_url.set_text("ws://localhost:41234")

        button_width = 100
        button_height = 50
        self.connect_button = pygame_gui.elements.UIButton(
            pygame.Rect(window_width/2 - button_width/2,
                        window_height-100, button_width, button_height),
            text="Connect",
            manager=self.ui_manager,
            container=self.server_window,
        )

        self.event_service.register_event(
            pygame.USEREVENT, self.on_user_event
        )

    def on_user_event(self, event):
        if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.connect_button:
                self.on_user_input(self.server_url.text)

    def hide(self):
        self.server_window.hide()

    def show(self):
        self.server_window.show()
