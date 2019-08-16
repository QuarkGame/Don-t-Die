import kivy

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import NumericProperty
from kivy.vector import Vector

base_speed = 2
starve_health_rate = 10
hunger_drop_rate = 10
interact_limit = 50
health_max = 100
hunger_max = 300
directions = {'w': ('s', 'center_y', - base_speed),
              'a': ('d', 'center_x', base_speed),
              's': ('w', 'center_y', base_speed),
              'd': ('a', 'center_x', - base_speed)}


class Player(Widget):

    _health = NumericProperty(health_max)
    _hunger = NumericProperty(hunger_max)

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
        self._health = value
        if self._health <= 0:
            self._health = 0
            self.die()
        elif self._health > health_max:
            self._health = health_max

    @property
    def hunger(self):
        return self._hunger

    @hunger.setter
    def hunger(self, value):
        self._hunger = value
        if self._hunger <= 0:
            self._hunger = 0
            if not self.starve_event:
                self.starve_event = Clock.schedule_interval(self.starve, 0.01)
        elif self._hunger > hunger_max:
            self._hunger = hunger_max

    def starve(self, dt):
        self.health -= dt * starve_health_rate
        if self.hunger > 0:
            self.starve_event.cancel()
            self.starve_event = None

    def interact(self):
        for other in Ground.ground.children:
            if other is Player.player:
                continue
            dist = Vector(self.center_x, self.center_y).distance(Vector(other.center_x, other.center_y))
            if dist <= interact_limit and hasattr(other, "loot"):
                other.loot()

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
        if not hasattr(self, "dead_sign"):
            self.dead_sign = self.parent.add_widget(Label(text="You died!",
                                                          font_size="100dp",
                                                          pos=self.pos))


class Ground(Widget):

    ground = None

    def __init__(self, **kwargs):
        super(Ground, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

        self.velocity_x, self.velocity_y = 0, 0
        self.move_events = set()
        Clock.schedule_interval(self.update, 0.01)
        Ground.ground = self

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if Player.player.dead:
            return
        key_id, key_chr = keycode
        if key_chr in directions:
            self.move_events.add(key_chr)
        elif key_chr == 'e':
            Player.player.interact()

    def _on_keyboard_up(self, keyboard, keycode):
        key_id, key_chr = keycode
        if key_chr in directions and key_chr in self.move_events:
            self.move_events.remove(key_chr)
        return True

    def move(self, attr, val, dt=None):
        if dt:
            Player.player.hunger -= dt * abs(val) * hunger_drop_rate
        setattr(self, attr, getattr(self, attr) + val)
        for child in self.children:
            if not isinstance(child, Player):
                setattr(child, attr, getattr(child, attr) + val)

    def update(self, dt):
        for direction, instruct in directions.items():
            opposite, attr, val = instruct
            if direction in self.move_events and opposite not in self.move_events:
                if not Player.player.dead:
                    self.move(attr, val, dt=dt)
