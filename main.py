import kivy

from kivy.app import App
from kivy.lang import Builder

from player import *
from entities import *

# Source: https://stackoverflow.com/a/37572966
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

Builder.load_file("player.kv")
Builder.load_file("entities.kv")


class DontDieApp(App):
    pass


DontDieApp().run()
