import pyglet

resources = {}

def load_image(path):
    if path not in resources:
        resources[path] = pyglet.resource.image(path)
    return resources[path]

def load_sound(path):
    if path not in resources:
        resources[path] = pyglet.resource.media(path, streaming=False)
    return resources[path]
