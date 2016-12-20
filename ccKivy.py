# 
# Code snippet to test putting boxes, text etc onto a background image
#
# Requires cc.kv and background.png
#

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class ccGame(Widget):
    pass
class ccApp(App):
    def build(self):
        return ccGame()


if __name__ == '__main__':
    ccApp().run()

