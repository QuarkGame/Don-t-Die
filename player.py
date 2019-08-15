import kivy

from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window
from kivy.clock import Clock


class Player(Widget):

    pframe = 0
    # def __init__(self, **kwargs):
    #     super(Player, self).__init__(**kwargs)
    #     self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
    #     self._keyboard.bind(on_key_down=self._on_keyboard_down)
    #
    # def _keyboard_closed(self):
    #     self._keyboard.unbind(on_key_down=self._on_keyboard_down)
    #     self._keyboard = None
    #
    # def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
    #     if keycode[1] == 'w':
    #         self.center_y += 5
    #         print(keyboard, keycode, text, modifiers)
    #         # Clock.schedule_once(lambda dt: self._on_keyboard_down(keyboard, keycode, text, modifiers), .25)
    #     elif keycode[1] == 's':
    #         self.center_y -= 5
    #     elif keycode[1] == 'a':
    #         self.center_x -= 5
    #     elif keycode[1] == 'd':
    #         self.center_x += 5
    #     return True

    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

        self.pressed_keys = set()

        self.pressed_actions = {
            'w': lambda: self.move('w'),
            's': lambda: self.move('s'),
            'a': lambda: self.move('a'),
            'd': lambda: self.move('d'),
        }

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self.pressed_keys.add(keycode[1])
        Clock.schedule_once(lambda dt: self.update(dt), .01)

    def _on_keyboard_up(self, keyboard, keycode):
        self.pressed_keys.remove(keycode[1])

    def move(self, direction):
        if direction == 'w':
            self.center_y += 5
        elif direction == 's':
            self.center_y -= 5
        elif direction == 'd':
            self.center_x += 5
        else:
            self.center_x -= 5

    def update(self, dt):
        for key in self.pressed_keys:
            try:
                self.pressed_actions[key]()
            except KeyError:
                return dt


class Ground(RelativeLayout):
    pass
