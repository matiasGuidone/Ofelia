from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

import sys, os
sys.path.append(os.getcwd())
from modelo.conexion import conexion 
# configuration
from kivy.config import Config
Config.set("graphics", "width",  540)
Config.set("graphics", "height", 200)

class Box(BoxLayout):
    pass
    def btnCancelar(self):
        print ('Aceptar')

    def btnAceptar(self): 
        usuario_text = self.ids.txt_usuario.text
        pass_text = self.ids.txt_pass.text
        cone = conexion()
        param = [usuario_text, "admin", pass_text]
        cone.insert(param,"Usuarios")
        
	

class UsuarioApp(App):
    def build(self):
		  		return Box() 

if __name__ == "__main__":
	UsuarioApp().run()