import os
import sys

from datetime import datetime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from modelo.conexion import conexion
from modelo.conexion import FechayHora

sys.path.append(os.getcwd())

class Box(BoxLayout):
    pass

class Venta(App):
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

    def borrarVenta(self):
        pass

    def ListarVentas(self):
        pass

    def BuscarVentas(self):
        pass
    
    def build(self):
        return Box()

        
if __name__ == "__venta__":
    Venta().run()