from pyglet.window import key
from scenes.gameplay import GamePlayScene
import pyglet
from entities.player.player_classes import HERO_CLASSES


class MainMenuScene:
    def __init__(self, window):
        self.window = window
        # Available hero classes; default list if none provided
        self.class_options = list(HERO_CLASSES.keys())
        self.selected_index = 0

        # Title label
        self.title_label = pyglet.text.Label(
            'Select Your Class',
            font_size=48,
            x=window.width // 2,
            y=window.height - 100,
            anchor_x='center',
            anchor_y='center'
        )
        # Instruction label
        self.instr_label = pyglet.text.Label(
            'Use ↑/↓ to navigate, ENTER to confirm',
            font_size=16,
            x=window.width // 2,
            y=50,
            anchor_x='center',
            anchor_y='center'
        )
        # Prepare labels for each class option
        self.option_labels = []
        start_y = window.height // 2 + len(self.class_options) * 20
        for i, cls in enumerate(self.class_options):
            label = pyglet.text.Label(
                cls,
                font_size=24,
                x=window.width // 2,
                y=start_y - i * 50,
                anchor_x='center',
                anchor_y='center'
            )
            self.option_labels.append(label)

    def draw(self):
        # Draw title and instructions
        self.title_label.draw()
        self.instr_label.draw()
        # Draw each option, with indicator for selected
        for i, label in enumerate(self.option_labels):
            if i == self.selected_index:
                # Draw a '>' indicator to the left of selected option
                indicator = pyglet.text.Label(
                    '>',
                    font_size=24,
                    x=label.x - 100,
                    y=label.y,
                    anchor_x='center',
                    anchor_y='center'
                )
                indicator.draw()
            label.draw()

    def update(self, dt):
        pass

    def on_key_press(self, symbol, modifiers):
        # Navigate menu
        if symbol == key.UP:
            self.selected_index = (self.selected_index - 1) % len(self.class_options)
        elif symbol == key.DOWN:
            self.selected_index = (self.selected_index + 1) % len(self.class_options)
        elif symbol == key.ENTER:
            print(self.selected_index)
            chosen = self.class_options[self.selected_index].lower()
            self.window.current_scene = GamePlayScene(self.window, class_index=chosen)

    # Unused events can remain empty or removed
    def on_key_release(self, symbol, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        # Optionally allow clicking on options
        for i, label in enumerate(self.option_labels):
            width = label.content_width
            height = label.content_height
            left = label.x - width // 2
            right = label.x + width // 2
            bottom = label.y - height // 2
            top = label.y + height // 2
            if left <= x <= right and bottom <= y <= top:
                self.selected_index = i
                self.on_key_press(key.ENTER, None)
                break

    def on_mouse_motion(self, x, y, dx, dy):
        # Highlight option on hover
        for i, label in enumerate(self.option_labels):
            width = label.content_width
            height = label.content_height
            left = label.x - width // 2
            right = label.x + width // 2
            bottom = label.y - height // 2
            top = label.y + height // 2
            if left <= x <= right and bottom <= y <= top:
                self.selected_index = i
                break
