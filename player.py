import kivy

from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window
from kivy.clock import Clock

base_speed = 2
directions = {'w': ('center_y', - base_speed),
              'a': ('center_x', base_speed),
              's': ('center_y', base_speed),
              'd': ('center_x', - base_speed)}


class Player(Widget):

    player = None

    def __init__(self, **kwargs):
        Player.player = self
        super(Player, self).__init__(**kwargs)


class Ground(Widget):

    def __init__(self, **kwargs):
        super(Ground, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)
        self.move_events = {'w': None, 'a': None, 's': None, 'd': None}

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        key_id, key_chr = keycode
        if key_chr in directions and not self.move_events[key_chr]:
            attr, val = directions[key_chr]
            self.move_events[key_chr] = Clock.schedule_interval(lambda _: self.move(attr, val), 0.01)
        return True

    def _on_keyboard_up(self, keyboard, keycode):
        key_id, key_chr = keycode
        if key_chr in directions:
            self.move_events[key_chr].cancel()
            self.move_events[key_chr] = None
        return True

    def move(self, attr, val):
        setattr(self, attr, getattr(self, attr) + val)
        for child in self.children:
            if not isinstance(child, Player):
                setattr(child, attr, getattr(child, attr) + val)
