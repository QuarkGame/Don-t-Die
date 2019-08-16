import kivy

from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.vector import Vector

import player


class Entity(Widget):

    def on_pos(self, instance, value):
        pass

    def loot(self):
        pass


class Transparent(Widget):
    pass


class Interactive(Widget):

    def __init__(self, **kwargs):
        Clock.schedule_interval(self.update, 0.01)
        super(Interactive, self).__init__(**kwargs)

    def update(self, dt):
        other = player.Player.player
        dist = Vector(self.center_x, self.center_y).distance(Vector(other.center_x, other.center_y))
        if dist <= player.interact_limit:
            if not hasattr(self, "action_btn") or not self.action_btn:
                self.action_btn = Button(text="E",
                                         size_hint=(None, None),
                                         size=(20, 20),
                                         x=self.x,
                                         y=self.y)
                self.action_btn.bind(on_press=lambda _: self.loot())
                self.add_widget(self.action_btn)
        else:
            if hasattr(self, "action_btn") and self.action_btn:
                self.action_btn = None
                self.clear_widgets()


class Bush(Entity, Interactive):

    def loot(self):
        player.Player.player.hunger += 10


class FirstAidKit(Entity, Interactive):

    def loot(self):
        player.Player.player.health += 10


class Leaves(Transparent):
    pass


class Stone(Widget):
    pass

