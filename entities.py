import kivy
import math

from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.properties import BooleanProperty, NumericProperty

import player
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label


class Entity(Widget):

    def on_pos(self, instance, value):
        pass


class Transparent(Widget):
    pass


class Interactive(Widget):

    def __init__(self, **kwargs):
        self.cool_down = False
        Clock.schedule_interval(self.update, 0.01)
        self.action_btn = None
        self.lootable = False
        super(Interactive, self).__init__(**kwargs)

    def update(self, dt):
        other = player.Player.player
        dist = Vector(self.center_x, self.center_y).distance(Vector(other.center_x, other.center_y))
        interact_limit = self.radius * 1.15
        if dist <= interact_limit:
            if not self.cool_down:
                if not hasattr(self, "action_btn") or not self.action_btn:
                    self.action_btn = Button(text="E",
                                             size_hint=(None, None),
                                             size=(30, 30),
                                             x=self.x,
                                             y=self.y)
                    self.action_btn.bind(on_press=lambda _: self.loot())
                    self.add_widget(self.action_btn)
                    self.lootable = True
            else:
                self.action_btn
                self.clear_widgets()
                self.lootable = False
        else:
            if hasattr(self, "action_btn") and self.action_btn:
                other._angle = 0
                self.action_btn = None
                self.clear_widgets()
                self.lootable = False

    def loot(self):
        if self.cool_down:
            return True
        else:
            other = player.Player.player
            if self.center_y - (self.radius / 2) < other.center_y < self.center_y + (self.radius / 2):
                other._angle = 0
            elif self.center_x - (self.radius / 2) < other.center_x < self.x + (self.radius / 2):
                other._angle = 0
            else:
                other._angle = (math.atan(abs(self.center_y - other.center_y) /
                                          abs(self.center_x - other.center_x))
                                * (180 / math.pi))
            self.cool_down = True
            Clock.schedule_once(lambda _: setattr(self, "cool_down", False), 3)


class Bush(Entity, Interactive):

    def __init__(self, **kwargs):
        self.radius = 50
        super(Bush, self).__init__(**kwargs)

    def loot(self):
        if super(Bush, self).loot():
            return
        player.Player.player.hunger += 10


class FirstAidKit(Entity, Interactive):

    def __init__(self, **kwargs):
        self.radius = 75
        super(FirstAidKit, self).__init__(**kwargs)

    def loot(self):
        if super(FirstAidKit, self).loot():
            return
        player.Player.player.health += 10


class Leaves(Transparent):

    def __init__(self, **kwargs):
        super(Leaves, self).__init__(**kwargs)
        self.radius = 45


class Stone(Widget):
    pass
