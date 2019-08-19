import kivy

from kivy.uix.widget import Widget
from kivy.properties import NumericProperty


class GameObject(Widget):

    def __le__(self, other):
        # calculate distance between self and others here
        dist = 0
        return dist