import pyglet
import os




def load_animation(character, animation_name, scale = 0.2):
    animation_path = f"assets/{character}/gifs/{animation_name}.gif"
    if not os.path.exists(animation_path):
        raise FileNotFoundError(f"Animation file not found: {animation_path}")
    animation = pyglet.image.load_animation(animation_path)
    for frame in animation.frames:
        frame.image.anchor_x = frame.image.width // 2
        frame.image.anchor_y = frame.image.height // 2
    sprite = pyglet.sprite.Sprite(animation)
    sprite.scale = scale
    return sprite


def load_all_animations(character):
    animations = {}
    gifs_path = f"assets/{character}/gifs"
    for filename in os.listdir(gifs_path):
        if filename.endswith('.gif'):
            name = filename[:-4]  # Remove '.gif' extension
            animations[name] = load_animation(character, name)
    return animations
