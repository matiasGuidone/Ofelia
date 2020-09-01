import os
import sys

from kivy.app import App
# configuration
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button 
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton

import sys, os
import platform
sys.path.append(os.getcwd())
from modelo.conexion import conexion 
Config.set("graphics", "window_state",  'maximized')
#Config.set("graphics", "width",  640)
#Config.set("graphics", "height", 480)


from kivy.uix.colorpicker import ColorPicker

class Principal(BoxLayout):
    user = []
    sesion = []
    abrir=0

    def __init__(self, **kwargs):
        super().__init__(**kwargs) 
        self.verificoUsuarioIniciado()

    def verificoUsuarioIniciado(self):
        self.user = conexion().selectAll('Usuarios', ['sesion', str(1)])
        if len(self.user)>0:
            self.sesion=self.user[0]
            conexion().update([self.sesion[1], self.sesion[2],self.sesion[3], 0, self.sesion[0]],'Usuarios')
            self.user = []
            self.sesion = []

    
    def cargoPrograma(self):        
        self.abrir=2
        if len(self.user) == 0 :
            self.openPopup()
        elif self.user[0][2]== 'admin' or self.user[0][2]== 'caja-pagos':
            but = BoxLayout(orientation='vertical')
            usu=Button(text="Gestionar Usuario" , on_release = lambda *args: self.btnUsuarios(), size_hint_y = None, height = 50, background_normal= 'normal.png', background_color= (1, .745, .039, 1), font_size =25.0)
            cie=Button(text="Cerrar Sesión" , on_release = lambda *args: self.btnCierroSesion(popUsu,True), size_hint_y = None, height = 50, background_normal= 'normal.png', background_color= (1, .745, .039, 1), font_size =25.0)
            sal=Button(text="Salir",on_release = lambda *args: popUsu.dismiss(), background_normal= 'normal.png', size_hint_y = None, height = 50, background_color= (1, .745, .039, 1), font_size =25.0)
            but.add_widget(usu)
            but.add_widget(cie)
            but.add_widget(sal)
            popUsu = Popup(title= 'Programa', content= but, size_hint=(None,None),auto_dismiss=False, size=(300, 250), background='Fondop.png', separator_color=(1, .745, .039, 1), title_size=25.0, separator_height=5.0)
            popUsu.open()
        elif self.user[0][2]== 'caja':
            but = BoxLayout(orientation='vertical')
            cie=Button(text="Cerrar Sesión" , on_release = lambda *args: self.btnCierroSesion(popUsu,True), size_hint_y = None, height = 50, background_normal= 'normal.png', background_color= (1, .745, .039, 1), font_size =25.0)
            sal=Button(text="Salir",on_release = lambda *args: popUsu.dismiss(), background_normal= 'normal.png', size_hint_y = None, height = 50, background_color= (1, .745, .039, 1), font_size =25.0)
            but.add_widget(cie)
            but.add_widget(sal)
            popUsu = Popup(title= 'Programa', content= but, size_hint=(None,None),auto_dismiss=False, size=(300, 200), background='Fondop.png', separator_color=(1, .745, .039, 1), title_size=25.0, separator_height=5.0)
            popUsu.open()
        pass       

    def btnCierroSesion(self, pop, v):
        conexion().update([self.sesion[1], self.sesion[2],self.sesion[3], 0, self.sesion[0]],'Usuarios')
        self.user = []
        self.sesion = []
        self.abrir=0
        pop.dismiss()

    def openPopup(self):
        #armado de popup 
        contenido = BoxLayout(orientation='vertical')

        #campos de llenado        
        tiuser = TextInput(hint_text="Nombre de usuario")
        ticontr = TextInput(hint_text="Contraseña", password = True)        
        ticontr.multiline=False
        tiuser.multiline=False
        
        but = BoxLayout(orientation='horizontal')
        but.add_widget(Button(text="Ingresar" ,on_release = lambda *args: self.iniciar(tiuser.text, ticontr.text, logueo), background_normal= 'normal.png', background_color= (1, .745, .039, 1), font_size =25.0))       
        but.add_widget(Button(text="Salir",on_press = lambda *args: logueo.dismiss(), background_normal= 'normal.png', background_color= (1, .745, .039, 1), font_size =25.0))
        
        contenido.add_widget(tiuser)
        contenido.add_widget(ticontr)

        contenido.add_widget(but)
        logueo = Popup(title= 'Logueo', content= contenido, size_hint=(None,None),auto_dismiss=False, size=(420, 170), background='Fondop.png', separator_color=(1, .745, .039, 1), title_size=25.0, separator_height=5.0)
        logueo.open()


    def iniciar(self, usuario, contr, popup):        
        self.user = conexion().selectAll('Usuarios',['nombre_usu',"'"+usuario+"'",'contraseña', "'"+contr+"'"])
        if len(self.user) == 0:
            contenido = BoxLayout(orientation='vertical')
            contenido.add_widget(Label(text=str("Usuario o contraseña errónea"),color= (0, 0, 0, 1)))
            contenido.add_widget(Button(text='Aceptar', on_press = lambda *args: popup.dismiss(), background_normal= 'normal.png', background_color= (1, .745, .039, 1), font_size =25.0))
            popup = Popup(title="Mensaje", content= contenido, size_hint=(None,None),auto_dismiss=False, size=(400, 130), background='Fondop.p', separator_color=(1, .745, .039, 1), title_size=25.0, separator_height=5.0)
            popup.open()
        else:  
            self.sesion=self.user[0]     
            conexion().update([self.sesion[1], self.sesion[2],self.sesion[3], 1, self.sesion[0]],'Usuarios')
            popup.dismiss()
            self.abrirVentana()
            print(self.sesion)
        pass

    def btnVentas(self):
        self.abrir=1
        if len(self.user) == 0 :
            self.openPopup()
        else:        
            os.system("python vista/Venta.py")
        pass

    def btnUsuarios(self):
        if self.user[0][2]== 'admin':
            os.system('python vista/usuario.py')
        pass

    def btnReporte(self):
        self.abrir=5
        if len(self.user) == 0 :
            self.openPopup()
        elif self.user[0][2]== 'admin':
            os.system('python vista/reportes.py')
        pass

    def btnCuentas(self):
        self.abrir=3
        if len(self.user) == 0 :
            self.openPopup()
        elif self.user[0][2]== 'admin':
            os.system('python vista/registrocuentas.py')
        pass

    def btnPagos(self):
        self.abrir=4
        if len(self.user) == 0 :
            self.openPopup()
        elif self.user[0][2]== 'admin' or self.user[0][2]== 'caja-pagos':
            os.system('python vista/registrogasto.py')
        pass

    def abrirVentana(self):
        if self.abrir==1:    
            os.system("python vista/Venta.py")
        elif self.abrir==2:
            self.cargoPrograma()
        elif self.abrir==3:
            os.system('python vista/registrocuentas.py')
        elif self.abrir==4:
            os.system('python vista/registrogasto.py')
        elif self.abrir==5:
            os.system('python vista/reportes.py')

class PrincipalApp(App):
    def build(self):
            prin = Principal()
            return prin
            # sm = ScreenManager()
            # vent = Screen(name='ventas')
            # vent.add_widget(Box())

            # cuent = Screen(name='cuentas')
            # cuent.add_widget(RegistroCuentas())

            # pag = Screen(name='pagos')
            # pag.add_widget(RegistroGasto())

            # # usu = Screen(name='usuarios')
            # # usu.add_widget(Usuario())

            # men = Screen(name='menu')
            # men.add_widget(Principal())

            # sm.add_widget(cuent)
            # sm.add_widget(pag)
            
            # sm.add_widget(vent)
            # # sm.add_widget(usu)  
            # sm.add_widget(men) 
            # sm.current = 'pagos' 
            # return sm 
if __name__ == "__main__":
    PrincipalApp().run()
