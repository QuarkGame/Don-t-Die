import kivy

from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window
from kivy.clock import Clock


class Player(Widget):

    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'w':
            self.center_y += 5
            # Clock.schedule_once(lambda dt: (self.center_y + 3), .25)
        elif keycode[1] == 's':
            self.center_y -= 5
        elif keycode[1] == 'a':
            self.center_x -= 5
        elif keycode[1] == 'd':
            self.center_x += 5
        return True


class Ground(RelativeLayout):
    pass
