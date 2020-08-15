from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button 

import sys, os
sys.path.append(os.getcwd())
from modelo.conexion import conexion 
# configuration

 


class Box(BoxLayout):
    pass

    id_subcategoria = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # from kivy.core.window import Window
        # Window.size = (800, 500)
        
  
    def cargarComboSubCategoria(self, datos):
        dropdown = self.ids.drpTipogasto  
        dropdown.clear_widgets()   
        for index in range(len(datos)): 
            btn = Button(text = '% d - ' % index + str(datos[index][1]), size_hint_y = None, id = str(datos[index][0]), height = 40) 
            
            btn.bind(on_press = lambda btn: self.elegirSubCat(btn.id))
            btn.bind(on_release = lambda btn: dropdown.select(btn.text)) 
            dropdown.add_widget(btn) 

        mainbutton = self.ids.btnMainTG 
        mainbutton.bind(on_release = dropdown.open) 
        dropdown.bind(on_select = lambda instance, x: setattr(mainbutton, 'text', x)) 

    def elegirSubCat(self,id):
        self.id_subcategoria = int(id)

    def btnEmpleado(self):
        self.id_subcategoria = 0
        self.ids.lblSubcate.text = "Empleados: "
        cone = conexion()
        subcatego = cone.selectAll("SubcategoriaGastos", ["CategoriaGastos_id_cat_gasto", "1"])
        self.cargarComboSubCategoria(subcatego)
        pass

    def btnProveedor(self):
        self.id_subcategoria = 0
        self.ids.lblSubcate.text = "Proveedor: "
        cone = conexion()
        subcatego = cone.selectAll("SubcategoriaGastos", ["CategoriaGastos_id_cat_gasto", "2"])
        self.cargarComboSubCategoria(subcatego)
        pass

    def btnFijos(self):
        self.id_subcategoria = 0
        self.ids.lblSubcate.text = "Fijos: "
        cone = conexion()
        subcatego = cone.selectAll("SubcategoriaGastos", ["CategoriaGastos_id_cat_gasto", "3"])
        self.cargarComboSubCategoria(subcatego)
        pass

    def btnOtros(self):
        self.id_subcategoria = 0
        self.ids.lblSubcate.text = "Otros: "
        cone = conexion()
        subcatego = cone.selectAll("SubcategoriaGastos", ["CategoriaGastos_id_cat_gasto", "4"])
        self.cargarComboSubCategoria(subcatego)
        pass

    def btnPagar(self): 
        #(monto_gasto, observacion_gasto, Turnos_id_turno, SubcategoriaGastos_id_subcat_gasto)
        param = [self.ids.txtMonto.text, self.ids.txtObservaciones.text,1,self.id_subcategoria]
        cone = conexion()
        cone.insert(param,"Gastos")
        self.ids.lblInfo.text = "Gasto almacenado con éxito -"
        pass
    def btnSalir(self):
        
        pass

class RegistroGastoApp(App):
    def build(self):
		  		return Box() 

if __name__ == "__main__":
	RegistroGastoApp().run()

