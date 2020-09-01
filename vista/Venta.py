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
    diccTipoPago={'1' : "Efectivo", '2' : "Débito", '3' : "Crédito"}
    turno=""
    caja=0
    tipoPago=1
    mont=False
    Pago=False
    cont=0
    user=[]
    sesion=[]
    turnos=[]
    turnoActual=[]
    ventas=[]
    controlaVentanaAbirta=0
    idUltimaVenta=''
    horaUltima=''

    def __init__(self, **kwargs):         
        super().__init__(**kwargs)
        self.inicio()           

    def inicio(self):
        #========================MANEJO EVENTOS DE TECLADO===========================
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        
        #========================SETEO PROGRAMA===========================
        self.focoComponentes()   
        self.setearTablita()

    #========================MANEJO EVENTOS DE TECLADO===========================
    #-----------------MANEJO Esc-----------------
    def _keyboard_closed(self):
        pass

            
#---------EFECTOS DE TECLADO PARA CAJA 1--------
    def enter(self, n):
        if n == 1:
            if self.ids.timonto.text!=None:
                self.ids.timonto.focus=False
                self.ids.tiPago.focus=True
                self.mont=True
        elif n == 2: 
            if self.ids.tiPago.text!=None and self.mont:
                self.ids.tiPago.focus=False
                self.ids.lbAnterior.text=self.ids.timonto.text                
                self.ids.lbPagoAnterior.text=self.diccTipoPago[str(self.tipoPago)]
                self.btnRegistrarVenta()
                self.ids.timonto.text=""
                self.ids.tiPago.text=""
                self.ids.lbPago.text="Efectivo"
                self.ids.timonto.focus=True
                self.Pago=False
                self.mmont=False

    #----------MANEJO DISTINTAS TECLAS-----------
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        teclas = {
            'numpadsubstract': self.btnBorrar, # '-'
            'numpadadd': self.seteoVenta,      # '+'
            'numpaddivide': self.verTabl,      # '/'
            'numpadmul': self.cajaA,           # '*'            
        }
        if keycode[1] in teclas:
            teclas[keycode[1]]()

    #----------BORRAR ÚLTIMA VENTA (PIDE JUSTIFICACIÓN)('-')-----------
    def btnBorrar(self):
        if self.controlaVentanaAbirta==0:
            self.controlaVentanaAbirta=1
            try:
                if self.horaUltima != '':                 
                    self.ventas=conexion().selectAll('Ventas', ['f_h_venta', self.horaUltima])
                    contenido = BoxLayout(orientation='vertical')
                    lala = Label(text = 'Hora de registro: ' + self.ventas[0][1], font_size =20.0)
                    lala1 = Label(text = 'Monto de venta:   $ ' + str(self.ventas[0][2]), font_size =20.0)
                    lala2 = Label(text = 'Tipo de Pago:     ' + self.diccTipoPago[self.ventas[0][7]], font_size =20.0)
                    lala3 = Label(text = 'Tipo de Pago:     ' + str(self.ventas[0][8]), font_size =20.0)
                    ticontr = TextInput(hint_text="Justificación", font_size=20.0)        
                    ticontr.multiline=False
                            
                    but = BoxLayout(orientation='horizontal')
                    but.add_widget(Button(text="Borrar" ,on_release = lambda *args: (self.borrarVenta(ticontr.text, bano)), background_normal= 'normal.png', background_color= (1, .745, .039, 1), font_size =25.0))       
                    but.add_widget(Button(text="Salir",on_press = lambda *args: (bano.dismiss(), self.contrl()), background_normal= 'normal.png', background_color= (1, .745, .039, 1), font_size =25.0))
                    
                    contenido.add_widget(lala)
                    contenido.add_widget(lala1)
                    contenido.add_widget(lala2)
                    contenido.add_widget(lala3)
                    contenido.add_widget(ticontr)

                    ticontr.on_text_validate = lambda *args: (self.borrarVenta(ticontr.text, bano))
                    ticontr.focus=True

                    contenido.add_widget(but)
                    bano = Popup(title= 'Borrar última venta', content= contenido, size_hint=(None,None),auto_dismiss=False, size=(420, 170), background='Fondop.png', separator_color=(1, .745, .039, 1), title_size=25.0, separator_height=5.0)
                    bano.open()
            except:
                    contenido = BoxLayout(orientation='vertical')
                    lala = Label(text = "No hay un registro de venta realizada /n durante la ejecución, le sugiero que /nverifique si existe un turno en ejecución,/n o bien acceda a gestionar registros." + self.ventas[0][1], font_size =20.0)                            
                    but=Button(text="Salir",on_press = lambda *args: (msg.dismiss(), self.contrl()), background_normal= 'normal.png', background_color= (1, .745, .039, 1), font_size =25.0)
                    
                    contenido.add_widget(lala)
                    contenido.add_widget(but)
                    msg = Popup(title= 'No hay registro', content= contenido, size_hint=(None,None),auto_dismiss=False, size=(420, 170), background='Fondop.png', separator_color=(1, .745, .039, 1), title_size=25.0, separator_height=5.0)
                    msg.open()
    
    #-----------REGISTRO VENTA----------------
    def btnRegistrarVenta(self):
        self.horaUltima=FechayHora().formatos(11)
        con=conexion()
        con.insert([self.horaUltima, float(self.ids.timonto.text), '0', '','', int(self.turnoActual[0]), self.tipoPago, 1 ], 'Ventas')

    #----------BORRAR ÚLTIMA VENTA-----------
    def borrarVenta(self, obs, pop):
        self.ventas[0][3]='1'
        self.ventas[0][4]=FechayHora().formatos(11)
        self.ventas[0][5]=obs
        conexion().update('Ventas', self.ventas[0])
        self.seteoVenta
        self.ids.lbAnterior.text=''              
        self.ids.lbPagoAnterior.text=''
        self.contrl()
        pop.dismiss()
    
    #---BANDERA PARA SABER SI HAY UN POPUP ABIERTO---
    def contrl(self):
        if self.controlaVentanaAbirta==1:
            self.controlaVentanaAbirta=0

    #----------SETEO CAJA 1 ('+')-----------
    def seteoVenta(self):
        self.ids.timonto.text=""
        self.ids.tiPago.text=""
        self.ids.lbPago.text="Efectivo"
        self.ids.timonto.focus=True
        self.Pago=False
        self.mmont=False
        
    #----------MUESTRO U OCULTO RESUMEN ('/')-----------
    def verTabl(self):        
        if self.ids.tgbEstado.state=='down':
            self.ids.tgbEstado.state='normal'
        else:
            self.ids.tgbEstado.state='down'
        self.estado()

    #-----MUESTRO U OCULTO CONTROLES DE LA TABLA------
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

    #---------------SETEO TABLA DE RESUMEN------------
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

    #----------FUNCION PARA:('*')(FUNCION DOBLE)-----------
    #-------SI NO HAY TURNO INICIADO INICIA UNO NUEVO-------
    def cajaA(self):
        if self.controlaVentanaAbirta==0:
            try:
                self.turnos = conexion().selectAll('Turnos', ['estado', str(1)])
                if len(self.turnos[0])>0:
                    self.ids.cajaa.active = not self.ids.cajaa.active                    
                    self.openPopup(1)
            except:
                self.btnGestionarTurno()

    #---------SEGURIDAD PARA HABILITAR CAJA--------
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

    #-----------DESHABILITO CAJA 1-----------
    def desact(self):
        self.ids.cajaa.active=False

    #----------HABILITO CAJA 1----------------
    def activoCaja(self, a, pop, al):
        if al:
            if a==1:
                self.ids.timonto.disabled = not self.ids.cajaa.active
                self.ids.lbAnterior.disabled = not self.ids.cajaa.active
                self.ids.tiPago.disabled = not self.ids.cajaa.active
                self.ids.lbPago.disabled= not self.ids.cajaa.active
                self.ids.lbPagoAnterior.disabled = not self.ids.cajaa.active
                self.ids.timonto.focus=True
        else:
            self.ids.cajaa.active=False
        pop.dismiss()

    #====================FUNCIONALES==================
    #----------------CAMBIO TIPO DE PAGO--------------
    def filtro(self):  
        if len(self.ids.tiPago.text) > 1:
            self.ids.tiPago.text=""
            self.Pago=False
            self.ids.lbPago.text="Efectivo"
        elif len(self.ids.tiPago.text) == 0:
            self.ids.lbPago.text="Efectivo"
        elif (int(self.ids.tiPago.text)) in range(1,4):   
            self.tipoPago=int(self.ids.tiPago.text)
            self.ids.lbPago.text=str(self.diccTipoPago[str(self.tipoPago)])
        else:
            self.ids.tiPago.text="1"
            self.tipoPago=1
            self.ids.lbPago.text="Efectivo"
            
    #-------------FOCO PARA COMPONENTE--------------
    def focoComponentes(self):  
        self.ids.timonto.focus=True

    #-----------DEVUELVE LA VENTA TOTAL DEL TURNO-------        
    def dameVenta(self):
        self.ventas = conexion().selectAll('Ventas', ['Turnos_id_turno', self.turnoActual[0]])
        contVent=0
        for i in range(len(self.ventas)):
            if self.ventas[i][3]=='0':
                contVent+=int(self.ventas[i][2])
        return contVent

    #--------CIERRA UN TURNO Y MUESTRA RESULTADO----------
    def cerrarTurno(self, pop, popup):
        popup.dismiss()
        pop.dismiss()
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
        lbInicial  = Label(text='$ ' + str(self.turnoActual[2]), font_size =20.0)   
        
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

    #------------PIDO CONFIRMACION PARA CERRAR TURNO------------
    def confirmo(self, pop):
        self.contrl()
        if self.controlaVentanaAbirta==0:
            self.controlaVentanaAbirta=1
            cont = BoxLayout(orientation='vertical')
            buttons = BoxLayout()
            cont.add_widget(Label(text='¿Desea dar por terminado el turno ' + self.turnoActual[1] + '?', font_size =20.0))
            buttons.add_widget(Button(text='si', on_press = lambda btn: self.cerrarTurno(mensj, pop), background_normal= 'normal.png', background_color= (1, .745, .039, 1), font_size =25.0) )
            buttons.add_widget(Button(text='no',on_press = lambda *args: mensj.dismiss(), background_normal= 'normal.png', background_color= (1, .745, .039, 1), font_size =25.0) )
            cont.add_widget(buttons)
            mensj = Popup(title="Confirmar", content= cont,auto_dismiss=False, size_hint=(None,None), size=(480, 150), background='Fondop.png', separator_color=(1, .745, .039, 1), title_size=25.0, separator_height=5.0)
            mensj.open()

    #-------------------------ABRO TURNO----------------------------
    def nuevoTurno(self, estr, pop):
        self.controlaVentanaAbirta=1
        self.user=conexion().selectAll("Usuarios", ["sesion", "1"])
        self.sesion=self.user[0]
        tourno='Mañana'
        if datetime.now().hour>13:
            tourno='Tarde'
        conexion().insert([tourno, estr, FechayHora().formatos(10), FechayHora().formatos(11), "s", self.sesion[0], 1], 'Turnos')
        self.setearTablita()
        self.contrl()
        pop.dismiss()

    #-------------------GESTION DE TURNO-----------------
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
                but.add_widget(Button(text="Cerrar" ,on_release = lambda *args: self.confirmo(logueo), background_normal= 'normal.png', background_color= (1, .745, .039, 1), font_size =25.0))       
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

class Venta(App):
    def build(self):
                return Box()   
        
if __name__ == "__main__":
    Venta().run()

