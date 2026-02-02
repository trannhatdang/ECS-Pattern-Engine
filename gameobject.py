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
