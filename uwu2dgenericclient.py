import pygame
import pygame_gui

from pywu2dclient import PyWU2DClient
from sprite.circlesprite import CircleSprite
from sprite.polygonsprite2d import PolygonSprite2D

from keymap import KEY_STRING_TO_PYGAME_KEY_MAP, PYGAME_KEY_TO_KEY_STRING_MAP


def create():
    # return UWUDP4Client(host="127.0.0.1")
    return UWU2DGenericClient()


class UWU2DGenericClient(PyWU2DClient):

    def __init__(self, width=1920, height=1080):
        super().__init__(width, height)

        self.server_window = None
        self.sprites = {}

    def on_load(self, game_service):
        super().on_load(game_service)
        game_service.ui_manager = pygame_gui.UIManager(
            game_service.screen_size)
        game_service.event_manager.register_for_all(self.on_event)

    def on_event(self, event):
        self.game_service.ui_manager.process_events(event)

    def on_connect(self, s):
        super().on_connect(s)
        self.server_window.kill()

    def on_disconnect(self):
        super().on_disconnect()
        self.server_window.show()

    def post_render(self):
        self.game_service.ui_manager.draw_ui(self.game_service.screen)
        super().post_render()

    def process(self, dt):
        super().process(dt)

        for sprite in self.sprites.values():
            sprite.tick(dt)

    def render(self):
        for sprite in self.sprites.values():
            if sprite.drawable is not None:
                sprite.drawable.draw(pygame.display.get_surface(), sprite)

    def on_close(self, game_service):
        super().on_close(game_service)

    def on_read(self, socket, message):
        super().on_read(socket, message)

        type = message["type"]
        data = message["data"]

        if type == "game":
            self.on_game(data)
        if type == "state":
            self.on_state(data)
        if type == "input":
            self.on_input_setup(data)

    def on_game(self, message):
        self.sync_entities(message)

    def on_state(self, message):
        return

    def sync_entities(self, game_objects):
        for game_object in game_objects:
            self.sync_entity(game_object)

    def sync_entity(self, game_object):
        id = game_object["id"]
        type = game_object["data"]["shape"]

        # we have not encountered this sprite yet
        if id not in self.sprites:
            # create it based on the types we know
            if type == "circle":
                self.sprites[id] = CircleSprite(id=id)
            elif type == "polygon":
                self.sprites[id] = PolygonSprite2D(id=id)
            else:
                print("Unknown sprite type: " + type)
                return

        if game_object["state"] == "deleted":
            self.destroy(id)
        else:
            # Update the info
            self.sprites[id].sync(game_object)

    def on_input_setup(self, message):

        if "keys" in message:
            self.register_keys(message["keys"])
        if "mouse" in message:
            self.register_mouse(message["mouse"])

    def register_mouse(self, mouse):
        if "motion" in mouse:
            self.register_mouse_motion()
        if "click" in mouse:
            self.register_mouse_click()

    def register_mouse_motion(self):
        self.game_service.input_service.register_mouse_motion(
            self.on_mouse_motion)

    def register_mouse_click(self):
        self.game_service.input_service.register_mouse_click(
            self.on_mouse_click)

    def register_keys(self, keys):

        for game_key, pygame_keys in keys.items():
            for pygame_key in pygame_keys:
                key = KEY_STRING_TO_PYGAME_KEY_MAP[pygame_key]
                self.register_key(game_key, key)

    def register_key(self, game_key, pygame_key):
        self.game_service.input_service.register_key_event(
            pygame_key,
            lambda key, pressed, game_key=game_key: self.on_key_press(
                game_key, key, pressed
            ),
        )

    def on_key_press(self, game_key, pygame_key, pressed):
        self.send_message(
            "game",
            {
                "type": "keyPress",
                "key": game_key,
                "pressed": pressed,
            },
        )

    def on_mouse_motion(self, x, y):
        self.send_message("game", {"type": "mouse", "x": x, "y": y})

    def on_mouse_click(self, x, y, button, pressed):
        if button == pygame.BUTTON_LEFT:
            button == "leftClick"
        elif button == pygame.BUTTON_RIGHT:
            button == "rightClick"
        elif button == pygame.BUTTON_MIDDLE:
            button == "middleClick"

        self.send_message(
            "game",
            {"type": "click", "x": x, "y": y, "button": button, "pressed": pressed},
        )

    def on_ui(self, dt):
        super().on_ui(dt)

        self.game_service.ui_manager.update(dt)

        if self.wait_for_user_input:
            if self.server_window is None:
                self.setup_server_window()

    def setup_server_window(self):
        self.server_window = pygame_gui.elements.UIWindow(
            pygame.Rect(0, 0, 400, 300), self.game_service.ui_manager
        )

        self.server_url = pygame_gui.elements.UITextEntryLine(
            pygame.Rect(25, 50, 100, 300),
            self.game_service.ui_manager,
            self.server_window,
        )
        self.server_url.text = "ws://localhost:41234"

        self.connect_button = pygame_gui.elements.UIButton(
            pygame.Rect(100, 200, 100, 300),
            text="Click",
            manager=self.game_service.ui_manager,
            container=self.server_window,
        )

        self.game_service.event_manager.register_event(
            pygame.USEREVENT, self.on_server_data_entry
        )

    def on_server_data_entry(self, event):
        if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.connect_button:
                self.try_connect(self.server_url.text)

    def sync_entities(self, game_objects):
        for game_object in game_objects:
            self.sync_entity(game_object)

    def sync_entity(self, game_object):
        id = game_object["id"]
        type = game_object["data"]["shape"]

        # we have not encountered this sprite yet
        if id not in self.sprites:
            # create it based on the types we know
            if type == "circle":
                self.sprites[id] = CircleSprite(id=id)
            elif type == "polygon":
                self.sprites[id] = PolygonSprite2D(id=id)
            else:
                print("Unknown sprite type: " + type)
                return

        if game_object["state"] == "deleted":
            self.destroy(id)
        else:
            # Update the info
            self.sprites[id].sync(game_object)

    def instantiate(self, type, debug_name, *args, **kwargs):

        id = self.next_id
        self.next_id += 1
        self.sprites[id] = type(id, debug_name=debug_name, *args, **kwargs)

        return self.sprites[id]

    def destroy_all_entities(self):
        print("Destroying entities")
        self.sprites.clear()

    def destroy(self, id):
        if id in self.sprites:
            del self.sprites[id]
