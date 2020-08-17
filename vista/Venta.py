import os
import sys
import platform

from datetime import datetime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

sys.path.append(os.getcwd())
from modelo.conexion import conexion
from modelo.FechayHora import FechayHora


# configuration
from kivy.config import Config
Config.set("graphics", "width",  520)
Config.set("graphics", "height", 90)
#damian
class Box(BoxLayout):
    pass
    sistema=None
    dropdown=None
    diccTipoPago={'0' : "Efectivo", '1' : "Débito", '2' : "Crédito"}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def btnRegistrarVenta(self):
        #self.ids.lblSubcate.text = "Registrar"
        #v=AccionVentas(turno, caja)
#montoDeVenta(float), observación,idTurno,tipoPago,Caja
        #v.cargarVenta([])
        print ("registro venta")

    def btnBorrar(self):
        #self.ids.lblSubcate.text = "Registrar"
        #v=AccionVentas(turno, caja)
#montoDeVenta(float), observación,idTurno,tipoPago,Caja
        #v.cargarVenta([])
        print ("Borro venta")

    def cargarCombo(self):
        self.dropdown = self.ids.drpTipoPago
        self.dropdown.clear_widgets()
        self.sistema = platform.system() 

        for i in range(len(self.diccTipoPago)):
            btn = Button(text=' %d' % i + self.diccTipoPago[i], size_hint_y=None, height=30)
            btn.bind(on_press=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)

        mainbutton = Button(text='Efectivo', size_hint=(None, None))
        mainbutton.bind(on_release=self.dropdown.open)
        self.dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))




class AccionVentas:
#Utiles para la corrida
    lista=None   
#conexion
    conex=None
#Datos venta
    id_Venta=0
    f_h_venta=None
    monto_venta=0.0
    borrado=0
    fechaBorrado=None
    observacion=""
    tiposDePago_id_tipo_pago=0
    caja=0
#turno
    id_Turno=0
#   turno=""
#   caja_ini_turno=0.0
#   fecha=0
#   f_h_apertura=0
#   f_h_cierre=0
#   id_usu=0
# tipo de Pago 0=Efectivo - 1=Targeta de Débito - 2=Targeta de Crédito
    tipoDePago=["Efectivo", "Targeta de Débito", "Targeta de Crédito"]

    def _init_(self, turno, caja):
        self.id_Turno=turno
        self.caja=caja
        self.conex=conexion()
        self.f_h_venta=FechayHora()
        self.fechaBorrado=FechayHora()
        pass

    def cargarVenta(self, lista2):
        #La lista viene con montoDeVenta(float), observación,idTurno,tipoPago,Caja        
        self.lista = lista2

        #pongo en 0 borrado y fecha de borrado
        (self.lista).insert(2,0)
        (self.lista).insert(3,"")   

        #formateo fecha y hora actuales
        self.f_h_venta.resetear()
        (self.lista).insert(0, ((self.f_h_venta).getAhoraGuardo()))

        self.conex.insert(self.lista, "Ventas")
        pass

    def borrarVenta(self):
        pass

    def ListarVentas(self):
        pass

    def BuscarVentas(self):
        pass
    

class Venta(App):
    def build(self):
                return Box()
        
if __name__ == "__main__":
    Venta().run()

