from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button 
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.config import Config
import platform

import sys, os
sys.path.append(os.getcwd())

from modelo.conexion import conexion 
from modelo.FechayHora import FechayHora 
Config.set("graphics", "window_state",  'maximized')
#Config.set("graphics", "width",  640)
#Config.set("graphics", "height", 450)
# configuration

 


class RegistroGasto(BoxLayout):
    pass

    id_subcategoria = 0
    str_seleccion = ""
    sub_categoria = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def foco(self, i):
        if i==1:
            self.ids.txtGasto.focus=False
            if self.ids.modMonto.active==True:
                self.ids.txtMonto.focus=True
            else:
                self.ids.txtObservaciones.focus=True
        elif i==2:
            self.ids.txtMonto.focus=False
            self.ids.txtObservaciones.focus=True
        else:
            self.btnPagar()
            self.ids.txtGasto.focus=True         
  
    def cargarComboSubCategoria(self, datos):
        dropdown = self.ids.drpTipogasto  
        dropdown.clear_widgets()  
        sistema = platform.system() 
        if len(datos) != 0:
            self.habilito(False)
            for index in range(len(datos)): 
                
                if sistema == "Windows":
                    btn = Button(text = '% d - ' % datos[index][0] + str(datos[index][1]), size_hint_y = None,  height = 40) 
                    btn.bind(on_press = lambda btn: self.elegirSubCat(btn.text.rsplit("-",2)[0]))
                else:
                    btn = Button(text = '% d - ' % index + str(datos[index][1]), size_hint_y = None, id = str(datos[index][0]), height = 40) 
                    btn.bind(on_press = lambda btn: self.elegirSubCat(btn.id))
                btn.bind(on_release = lambda btn: dropdown.select(btn.text)) 
                dropdown.add_widget(btn) 
        else:
            self.habilito(True)            
        mainbutton = self.ids.btnMainTG 
        mainbutton.bind(on_release = dropdown.open) 
        dropdown.bind(on_select = lambda instance, x: setattr(mainbutton, 'text', x)) 

    def habilito(self, v):
        self.ids.lblSubcate.disabled = v
        self.ids.btnMainTG.disabled = v
        self.ids.drpTipogasto.disabled = v
        self.ids.lbgasto.disabled = v
        self.ids.lbpesos.disabled = v
        self.ids.txtGasto.disabled = v
        self.ids.lbmontoabonado.disabled = v        
        self.ids.modMonto.active = v
        self.ids.modMonto.disabled = v
        self.ids.lbmodificar.disabled = v
        self.ids.lbPesos.disabled = v
        self.ids.lbobservacion.disabled = v
        self.ids.txtObservaciones.disabled = v
        self.ids.lblInfo.disabled = v
        self.ids.btnpagar.disabled = v   

    def elegirSubCat(self,id):
        self.id_subcategoria = int(id)
        con = conexion()
        subaux = con.selectId(self.id_subcategoria, 'SubcategoriaGastos')
        if len(subaux) > 0 :
            self.sub_categoria = subaux
            self.ids.lblInfo.text = "Dinero en cuenta: $ % d " % subaux[0][11] 
            ##la columna 11 tiene el dinero en cuenta 

#eventos de los botones toggle de arriba cada uno busca en la base los resultados correspondientes con cada tipo de gasto
    def btnEmpleado(self):
        self.id_subcategoria = 0
        self.ids.lblSubcate.text = "Empleados: "
        self.str_seleccion = "Empleado"
        cone = conexion()
        subcatego = cone.selectAll("SubcategoriaGastos", ["CategoriaGastos_id_cat_gasto", "1"])
        self.cargarComboSubCategoria(subcatego)
        pass

    def btnProveedor(self):
        self.id_subcategoria = 0
        self.ids.lblSubcate.text = "Proveedor: "
        self.str_seleccion = "Proveedor"
        cone = conexion()
        subcatego = cone.selectAll("SubcategoriaGastos", ["CategoriaGastos_id_cat_gasto", "2"])
        self.cargarComboSubCategoria(subcatego)
        pass

    def btnFijos(self):
        self.id_subcategoria = 0
        self.ids.lblSubcate.text = "Fijos: "
        self.str_seleccion = "Fijo"
        cone = conexion()
        subcatego = cone.selectAll("SubcategoriaGastos", ["CategoriaGastos_id_cat_gasto", "3"])
        self.cargarComboSubCategoria(subcatego)
        pass

    def btnOtros(self):
        self.id_subcategoria = 0
        self.ids.lblSubcate.text = "Otros: "
        self.str_seleccion = "Otros"
        cone = conexion()
        subcatego = cone.selectAll("SubcategoriaGastos", ["CategoriaGastos_id_cat_gasto", "4"])
        self.cargarComboSubCategoria(subcatego)
        pass

#Evento de botn de pagar realiza el descuento en la cuenta que tiene a favor el registro seleccionado
    def btnPagar(self): 
        if self.id_subcategoria == 0 or not  len(self.ids.txtMonto.text) > 0:
            contenido = BoxLayout(orientation='vertical')
            contenido.add_widget(Label(text=str("Seleccione un "+self.str_seleccion+" de la lista e ingrese monto.")))
            contenido.add_widget(Button(text='Aceptar', on_press = lambda *args: popup.dismiss()))
            popup = Popup(title="Mensaje", content= contenido, size_hint=(None,None),auto_dismiss=False, size=(400, 130))
            popup.open()
        #(monto_gasto, observacion_gasto, Turnos_id_turno, SubcategoriaGastos_id_subcat_gasto)
        else : 

            #insercion de gasto
            hora = FechayHora().getAhoraGuardo()
            param = [self.ids.txtMonto.text,self.str_seleccion + ' : -'+self.sub_categoria[0][1]+': '+ self.ids.txtObservaciones.text,1,self.id_subcategoria,hora]
            cone = conexion()
            cone.insert(param,"Gastos")

            #"update SubcategoriaGastos set nomb_subcat = ?, descr_subcat = ?, empleado_id = ?, 
            # proveedor_id = ?, sueldo = ?, adelanto = ?, contacto = ?, f_h_adelanto = ?, f__h_pago = ?,
            #  CategoriaGastos_id_cat_gasto = ?, cuenta = ? where id_subcat_gasto = ?"

            #insercion en la cuenta
            cuenta = (self.sub_categoria[0][11]  + float(self.ids.txtGasto.text)) - float(self.ids.txtMonto.text)
            param = [self.sub_categoria[0][1], self.sub_categoria[0][2],self.sub_categoria[0][3],self.sub_categoria[0][4],self.sub_categoria[0][5],self.sub_categoria[0][6],self.sub_categoria[0][7],self.sub_categoria[0][8],self.sub_categoria[0][9],self.sub_categoria[0][10],cuenta,self.id_subcategoria]
            cone.update(param,"SubcategoriaGastos")
            self.ids.txtGasto.text = ''
            self.ids.txtMonto.text = ''
            self.ids.modMonto.active = False
            self.ids.lblInfo.text = "Gasto almacenado exitosamente ._"+hora
            pass
     
    def ingMonto(self):
        if len(self.sub_categoria) > 0 and self.ids.txtGasto.text != '':
            self.ids.txtMonto.text = str(float(self.ids.txtGasto.text) + self.sub_categoria[0][11])
        else :
            self.ids.txtMonto.text = self.ids.txtGasto.text
        pass
 

class RegistroGastoApp(App):
    def build(self):
		  		return RegistroGasto() 

if __name__ == "__main__":
	RegistroGastoApp().run()

