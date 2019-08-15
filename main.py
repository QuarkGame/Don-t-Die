import kivy

from kivy.app import App
from kivy.lang import Builder

Builder.load_file("player.kv")
Builder.load_file("entities.kv")


class DontDieApp(App):
    pass


DontDieApp().run()

