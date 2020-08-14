from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button 

import sys, os
sys.path.append(os.getcwd())
from modelo.conexion import conexion 
# configuration
from kivy.config import Config
Config.set("graphics", "width",  800)
Config.set("graphics", "height", 400)
 


class Box(BoxLayout):
    pass
     
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        

    #     # dropdown = self.ids.drp_tipogasto
    #     # for index in range(10): 
  
    #     # # Adding button in drop down list 
    #     #     btn = Button(text ='Value % d' % index, size_hint_y = None, height = 40) 
        
    #     #     # binding the button to show the text when selected 
    #     #     btn.bind(on_release = lambda btn: dropdown.select(btn.text)) 
        
    #     #     # then add the button inside the dropdown 
    #     #     dropdown.add_widget(btn)
    #     # pass

    def btnEmpleado(self):
        self.ids.lblSubcate.text = "Empleados "
        cone = conexion()
        subcatego = cone.selectAll("SubcategoriaGastos", ["CategoriaGastos_id_cat_gasto", "1"])
        print (subcatego)
        pass

    def btnProveedor(self):
        self.ids.lblSubcate.text = "Proveedor "
        cone = conexion()
        subcatego = cone.selectAll("SubcategoriaGastos", ["CategoriaGastos_id_cat_gasto", "2"])
        print (subcatego)
        pass

    def btnFijos(self):
        self.ids.lblSubcate.text = "Fijos "
        cone = conexion()
        subcatego = cone.selectAll("SubcategoriaGastos", ["CategoriaGastos_id_cat_gasto", "3"])
        print (subcatego)
        pass

    def btnOtros(self):
        self.ids.lblSubcate.text = "Otros "
        cone = conexion()
        subcatego = cone.selectAll("SubcategoriaGastos", ["CategoriaGastos_id_cat_gasto", "4"])
        print (subcatego)
        pass

    def btnPagar(self): 
        # usuario_text = self.ids.txt_usuario.text
        # pass_text = self.ids.txt_pass.text
        # cone = conexion()
        # param = [usuario_text, "admin", pass_text]
        # cone.insert(param,"Usuarios")
        pass
    def btnSalir(self):
        #print ('Aceptar')
        pass

class RegistroGastoApp(App):
    def build(self):
		  		return Box() 

if __name__ == "__main__":
	RegistroGastoApp().run()

