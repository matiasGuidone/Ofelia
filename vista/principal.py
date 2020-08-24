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
    abrir=0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)  

    def openPopup(self):
        #armado de popup 
        contenido = BoxLayout(orientation='vertical')

        #campos de llenado        
        tiuser = TextInput(hint_text="Nombre de usuario")
        ticontr = TextInput(hint_text="Contraseña", password = True)        
        ticontr.multiline=False
        tiuser.multiline=False
        
        but = BoxLayout(orientation='horizontal')
        but.add_widget(Button(text="Ingresar" ,on_press = lambda *args: self.iniciar(tiuser.text, ticontr.text, logueo), background_normal= 'normal.png', background_color= (1, .745, .039, 1), font_size =25.0))       
        but.add_widget(Button(text="Salir",on_press = lambda *args: logueo.dismiss(), background_normal= 'normal.png', background_color= (1, .745, .039, 1), font_size =25.0))
        
        contenido.add_widget(tiuser)
        contenido.add_widget(ticontr)

        contenido.add_widget(but)
        logueo = Popup(title= 'Logueo', content= contenido, size_hint=(None,None),auto_dismiss=False, size=(420, 170))
        logueo.open()
        
        pass


    def iniciar(self,usuario, contr, popup):
        self.user = conexion().selectAll('Usuarios',['nombre_usu',"'"+usuario+"'",'contraseña', "'"+contr+"'"])
        if len(self.user) == 0:
            contenido = BoxLayout(orientation='vertical')
            contenido.add_widget(Label(text=str("Usuario o contraseña errónea")))
            contenido.add_widget(Button(text='Aceptar', on_press = lambda *args: popup.dismiss(), background_normal= 'normal.png', background_color= (1, .745, .039, 1), font_size =25.0))
            popup = Popup(title="Mensaje", content= contenido, size_hint=(None,None),auto_dismiss=False, size=(400, 130))
            popup.open()
        else:
            popup.dismiss()
            self.abrirVentana()
        pass

    def btnVentas(self):
        self.abrir=1
        if len(self.user) == 0 :
            self.openPopup()
        else:        
            os.system("python vista/Venta.py")
        pass

    def btnUsuarios(self):
        self.abrir=2 
        if len(self.user) == 0 :
            self.openPopup()
        elif self.user[0][2]== 'admin':
            os.system('python vista/usuario.py')
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
            os.system('python vista/usuario.py')
        elif self.abrir==3:
            os.system('python vista/registrocuentas.py')
        elif self.abrir==4:
            os.system('python vista/registrogasto.py')

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
