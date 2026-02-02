import pygame
import time
import os
import random
import math
import operator
from pygame.locals import *

class GameObject:
    def __init__(self, position, children_objects = []):
        self.position = position
        self.children_objects = children_objects

        self.should_be_destroyed = False
        pass

    def on_loop(self, frametime):
        for child in self.children_objects:
            if child.should_be_destroyed:
                child.on_destroy()
                self.children_objects.remove(child)
                continue

            child.on_loop(frametime)
        pass

    def on_render(self, display_surf):
        for child in self.children_objects:
            child.on_render(display_surf)
        pass

    def on_event(self, event):
        for child in self.children_objects:
            child.on_event(event)
        pass

    def on_destroy(self):
        for child in self.children_objects:
            child.on_destroy()

        self.should_be_destroyed = True
        pass

    def add_children_object(self, obj):
        if isinstance(obj, GameObject):
            children_objects.add(obj)

    def add_component(self, obj):
        if isinstance(obj, Component)
        components.add()

class Component:
    def __init__(self, game_object):
        pass

class App():
    def __init__(self):
        self._display_surf = None
        self._alive_zombies = []

        self._free_spawn_locations = SPAWN_LOCATIONS
        self._occupied_spawn_locations = []

        self._background_sprite = pygame.image.load(BACKGROUND_IMG)
        self._background_sprite = pygame.transform.scale(self._background_sprite, (1584/1.33, 887/1.33))
        self._font = None

        self._debug = False
        self._spawn_time = DEFAULT_SPAWN_TIME
        self._alive_time = DEFAULT_ZOMBIE_ALIVE_TIME
        self._curr_spawn_timer = self._spawn_time
        self._frametime = 0

        self._streak = 0
        self._points = 0
        self._misses = 0
        self._hitrate = 0

        self.size = self.weight, self.height = 1584/1.33, 887/1.33
        #print(self.size)

    def get_random_spawn_location(self):
        if(len(self._free_spawn_locations) == 0):
            return (0, 0)

        retval = self._free_spawn_locations[random.randrange(0, len(self._free_spawn_locations))]

        return retval

    def on_init(self):
        random.seed(time.time())
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        self._font = pygame.font.Font(VCR_OSD_MONO_FONT, 24)
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
 
    def on_loop(self):
        for zombie in self._alive_zombies:
            zombie.on_loop(self._frametime)

            if zombie.should_be_destroyed:
                location = zombie.position
                self._free_spawn_locations.append(location)
                self._occupied_spawn_locations.remove(location)
                self._alive_zombies.remove(zombie)

        self._curr_spawn_timer = self._curr_spawn_timer - self._frametime
        if self._curr_spawn_timer <= 0 and len(self._free_spawn_locations) > 0:
            spawn_location = self.get_random_spawn_location()
            self._occupied_spawn_locations.append(spawn_location)
            self._free_spawn_locations.remove(spawn_location)

            self._alive_zombies.append(Zombie(spawn_location, alive_time = self._alive_time))
            self._curr_spawn_timer = self._spawn_time

        self._spawn_time = min(max(DEFAULT_SPAWN_TIME - math.log(max(self._streak, 1))/5, .1), DEFAULT_SPAWN_TIME)
        self._alive_time = min(max(DEFAULT_ZOMBIE_ALIVE_TIME - math.log(max(self._streak, 1)), 1), DEFAULT_ZOMBIE_ALIVE_TIME)
        if(self._points + self._misses != 0):
            self._hitrate = self._points / (self._points + self._misses)
        else:
            self._hitrate = 0

    def on_render(self):
        self._display_surf.blit(self._background_sprite, self._background_sprite.get_rect())
        for zombie in self._alive_zombies:
            zombie.on_render(self._display_surf)

        points_surf = self._font.render("POINTS: " + str(self._points), False, (0, 0, 0))
        misses_surf = self._font.render("MISSES: " + str(self._misses), False, (0, 0, 0))
        hitrate_surf = self._font.render("ACC: " + str(round(self._hitrate, 2) * 100) + "%", False, (0, 0, 0))

        self._display_surf.blit(points_surf, (10, 120))
        self._display_surf.blit(misses_surf, (10, 145))
        self._display_surf.blit(hitrate_surf, (10, 170))

        if self._debug:
            spawn_time_surf = self._font.render("SPAWN_TIME: " + str(round(self._spawn_time, 2)), False, (0, 0, 0))
            alive_time_surf = self._font.render("ALIVE_TIME: " + str(round(self._alive_time, 2)), False, (0, 0, 0))
            streak_surf = self._font.render("STREAK: " + str(self._streak), False, (0, 0, 0))
            self._display_surf.blit(spawn_time_surf, (10, 245))
            self._display_surf.blit(alive_time_surf, (10, 270))
            self._display_surf.blit(streak_surf, (10, 305))

        pygame.display.flip()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.on_mouse_down(event)

        if event.type == pygame.KEYDOWN and event.key == 100:
            self._debug = not self._debug

        if event.type == ZOMBIE_HIDDEN_EVENT:
            self._streak = max(self._streak - 1, 0)
            #self._misses = max(self._misses + 1, 0)


        for zombie in self._alive_zombies:
            zombie.on_event(event)


    def on_mouse_down(self, event):
        has_hit = False
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for zombie in self._alive_zombies:
            min_width = zombie.position[0]
            max_width = zombie.position[0] + 64 + zombie.collider_offset[0]
            min_height = zombie.position[1]
            max_height = zombie.position[1] + 64 + zombie.collider_offset[1]

            if mouse_x >= min_width and mouse_x <= max_width and mouse_y >= min_height and mouse_y <= max_height and zombie.get_bonkable() and zombie.status != zombie.DEATH:
                has_hit = True
                zombie.die()
                break

        if has_hit:
            self._streak = max(self._streak + 1, 0)
            self._points = max(self._points + 1, 0)
        else:
            self._streak = max(self._streak - 1, 0)
            self._misses = max(self._misses + 1, 0)

    def on_cleanup(self):
        pygame.font.quit()
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        sound = pygame.mixer.Sound(BACKGROUND_MUSIC)
        sound.set_volume(0.2)
        sound.play(loops = 1)
 
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
