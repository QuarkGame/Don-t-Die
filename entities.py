import kivy

from kivy.uix.widget import Widget

import player


class Entity(Widget):

    def on_pos(self, instance, value):
        pass

    def loot(self):
        pass


class Transparent(Widget):
    pass


class Bush(Entity):

    def loot(self):
        player.Player.player.hunger += 10


class FirstAidKit(Entity):

    def loot(self):
        player.Player.player.health += 10


class Leaves(Transparent):
    pass


class Stone(Widget):
    pass

