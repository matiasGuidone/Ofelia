from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button 
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.config import Config
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
import platform

import sys, os
sys.path.append(os.getcwd())
from modelo.conexion import conexion 
from modelo.FechayHora import FechayHora 
Config.set("graphics", "width",  640)
Config.set("graphics", "height", 380)
# configuration

class Box(BoxLayout):
    pass

    id = 0
    str_seleccion = ""
    cuenta = []
    tipoCuenta = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
              
  
    def cargarComboSubCategoria(self, datos):
        dropdown = self.ids.drpTipogasto  
        dropdown.clear_widgets()  
        sistema = platform.system() 
        for index in range(len(datos)): 
            
            if sistema == "Windows":
                btn = Button(text = '% d - ' % datos[index][0] + str(datos[index][1]), size_hint_y = None,  height = 40) 
                btn.bind(on_press = lambda btn: self.elegirSubCat(btn.text.rsplit("-",2)[0]))
            else:
                btn = Button(text = '% d - ' % index + str(datos[index][1]), size_hint_y = None, id = str(datos[index][0]), height = 40) 
                btn.bind(on_press = lambda btn: self.elegirSubCat(btn.id))
            btn.bind(on_release = lambda btn: dropdown.select(btn.text)) 
            dropdown.add_widget(btn) 

        mainbutton = self.ids.btnMainTG 
        mainbutton.bind(on_release = dropdown.open) 
        dropdown.bind(on_select = lambda instance, x: setattr(mainbutton, 'text', x)) 

    def elegirSubCat(self,id):
        self.id = int(id) 
        self.cuenta = conexion().selectId(self.id, 'SubcategoriaGastos')
        if len(self.cuenta)>0:
            self.ids.btnNuevo.disabled = False
            self.ids.btnEditar.disabled = False
            self.ids.btnEliminar.disabled = False    
    
         

#eventos de los botones toggle de arriba cada uno busca en la base los resultados correspondientes con cada tipo de gasto
    def btnEmpleado(self):
        self.id = 0
        self.ids.lblSubcate.text = "Empleados: "
        self.str_seleccion = "Empleado" 
        self.tipoCuenta = 1
        subcatego = conexion().selectAll("SubcategoriaGastos", ["CategoriaGastos_id_cat_gasto", "1"])
        self.cargarComboSubCategoria(subcatego)
        self.ids.btnNuevo.disabled = False
        self.ids.btnEditar.disabled = True
        self.ids.btnEliminar.disabled = True
        pass

    def btnProveedor(self):
        self.id = 0
        self.ids.lblSubcate.text = "Proveedor: "
        self.str_seleccion = "Proveedor" 
        self.tipoCuenta = 2
        subcatego = conexion().selectAll("SubcategoriaGastos", ["CategoriaGastos_id_cat_gasto", "2"])
        self.cargarComboSubCategoria(subcatego)
        self.ids.btnNuevo.disabled = False
        self.ids.btnEditar.disabled = True
        self.ids.btnEliminar.disabled = True
        pass

    def btnFijos(self):
        self.id = 0
        self.ids.lblSubcate.text = "Fijos: "
        self.str_seleccion = "Fijo" 
        self.tipoCuenta = 3
        subcatego = conexion().selectAll("SubcategoriaGastos", ["CategoriaGastos_id_cat_gasto", "3"])
        self.cargarComboSubCategoria(subcatego)
        self.ids.btnNuevo.disabled = False
        self.ids.btnEditar.disabled = True
        self.ids.btnEliminar.disabled = True
        pass

    def btnOtros(self):
        self.id = 0
        self.ids.lblSubcate.text = "Otros: "
        self.str_seleccion = "Otros" 
        self.tipoCuenta = 4
        subcatego = conexion().selectAll("SubcategoriaGastos", ["CategoriaGastos_id_cat_gasto", "4"])
        self.cargarComboSubCategoria(subcatego)
        self.ids.btnNuevo.disabled = False
        self.ids.btnEditar.disabled = True
        self.ids.btnEliminar.disabled = True
        pass
    
    def openPopup(self, titulo):
        #armado de popup 
        contenido = BoxLayout(orientation='vertical')
        #campos de llenado
        if self.id != 0:
            nombre = TextInput(hint_text="Nombre de "+self.str_seleccion,text = self.cuenta[0][1])
            descr = TextInput( hint_text="Descripción",text = self.cuenta[0][2] )
            sueldo = TextInput( hint_text="Sueldo", input_filter = 'float',text = str(self.cuenta[0][5]) )
            contacto = TextInput( hint_text="Contacto" ,text = self.cuenta[0][7] )
            cuenta = TextInput(hint_text = "Cuenta", input_filter = 'float',text = str(self.cuenta[0][11]) )
        else:
            nombre = TextInput(hint_text="Nombre de "+self.str_seleccion)
            descr = TextInput( hint_text="Descripción" )
            sueldo = TextInput( hint_text="Sueldo", input_filter = 'float' )
            contacto = TextInput( hint_text="Contacto" )
            cuenta = TextInput(hint_text = "Cuenta", input_filter = 'float')

        
 
        but = BoxLayout(orientation='horizontal')
        but.add_widget(Button(text="Cancelar",on_press = lambda *args: popup.dismiss()))
        
        contenido.add_widget(nombre)
        contenido.add_widget(descr)
        if self.tipoCuenta == 1 :
            contenido.add_widget(sueldo)
            but.add_widget(Button(text="Guardar" ,on_press = lambda *args: self.guardarCuenta(nombre.text, descr.text, float(sueldo.text), contacto.text, float(cuenta.text), popup)))
        else:
            but.add_widget(Button(text="Guardar" ,on_press = lambda *args: self.guardarCuenta(nombre.text, descr.text, 0, contacto.text, float(cuenta.text), popup)))
        contenido.add_widget(contacto)
        contenido.add_widget(cuenta)
        contenido.add_widget(but)
        popup = Popup(title = titulo, content= contenido, size_hint=(None,None),auto_dismiss=False, size=(460, 370))
        popup.open()
        pass

    def guardarCuenta(self, nombre , descr, sueldo, contacto , cuenta, popup):
        if self.id == 0:
            #insert into SubcategoriaGastos ( nomb_subcat, descr_subcat, 
            # empleado_id, proveedor_id, sueldo, adelanto, contacto, f_h_adelanto, 
            # f__h_pago, CategoriaGastos_id_cat_gasto, cuenta) values (?,?,?,?,?,?,?,?,?,?,?)"
            conexion().insert([nombre, descr , 0, 0, sueldo, 0, contacto, None, None, self.tipoCuenta, cuenta], 'SubcategoriaGastos')
            popup.dismiss()
        else :
            conexion().update([nombre, descr , 0, 0, sueldo, 0, contacto, None, None, self.tipoCuenta, cuenta, self.id], 'Usuarios')
            popup.dismiss()
             
        pass

    #eventos botones de edición

    def btnNuevo(self):
        self.id = 0
        self.openPopup("Nueva cuenta de "+self.str_seleccion)
        pass

    def btnEditar(self): 
        self.openPopup("Editar cuenta de "+self.str_seleccion)
        pass

    def btnEliminar(self):
        if len(self.cuenta) == 0 :
            contenido = BoxLayout(orientation='vertical')
            contenido.add_widget(Label(text=str("Seleccione una cuenta de la lista.")))
            contenido.add_widget(Button(text='Aceptar', on_press = lambda *args: popup.dismiss()))
            popup = Popup(title="Mensaje", content= contenido, size_hint=(None,None),auto_dismiss=False, size=(400, 130))
            popup.open()
        else:    
            cont = BoxLayout(orientation='vertical')
            buttons = BoxLayout()
            cont.add_widget(Label(text='¿ Desea eliminar la cuenta de "'+self.cuenta[0][1]+'" ?'))
            buttons.add_widget(Button(text='si', on_press = lambda btn: self.elimina(mensj) ))
            buttons.add_widget(Button(text='no',on_press = lambda *args: mensj.dismiss() ))
            cont.add_widget(buttons)
            mensj = Popup(title="Confirmar", content= cont,auto_dismiss=False, size_hint=(None,None), size=(430, 120))
            mensj.open()
         
        pass
    
    def elimina(self,popup):
        conexion().delete(self.id, 'SubcategoriaGastos')
        popup.dismiss() 
        pass


class RegistroCuentasApp(App):
    def build(self):
		  		return Box() 

if __name__ == "__main__":
	RegistroCuentasApp().run()

