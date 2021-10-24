import pygame

import uuid

from core.timer import Timer

from public.gameservice import IGameService
from public.uiservice import IUIService

from pywu2dclient import UWU2DService
from pywu2dclient.public.messagehandler import IMessageHandler
from pywu2dclient.core.network.websocketclient import WebsocketClient

from core.pygame.sprite.circlesprite import CircleSprite
from core.pygame.sprite.polygonsprite2d import PolygonSprite2D
from core.pygame.keymap import KEY_STRING_TO_PYGAME_KEY_MAP


def create():
    return Client(1920, 1080)


class Client(IGameService, IMessageHandler):

    def __init__(self, width, height):

        self.__width = width
        self.__height = height
        self.uwu_service = None

        self.__sprites = {}

        self.input_service = None
        self.ui_service = None
        self.should_exit = False

        self.try_to_connect = False
        self.connection_url = None
        self.connection_timer = Timer(5000)

    '''
    IGameService Implementation
    '''

    def initialize(self, event_service, input_service, render_service, ui_service):
        self.input_service = input_service
        self.ui_service = ui_service
        self.ui_service.on_try_connect = self.on_try_connect

    def stop(self):
        if self.uwu_service:
            self.uwu_service.stop()
            self.uwu_service = None

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def resolution(self):
        return (self.width, self.height)

    @property
    def exit(self):
        return self.should_exit

    @property
    def sprites(self):
        return self.__sprites.values()

    def maintain(self, dt):

        if self.try_to_connect:
            if self.uwu_service == None:
                self.uwu_service = UWU2DService(
                    WebsocketClient(self.connection_url), self)

            if self.uwu_service.is_connected():
                self.try_to_connect = False
            elif self.connection_timer.is_elapsed():
                self.try_to_connect = False
                self.stop()
                self.ui_service.show()

        if self.uwu_service is not None:
            self.uwu_service.maintain()

        for sprite in self.__sprites.values():
            sprite.maintain(dt)

    def on_try_connect(self, text):
        self.try_to_connect = True
        self.connection_url = text
        self.connection_timer.reset()
        self.ui_service.hide()

    '''
    IMessageHandler Implementation
    '''

    def on_connect(self):
        print("on_connect")
        self.ui_service.hide()

    def on_disconnect(self):
        print("on_disconnect")
        self.destroy_all_entities()
        self.stop()
        self.ui_service.show()

    def on_read(self, type, id, data):

        if type == "game":
            self.on_game(data)
        if type == "state":
            self.on_state(data)

    def on_handshake(self, clientId):
        print("on_handshake, clientId: " + clientId)

    def on_client_config(self, config):
        self.on_input_setup(config)

    '''
    Generic message handling stuff
    '''

    def on_game(self, message):
        self.sync_entities(message)

    def on_state(self, message):
        return

    def on_input_setup(self, message):

        message = message['input']

        for type in message['types']:
            if type == 'click':
                self.register_mouse_click()
            elif type == 'mouse':
                self.register_mouse_motion()

        if "keyMappings" in message:
            self.register_keys(message["keyMappings"])

    '''
    Entity Syncing
    '''

    def sync_entities(self, game_objects):
        for game_object in game_objects:
            self.sync_entity(game_object)

    def sync_entity(self, game_object):
        id = game_object["id"]
        

        # we have not encountered this sprite yet
        if id not in self.__sprites:
            type = game_object["data"]["shape"]
            # create it based on the types we know
            if type == "circle":
                self.__sprites[id] = CircleSprite(id=id)
            elif type == "polygon":
                self.__sprites[id] = PolygonSprite2D(id=id)
            else:
                print("Unknown sprite type: " + type)
                return

        if "state" in game_object and game_object["state"] == "deleted":
            self.destroy(id)
        else:
            # Update the info
            self.__sprites[id].sync(game_object)

    def instantiate(self, type, debug_name, *args, **kwargs):
        id = uuid.uuid4()
        self.__sprites[id] = type(id, debug_name=debug_name, *args, **kwargs)
        return self.__sprites[id]

    def destroy_all_entities(self):
        print("Destroying entities")
        self.__sprites.clear()

    def destroy(self, id):
        if id in self.__sprites:
            del self.__sprites[id]

    '''
    Generic input registration
    '''

    def register_mouse_motion(self):
        self.input_service.register_mouse_motion(
            self.on_mouse_motion)

    def register_mouse_click(self):
        self.input_service.register_mouse_click(
            self.on_mouse_click)

    def register_keys(self, keys):

        # for game_key, pygame_keys in keys.items():
        #     for pygame_key in pygame_keys:
        #         key = KEY_STRING_TO_PYGAME_KEY_MAP[pygame_key]
        #         self.register_key(game_key, key)

        for key_tuple in keys:
            key, reported_key = key_tuple
            if key not in KEY_STRING_TO_PYGAME_KEY_MAP:
                print("Unknown requested key " + key)
                continue

            pygame_key_id = KEY_STRING_TO_PYGAME_KEY_MAP[key]
            self.register_key(reported_key, pygame_key_id)

    def register_key(self, game_key, pygame_key):
        self.input_service.register_key_event(
            pygame_key,
            lambda key, pressed, game_key=game_key: self.on_key_press(
                game_key, key, pressed
            ),
        )

    def on_key_press(self, game_key, pygame_key, pressed):
        self.uwu_service.send_message(
            "game",
            {
                "type": "keyPress",
                "key": game_key,
                "pressed": pressed,
            },
        )

    def on_mouse_motion(self, x, y):
        self.uwu_service.send_message(
            "game", {"type": "mouse", "x": x, "y": y})

    def on_mouse_click(self, x, y, button, pressed):
        if button == pygame.BUTTON_LEFT:
            button == "leftClick"
        elif button == pygame.BUTTON_RIGHT:
            button == "rightClick"
        elif button == pygame.BUTTON_MIDDLE:
            button == "middleClick"

        self.uwu_service.send_message(
            "game",
            {"type": "click", "x": x, "y": y, "button": button, "pressed": pressed},
        )
