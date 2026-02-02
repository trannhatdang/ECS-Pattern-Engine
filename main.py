import pygame
import time
import os
import random
import math
import operator
import gameobject
from pygame.locals import *

class App():
    def __init__(self, size = 1280, 720):
        self._display_surf = None
        self._frametime = 0

    def on_init(self):
        random.seed(time.time())
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        self._font = pygame.font.Font(VCR_OSD_MONO_FONT, 24)
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
 
    def on_loop(self):
        for obj in self.children_objects:
            obj.on_loop(self._frametime)

    def on_render(self):
        for obj in self.children_objects:
            obj.on_render()
        pygame.display.flip()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        for obj in self.children_objects.on_event(event)

    def on_cleanup(self):
        pygame.font.quit()
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            start_time = time.time()

            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()

            self._frametime = time.time() - start_time
        self.on_cleanup()

 
if __name__ == "__main__" :
    game = App()
    game.on_execute()
