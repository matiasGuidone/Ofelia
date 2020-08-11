from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

# configuration
from kivy.config import Config
Config.set("graphics", "width",  800)
Config.set("graphics", "height", 600)

class Box(BoxLayout):
	pass

class UsuarioApp(App):
	def build(self):
		  		return Box()  

if __name__ == "__main__":
	UsuarioApp().run()