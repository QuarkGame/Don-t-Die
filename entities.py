import kivy

from kivy.uix.widget import Widget
from player import Player


class Tree(Widget):

    def on_pos(self, instance, value):
        if self.collide_widget(Player.player):
            pass


class Stone(Widget):
    pass

