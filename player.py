import kivy

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
from kivy.properties import BoundedNumericProperty

base_speed = 2
starve_rate = 10
directions = {'w': ('center_y', - base_speed),
              'a': ('center_x', base_speed),
              's': ('center_y', base_speed),
              'd': ('center_x', - base_speed)}


class Player(Widget):

    _health = BoundedNumericProperty(100, min=0, max=100)
    _hunger = BoundedNumericProperty(300, min=0, max=300)

    player = None

    def __init__(self, **kwargs):
        self.dead = False
        self.starve_event = None
        Player.player = self
        Clock.schedule_interval(self.update, 0.01)
        super(Player, self).__init__(**kwargs)

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        try:
            self._health = value
        except ValueError:
            self.die()

    @property
    def hunger(self):
        return self._hunger

    @hunger.setter
    def hunger(self, value):
        try:
            self._hunger = value
        except ValueError:
            if self._hunger < 0:
                self._hunger = 0
                if not self.starve_event:
                    self.starve_event = Clock.schedule_interval(self.starve, 0.01)

    def starve(self, dt):
        self.health -= dt * starve_rate
        if self.hunger > 0:
            self.starve_event.cancel()
            self.starve_event = None

    def update(self, dt):
        for other in Ground.ground.children:
            if self.collide_widget(other) and other is not Player.player:
                dx = other.center_x - self.center_x
                dy = other.center_y - self.center_y
                if abs(dx) > abs(dy):
                    dir_attr = 'center_x'
                    if dx > 0:
                        move_val = base_speed
                    else:
                        move_val = - base_speed
                else:
                    dir_attr = 'center_y'
                    if dy > 0:
                        move_val = base_speed
                    else:
                        move_val = - base_speed
                Ground.ground.move(dir_attr, move_val)

    def die(self):
        self.dead = True
        print("Game over")


class Ground(Widget):

    ground = None

    def __init__(self, **kwargs):
        super(Ground, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)
        self.move_events = {'w': None, 'a': None, 's': None, 'd': None}
        Ground.ground = self

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        key_id, key_chr = keycode
        if key_chr in directions and not self.move_events[key_chr]:
            attr, val = directions[key_chr]
            self.move_events[key_chr] = Clock.schedule_interval(lambda dt: self.move(attr, val, dt=dt), 0.01)
        return True

    def _on_keyboard_up(self, keyboard, keycode):
        key_id, key_chr = keycode
        if key_chr in directions:
            self.move_events[key_chr].cancel()
            self.move_events[key_chr] = None
        return True

    def move(self, attr, val, dt=None):
        if dt:
            Player.player.hunger -= dt * abs(val) * 10
        setattr(self, attr, getattr(self, attr) + val)
        for child in self.children:
            if not isinstance(child, Player):
                setattr(child, attr, getattr(child, attr) + val)
