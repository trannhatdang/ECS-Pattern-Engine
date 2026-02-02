import pygame
import time
import os
import random
import math
import operator
import gameobject
from scene import Scene
from pygame.locals import *

class App():
    def __init__(self, size = (1280, 720)):
        self._display_surf = None
        self._frametime = 0
        self._scenes = []
        self._curr_scene = 0
        self.size = size

    def on_init(self):
        random.seed(time.time())
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        #self._font = pygame.font.Font(VCR_OSD_MONO_FONT, 24)
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._scenes.append(Scene(self._display_surf))
 
    def on_cleanup(self):
        pygame.font.quit()
        pygame.quit()
 
    def on_execute(self):
        self.on_init()

        next_scene = 0
        while next_scene >= 0:
            next_scene = self._scenes[0].on_execute()

    def add_scene(self, scene):
        self._scenes.append(scene)
        pass
 
if __name__ == "__main__" :
    game = App()
    game.on_execute()
