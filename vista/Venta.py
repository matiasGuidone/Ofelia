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
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
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
    ventas=[]
    controlaVentanaAbirta=0

    def __init__(self, **kwargs):         
        super().__init__(**kwargs)
        self.inicio() 
        
    def btnRegistrarVenta(self):
        #v = AccionVentas(self.turno, self.caja)
        #montoDeVenta(float), observación,idTurno,tipoPago,Caja
        #v.cargarVenta([])
        print ("registro venta")

    def btnBorrar(self):
        
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
        self.setearTablita()
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
        

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        teclas = {
            'numpadsubstract': self.btnBorrar,
            'numpadadd': self.seteoVenta,
            'numpaddivide': self.verTabl,
            'numpadmul': self.cajaA,
            
        }

        if keycode[1] in teclas:
            teclas[keycode[1]]()

    def verTabl(self):        
        if self.ids.tgbEstado.state=='down':
            self.ids.tgbEstado.state='normal'
        else:
            self.ids.tgbEstado.state='down'
        self.estado()

    def cajaA(self):
        if self.controlaVentanaAbirta==0:
            try:
                self.turnos = conexion().selectAll('Turnos', ['estado', str(1)])
                if len(self.turnos[0])>0:
                    self.ids.cajaa.active = not self.ids.cajaa.active                    
                    self.openPopup(1)
            except:
                self.btnGestionarTurno()

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

    def openPopup(self, a):
        if self.controlaVentanaAbirta==0:
            self.controlaVentanaAbirta=1
            if self.ids.cajaa.active:  
                self.user=conexion().selectAll('Usuarios', ['sesion', 1])
                self.sesion=self.user[0]
                contenido = BoxLayout(orientation='vertical')
                lala = Label(text = self.sesion[1], font_size =25.0)
                ticontr = TextInput(hint_text="Contraseña", password = True)        
                ticontr.multiline=False
                        
                but = BoxLayout(orientation='horizontal')
                but.add_widget(Button(text="Acceder" ,on_release = lambda *args: self.activoCaja(a, bano, ticontr.text==self.sesion[3]), background_normal= 'normal.png', background_color= (1, .745, .039, 1), font_size =25.0))       
                but.add_widget(Button(text="Salir",on_press = lambda *args: (bano.dismiss(), self.desact(), self.contrl()), background_normal= 'normal.png', background_color= (1, .745, .039, 1), font_size =25.0))
                
                contenido.add_widget(lala)
                contenido.add_widget(ticontr)

                ticontr.on_text_validate = lambda *args: (self.activoCaja(a, bano, ticontr.text==self.sesion[3]), self.contrl())
                ticontr.focus=True

                contenido.add_widget(but)
                bano = Popup(title= 'Acceso', content= contenido, size_hint=(None,None),auto_dismiss=False, size=(420, 170), background='Fondop.png', separator_color=(1, .745, .039, 1), title_size=25.0, separator_height=5.0)
                bano.open()
            else:
                self.contrl()

    def desact(self):
        self.ids.cajaa.active=False

    def activoCaja(self, a, pop, al):
        if al:
            print("1")
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
        else:
            print("2")
            self.ids.cajaa.active=False
        pop.dismiss()

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
    
    def dameVenta(self):        
        self.turnos = conexion().selectAll('Turnos', ['estado', str(1)])
        self.turnoActual=self.turnos[0]        

        self.ventas = conexion().selectAll('Ventas', ['Turnos_id_turno', self.turnoActual[0]])
        contVent=0
        for i in range(len(self.ventas)):
            if self.ventas[i][3]=='0':
                contVent+=int(self.ventas[i][2])
        return contVent

    def cerrarTurno(self, pop):
        self.controlaVentanaAbirta=1
        fhf=FechayHora().formatos(11)
        conexion().update([self.turnoActual[1], self.turnoActual[2],self.turnoActual[3], self.turnoActual[4], fhf,  self.turnoActual[6], 0, self.turnoActual[0]],'Turnos')
        
        #Muestro un resumen del turno que se cerró
        contenido = BoxLayout(orientation='vertical')       
        con = BoxLayout(orientation='horizontal')
        lbF  = Label(text="Fecha: ", font_size =20.0)
        lbFecha  = Label(text=self.turnoActual[3], font_size =20.0)    

        con1 = BoxLayout(orientation='horizontal')
        lbT  = Label(text="Turno: ", font_size =20.0)
        lbTurno  = Label(text=self.turnoActual[1], font_size =20.0)  

        con2 = BoxLayout(orientation='horizontal') 
        lbI  = Label(text="Inicial: ", font_size =20.0)
        lbInicial  = Label(text='$ ' + self.turnoActual[2], font_size =20.0)   
        
        con3 = BoxLayout(orientation='horizontal') 
        lbC  = Label(text="Caja: ", font_size =20.0)
        lbCaja = Label(text='$ ' + str(self.dameVenta()), font_size =20.0)  

        con4 = BoxLayout(orientation='horizontal') 
        lbA = Label(text="Abierto: ", font_size =20.0)
        lbAbierto  = Label(text=self.turnoActual[4], font_size =20.0)   
        
        con6 = BoxLayout(orientation='horizontal') 
        lbB = Label(text="Cerrado: ", font_size =20.0)
        lbBa  = Label(text= fhf, font_size =20.0)   

        con5 = BoxLayout(orientation='horizontal') 
        lbin  = Label(text="Iniciado por: ", font_size =20.0)
        lbini  = Label(text=self.sesion[1], font_size =20.0)   
        
        but = BoxLayout(orientation='horizontal')
        but.add_widget(Button(text="Aceptar",on_press = lambda *args: (logueo.dismiss(), self.contrl()), background_normal= 'normal.png', background_color= (1, .745, .039, 1), font_size =25.0))
        
        con.add_widget(lbF)
        con.add_widget(lbFecha)
        con1.add_widget(lbT)
        con1.add_widget(lbTurno)
        con2.add_widget(lbI)
        con2.add_widget(lbInicial)
        con3.add_widget(lbC)
        con3.add_widget(lbCaja)
        con4.add_widget(lbA)
        con4.add_widget(lbAbierto)
        con5.add_widget(lbin)
        con5.add_widget(lbini)
        con6.add_widget(lbB)
        con6.add_widget(lbBa)

        contenido.add_widget(con)
        contenido.add_widget(con1)
        contenido.add_widget(con2)
        contenido.add_widget(con3)
        contenido.add_widget(con4)
        contenido.add_widget(con6)
        contenido.add_widget(con5)
        contenido.add_widget(but)

        logueo = Popup(title= 'Resumen del Turno', content= contenido, size_hint=(None,None),auto_dismiss=False, size=(420, 280), background='Fondop.png', separator_color=(1, .745, .039, 1), title_size=25.0, separator_height=5.0)
        logueo.open()
        
        #Deshabilitar controles y setear en 0

    def confirmo(self):
        if self.controlaVentanaAbirta==0:
            self.controlaVentanaAbirta=1
            cont = BoxLayout(orientation='vertical')
            buttons = BoxLayout()
            cont.add_widget(Label(text='¿ Desea dar por terminado el turno "'+self.turnoActual[1]+'" ?', font_size =20.0))
            buttons.add_widget(Button(text='si', on_press = lambda btn: self.cerrarTurno(mensj), background_normal= 'normal.png', background_color= (1, .745, .039, 1), font_size =25.0) )
            buttons.add_widget(Button(text='no',on_press = lambda *args: mensj.dismiss(), background_normal= 'normal.png', background_color= (1, .745, .039, 1), font_size =25.0) )
            cont.add_widget(buttons)
            mensj = Popup(title="Confirmar", content= cont,auto_dismiss=False, size_hint=(None,None), size=(480, 150), background='Fondop.png', separator_color=(1, .745, .039, 1), title_size=25.0, separator_height=5.0)
            mensj.open()
    
    def setearTablita(self):
        try:
            self.turnos = conexion().selectAll('Turnos', ['estado', str(1)])
            if len(self.turnos[0])>0:
                self.turnoActual=self.turnos[0]
                self.ids.lbtitu.text = 'Turno: ' + self.turnoActual[1]
                self.ids.lblinicial.text = '$ ' + str(self.turnoActual[2])
                self.ids.lblventa.text = '$ ' + str(self.dameVenta())
                self.ids.lbltotal.text = '$ ' + str(self.dameVenta()+int(self.turnoActual[2]))
                self.ids.lbhora.text = self.turnoActual[4]
                self.ids.cajaa.disabled=False
        except:            
            self.ids.lbtitu.text = 'Turno: '
            self.ids.lblinicial.text = '$ 0'
            self.ids.lblventa.text = '$ 0'
            self.ids.lbltotal.text = '$ 0'
            self.ids.lbhora.text = 'Cerrado'
            self.ids.cajaa.disabled=True


    def nuevoTurno(self, estr, pop):
        self.user=conexion().selectAll("Usuarios", ["sesion", "1"])
        self.sesion=self.user[0]
        tourno='Mañana'
        if datetime.now().hour>13:
            tourno='Tarde'
        conexion().insert([tourno, estr, FechayHora().formatos(10), FechayHora().formatos(11), "s", self.sesion[0], 1], 'Turnos')
        self.setearTablita()
        pop.dismiss()

    def contrl(self):
        if self.controlaVentanaAbirta==1:
            self.controlaVentanaAbirta=0

    def btnGestionarTurno(self):
        if self.controlaVentanaAbirta==0:
            self.controlaVentanaAbirta=1
            self.turnos = conexion().selectAll('Turnos', ['estado', str(1)])
            if len(self.turnos)>0:
                self.turnoActual=self.turnos[0]
                self.user=conexion().selectAll('Usuarios',['id_usu', self.turnoActual[6]])
                self.sesion=self.user[0]           

            contenido = BoxLayout(orientation='vertical')
            # me fijo si ya hay un turno abierto
            if len(self.turnoActual) > 0:
                #si abierto ofrezco cerrarlo mostrando los detalles del turno en un popup        
                con = BoxLayout(orientation='horizontal')
                lbF  = Label(text="Fecha: ", font_size =20.0)
                lbFecha  = Label(text=self.turnoActual[3], font_size =20.0)    

                con1 = BoxLayout(orientation='horizontal')
                lbT  = Label(text="Turno: ", font_size =20.0)
                lbTurno  = Label(text=self.turnoActual[1], font_size =20.0)  

                con2 = BoxLayout(orientation='horizontal') 
                lbI  = Label(text="Inicial: ", font_size =20.0)
                lbInicial  = Label(text='$ ' + str(self.turnoActual[2]), font_size =20.0)   
                
                con3 = BoxLayout(orientation='horizontal') 
                lbC  = Label(text="Caja: ", font_size =20.0)
                lbCaja = Label(text='$ ' + str(self.dameVenta()), font_size =20.0)  

                con4 = BoxLayout(orientation='horizontal') 
                lbA = Label(text="Abierto: ", font_size =20.0)
                lbAbierto  = Label(text=self.turnoActual[4], font_size =20.0)   

                con5 = BoxLayout(orientation='horizontal') 
                lbin  = Label(text="Iniciado por: ", font_size =20.0)
                lbini  = Label(text=self.sesion[1], font_size =20.0)   
                
                but = BoxLayout(orientation='horizontal')
                but.add_widget(Button(text="Cerrar" ,on_release = lambda *args: self.confirmo(), background_normal= 'normal.png', background_color= (1, .745, .039, 1), font_size =25.0))       
                but.add_widget(Button(text="Salir",on_press = lambda *args: (logueo.dismiss(), self.contrl()), background_normal= 'normal.png', background_color= (1, .745, .039, 1), font_size =25.0))
                
                con.add_widget(lbF)
                con.add_widget(lbFecha)
                con1.add_widget(lbT)
                con1.add_widget(lbTurno)
                con2.add_widget(lbI)
                con2.add_widget(lbInicial)
                con3.add_widget(lbC)
                con3.add_widget(lbCaja)
                con4.add_widget(lbA)
                con4.add_widget(lbAbierto)
                con5.add_widget(lbin)
                con5.add_widget(lbini)

                contenido.add_widget(con)
                contenido.add_widget(con1)
                contenido.add_widget(con2)
                contenido.add_widget(con3)
                contenido.add_widget(con4)
                contenido.add_widget(con5)
                contenido.add_widget(but)

                logueo = Popup(title= 'Cerrar Turno', content= contenido, size_hint=(None,None),auto_dismiss=False, size=(420, 300), background='Fondop.png', separator_color=(1, .745, .039, 1), title_size=25.0, separator_height=5.0)
                logueo.open()
            
            else:
                con = BoxLayout(orientation='horizontal')
                lbin  = Label(text='$', font_size =20.0) 
                tini = TextInput(hint_text="Caja inicial", font_size =20.0, multiline=False, input_filter = 'float', on_text_validate = lambda *args: self.nuevoTurno(tini.text, nuevoTurn))
                
                but = BoxLayout(orientation='horizontal')
                but.add_widget(Button(text="Abrir" ,on_release = lambda *args: self.nuevoTurno(tini.text, nuevoTurn), background_normal= 'normal.png', background_color= (1, .745, .039, 1), font_size =25.0))       
                but.add_widget(Button(text="Salir",on_press = lambda *args: (nuevoTurn.dismiss(), self.contrl()), background_normal= 'normal.png', background_color= (1, .745, .039, 1), font_size =25.0))
                
                con.add_widget(lbin)
                con.add_widget(tini)

                contenido.add_widget(con)
                contenido.add_widget(but)

                nuevoTurn = Popup(title= 'Abrir Turno', content= contenido, size_hint=(None,None),auto_dismiss=False, size=(420, 140), background='Fondop.png', separator_color=(1, .745, .039, 1), title_size=25.0, separator_height=5.0)
                nuevoTurn.open()
        







# Manejo escucha de teclado de caja
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

