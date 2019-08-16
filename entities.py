import kivy

from kivy.uix.widget import Widget
from player import Player


class Entity(Widget):

    def on_pos(self, instance, value):
        pass

    def loot(self):
        pass


class Bush(Entity):

    def loot(self):
        Player.player.hunger += 10


class FirstAidKit(Entity):

    def loot(self):
        Player.player.health += 10


class Stone(Widget):
    pass

