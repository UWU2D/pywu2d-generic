import pygame
from pygame_gui import elements

from public.eventservice import IEventService
from public.maintainable import IMaintainable


class EventService(IEventService, IMaintainable):
    def __init__(self):
        self.listeners = {}
        self.all_listeners = []
        self.quit_listeners = []

    def register_event(self, type, callback):
        if type not in self.listeners:
            self.listeners[type] = []

        self.listeners[type].append(callback)

    def register_for_all(self, callback):
        self.all_listeners.append(callback)

    def register_quit(self, callback):
        self.quit_listeners.append(callback)

    def maintain(self, dt):
        try:
            pygame.event.pump()
        except Exception:
            pass

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                for c in self.quit_listeners:
                    c()

            if event.type in self.listeners:
                for c in self.listeners[event.type]:
                    c(event)
            for c in self.all_listeners:
                c(event)
