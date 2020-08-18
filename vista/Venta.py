import os
import sys
import platform
from datetime import datetime

from kivy.app import App
# configuration
from kivy.config import Config
Config.set("graphics", "window_state",  'maximized')
#Config.set("graphics", "height", 110)
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
sys.path.append(os.getcwd())
from modelo.conexion import conexion
from modelo.FechayHora import FechayHora


#damian
class Box(BoxLayout):
    pass
    sistema=None
    dropdown=None
    diccTipoPago={'0' : "Efectivo", '1' : "Débito", '2' : "Crédito"}
    turno=""
    caja=0
    tipoPago=0
    mont=False
    Pago=False

    def __init__(self, **kwargs):         
        super().__init__(**kwargs)
        self.inicio() 
        pass
        
    def btnRegistrarVenta(self):
        #v = AccionVentas(self.turno, self.caja)
#montoDeVenta(float), observación,idTurno,tipoPago,Caja
        #v.cargarVenta([])
        print ("registro venta")

    def btnBorrar(self):
        #self.ids.lblSubcate.text = "Registrar"
        #v=AccionVentas(turno, caja)
#montoDeVenta(float), observación,idTurno,tipoPago,Caja
        #v.cargarVenta([])
        print ("Borro venta")

    def inicio(self):
        self.turno=0#consulto en base de datos
        self.caja=0 
        self.focoComponentes()   
        

    def filtro(self):  
        if len(self.ids.tiPago.text) > 1:
            self.ids.tiPago.text=""
            self.Pago=False
            self.ids.lbPago.text="Efectivo"
        elif len(self.ids.tiPago.text) == 0:
            self.ids.lbPago.text="Efectivo"
        elif (int(self.ids.tiPago.text)) in range(1,4):   
            self.tipoPago=(int(self.ids.tiPago.text)-1)
            self.ids.lbPago.text=str(self.diccTipoPago[str(self.tipoPago)])
        else:
            self.ids.tiPago.text="1"
            self.tipoPago=0
            self.ids.lbPago.text="Efectivo"
            
        
    def focoComponentes(self):        
        self.ids.timonto.multiline=False
        self.ids.tiobservacion.multiline=False
        self.ids.timonto.focus=True
    

# Manejo escucha de teclado
    def enter(self, n):
        if n == 1:
            if self.ids.timonto.text!=None:
                self.ids.timonto.focus=False
                self.ids.tiPago.focus=True
                self.mont=True
        elif n == 2: 
            if self.ids.tiPago.text!=None and self.mont:
                self.ids.tiPago.focus=False
                self.ids.tiobservacion.focus=True
                self.Pago=True
        elif n == 3:
            if self.mont and self.Pago:
                self.ids.tiobservacion.focus=False
                self.ids.lbAnterior.text=self.ids.timonto.text
                print(self.ids.timonto.text)
                self.ids.lbPagoAnterior.text=self.diccTipoPago[str(self.tipoPago)]
                print(self.diccTipoPago[str(self.tipoPago)])
                self.ids.lbobserAnt.text=self.ids.tiobservacion.text
                print(self.ids.tiobservacion.text)
            
                #Guardar en base
                self.btnRegistrarVenta()
                self.ids.timonto.text=""
                self.ids.tiobservacion.text=""
                self.ids.tiPago.text=""
                self.ids.lbPago.text="Efectivo"
                self.ids.timonto.focus=True
                self.Pago=False
                self.mmont=False


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

