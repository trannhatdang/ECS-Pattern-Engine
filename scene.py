import gameobject
class Scene():
    def __init__(self, display_surf, size = (1280, 720)):
        self._display_surf = display_surf
        self._frametime = 0
        self._next_scene = 0
        self._game_objects = []
        self._running = True
        self.size = size

    def on_loop(self):
        for obj in self._game_objects:
            obj.on_loop(frametime, self)
        pass

    def on_render(self):
        for obj in self._game_objects:
            obj.on_render(display_surf, self)
        pygame.display.flip()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_execute(self):
        if self.on_init() == False:
            self._running = False
            self._next_scene = -1
 
        while( self._running ):
            start_time = time.time()

            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()

            self._frametime = time.time() - start_time

        return self._next_scene

    def add_game_obj(self, obj):
        if isinstance(obj, GameObject):
            self._game_objects.append(obj)
