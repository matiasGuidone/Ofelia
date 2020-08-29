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
    sistema=None
    dropdown=None
    diccTipoPago={'0' : "Efectivo", '1' : "Débito", '2' : "Crédito"}
    turno=""
    caja=0
    tipoPago=0
    mont=False
    Pago=False
    cont=0
    user=[]
    sesion=[]
    turnos=[]
    turnoActual=[]

    def __init__(self, **kwargs):         
        super().__init__(**kwargs)
        self.inicio() 
        
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
        self.cont += 1
        print ("Borro venta " + str(self.cont))

    def inicio(self):

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        self.turno=0#consulto en base de datos
        self.caja=0 
        self.focoComponentes()   
        self.ids.cajaa.active=False
    #    self.ids.cajab.active=False
        self.activoCaja(1)
    #    self.activoCaja(2)

    def _keyboard_closed(self):
        pass

    def seteoVenta(self):
        self.ids.timonto.text=""
        self.ids.tiPago.text=""
        self.ids.lbPago.text="Efectivo"
        self.ids.timonto.focus=True
        self.Pago=False
        self.mmont=False

        self.cont += 1
        print ("Seteo venta " + str(self.cont))

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        
        print ("Pruebo venta " + str(keycode[1]))

        teclas = {
            'numpadsubstract': self.btnBorrar,
            'numpadadd': self.seteoVenta,
            '/': self.btnGestionarTurno,
        }

        if keycode[1] in teclas:
            teclas[keycode[1]]()

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
        #self.ids.Scat(do_rotation=False)   
        #self.ids.timonto(hint_text = "Monto" )
        #self.ids.timonto(hint_text = "Tipo de Pago" )
        #self.ids.tiPago(hint_text = "Observación" )
        self.ids.timonto.multiline=False
      #  self.ids.tiobservacion.multiline=False
        self.ids.timonto.focus=True

    def activoCaja(self, a):
        if a==1:
            self.ids.timonto.disabled = not self.ids.cajaa.active
            self.ids.lbAnterior.disabled = not self.ids.cajaa.active
            self.ids.tiPago.disabled = not self.ids.cajaa.active
            self.ids.lbPago.disabled= not self.ids.cajaa.active
            self.ids.lbPagoAnterior.disabled = not self.ids.cajaa.active
         #   self.ids.tiobservacion.disabled = not self.ids.cajaa.active
         #   self.ids.lbobserAnt.disabled = not self.ids.cajaa.active
            self.ids.timonto.focus=True
    #   else:
    #       self.ids.timontob.disabled = not self.ids.cajab.active
    #       self.ids.lbAnteriorb.disabled = not self.ids.cajab.active
    #       self.ids.tiPagob.disabled = not self.ids.cajab.active
    #       self.ids.lbPagob.disabled = not self.ids.cajab.active
    #       self.ids.lbPagoAnteriorb.disabled = not self.ids.cajab.active
    #       self.ids.tiobservacionb.disabled = not self.ids.cajab.active
    #       self.ids.lbobserAntb.disabled = not self.ids.cajab.active
    
    #Muestro estado de cajas
    def estado(self):
        if self.ids.tgbEstado.state=='down':
            self.ids.lbhora.color=(0,0,0,1)
            self.ids.lbAbri.color=(0,0,0,1)
            self.ids.lbltotal.color=(0,0,0,1)
            self.ids.lbtot.color=(0,0,0,1)
            self.ids.lblventa.color=(0,0,0,1)
            self.ids.lbvent.color=(0,0,0,1)
            self.ids.lblinicial.color=(0,0,0,1)
            self.ids.laIni.color=(0,0,0,1)
            self.ids.lbtitu.color=(0,0,0,1)
        else:            
            self.ids.lbhora.color=(1,1,1,1)
            self.ids.lbAbri.color=(1,1,1,1)
            self.ids.lbltotal.color=(1,1,1,1)
            self.ids.lbtot.color=(1,1,1,1)
            self.ids.lblventa.color=(1,1,1,1)
            self.ids.lbvent.color=(1,1,1,1)
            self.ids.lblinicial.color=(1,1,1,1)
            self.ids.laIni.color=(1,1,1,1)
            self.ids.lbtitu.color=(1,1,1,1)
        pass
#Falta estado de turno
    def btnGestionarTurno(self):
        self.user = conexion().selectAll('Turnos', ['sesion', str(1)])
        self.sesion=self.user[0]
        if
            self.user = conexion().selectAll('Usuarios', ['sesion', str(1)])
            self.sesion=self.user[0]





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
            #    self.ids.tiobservacion.focus=True                
                
                
            #esto no estaría con observacion                    
                self.ids.lbAnterior.text=self.ids.timonto.text                
                self.ids.lbPagoAnterior.text=self.diccTipoPago[str(self.tipoPago)]
            
                #Guardar en base
                self.btnRegistrarVenta()
                self.ids.timonto.text=""
                self.ids.tiPago.text=""
                self.ids.lbPago.text="Efectivo"
                self.ids.timonto.focus=True
                self.Pago=False
                self.mmont=False
      #elif n == 3:
      #    if self.mont and self.Pago:
      #        self.ids.tiobservacion.focus=False
      #        self.ids.lbAnterior.text=self.ids.timonto.text
      #        print(self.ids.timonto.text)
      #        self.ids.lbPagoAnterior.text=self.diccTipoPago[str(self.tipoPago)]
      #        print(self.diccTipoPago[str(self.tipoPago)])
      #        self.ids.lbobserAnt.text=self.ids.tiobservacion.text
      #        print(self.ids.tiobservacion.text)
      #    
      #        #Guardar en base
      #        self.btnRegistrarVenta()
      #        self.ids.timonto.text=""
      #        self.ids.tiobservacion.text=""
      #        self.ids.tiPago.text=""
      #        self.ids.lbPago.text="Efectivo"
      #        self.ids.timonto.focus=True
      #        self.Pago=False
      #        self.mmont=False


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

