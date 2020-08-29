import os
import sys
import platform
from datetime import datetime

from kivy.app import App
# configuration
from kivy.config import Config
Config.set("graphics", "window_state",  'maximized')
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
sys.path.append(os.getcwd())
from modelo.conexion import conexion
from modelo.FechayHora import FechayHora

#damian
class Box(BoxLayout):
    
    def __init__(self, **kwargs):         
        super().__init__(**kwargs)



class Turno(App):
    def build(self):
                return Box()   
        
if __name__ == "__main__":
    Turno().run()