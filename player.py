import kivy
import entities
import math

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import NumericProperty, StringProperty
from kivy.vector import Vector
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.boxlayout import BoxLayout

import entities

base_speed = 2
starve_health_rate = 10
hunger_drop_rate = 5
health_max = 100
hunger_max = 300
directions = {'w': ('s', 0, -base_speed),
              'a': ('d', base_speed, 0),
              's': ('w', 0, base_speed),
              'd': ('a', -base_speed, 0)}

inventory = [('Sword', 'assets/sprites/material/diamond_pick.png'),
             ('Dirt', ''),
             ('Bush', ''),
             ('Med Kit', '')]


class Player(Widget):

    _health = NumericProperty(health_max)
    _hunger = NumericProperty(hunger_max)
    _angle = NumericProperty(0)

    player = None

    def __init__(self, **kwargs):
        self.dead = False
        self.starve_event = None
        self.interact_limit = 0
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
            dist = Vector(self.center_x, self.center_y).distance(Vector(other.center_x, other.center_y))
            if hasattr(other, "loot"):
                # self.interact_limit = other.radius + (0.1 * other.radius)
                if other.center_y - (other.radius / 2) < self.center_y < other.center_y + (other.radius / 2):
                    self._angle = 0
                elif other.center_x - (other.radius / 2) < self.center_x < other.x + (other.radius / 2):
                    self._angle = 0
                else:
                    self._angle = (math.atan(abs(other.center_y - self.center_y) /
                                             int(abs(other.center_x - self.center_x)))
                                   * (180 / math.pi))
                if dist <= self.interact_limit:
                    other.loot()

    def update(self, dt):
        for other in Ground.ground.children:
            if self.collide_widget(other) and isinstance(other, entities.Entity):
                dx = other.center_x - self.center_x
                dy = other.center_y - self.center_y
                if abs(dx) > abs(dy):
                    move_y = 0
                    if dx > 0:
                        move_x = base_speed
                    else:
                        move_x = - base_speed
                else:
                    move_x = 0
                    if dy > 0:
                        move_y = base_speed
                    else:
                        move_y = - base_speed
                Ground.ground.move(move_x, move_y, dt=-dt, passive=True)

    def die(self):
        self.dead = True
        if not hasattr(self, "dead_sign"):
            self.dead_sign = self.parent.add_widget(Label(text="You died!",
                                                          font_size="100dp",
                                                          pos=self.pos))


class Ground(RelativeLayout):

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

    def move(self, move_x, move_y, dt=None, passive=False):
        if dt and Player.player.hunger:
            move = math.sqrt(move_x ** 2 + move_y ** 2)
            Player.player.hunger -= dt * abs(move) * hunger_drop_rate
        # self.center_x += move_x
        # self.center_y += move_y
        for child in self.children:
            child.center_x += move_x
            child.center_y += move_y

    def update(self, dt):
        for direction, instruct in directions.items():
            opposite, move_x, move_y = instruct
            if direction in self.move_events and opposite not in self.move_events:
                if not Player.player.dead:
                    self.move(move_x, move_y, dt=dt)


class ItemBox(ToggleButton):
    image = StringProperty()

    def __init__(self, **kwargs):
        super(ItemBox, self).__init__(**kwargs)
        self.image = kwargs.pop('image')
        if self.image == '':
            self.image = 'atlas://data/images/defaulttheme/button'


class InventoryBox(BoxLayout):

    def __init__(self, **kwargs):
        super(InventoryBox, self).__init__(**kwargs)
        for each in range(4):
            try:
                if inventory[each]:
                    self.add_widget(ItemBox(image=inventory[each][1], border=(3, 3, 3, 3)))
            except IndexError:
                self.add_widget(ItemBox(image=''))

