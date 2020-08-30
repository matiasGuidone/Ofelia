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
from kivy.uix.screenmanager import ScreenManager, Screen
import sys, os
import platform
sys.path.append(os.getcwd())
from modelo.conexion import conexion 
Config.set("graphics", "window_state",  'maximized')
#Config.set("graphics", "width",  540)
#Config.set("graphics", "height", 300)

class Usuario(BoxLayout):
    pass
    id = 0
    tipo = ''
    user = []
    verSesion=[]
    sesion=[]
   
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cargarDrp()
        self.ids.btnEditar.disabled=True
        self.ids.btnEliminar.disabled=True
        pass

    def cargarDrp(self):
        datos = conexion().selectAll("Usuarios")        
        self.ids.drpUsuarios.clear_widgets()  
        sistema = platform.system() 

        for index in range(len(datos)): 
            btn = Button()
           
            if sistema == "Windows":
                btn = Button(text = '% d - ' % datos[index][0] + str(datos[index][1]), size_hint_y = None, height = 50, background_normal= 'normal.png', background_color= (1, .745, .039, 1), font_size =20.0) 
                btn.bind(on_press = lambda btn: self.selectUsuario(btn.text.rsplit("-",2)[0]))
            else:
                btn = Button(text = '% d - ' % index + str(datos[index][1]), size_hint_y = None, id = str(datos[index][0]), height = 50, background_normal= 'normal.png', background_color= (1, .745, .039, 1), font_size =20.0) 
                btn.bind(on_press = lambda btn: self.selectUsuario(btn.id))
            
            btn.bind(on_release = lambda btn: (self.ids.drpUsuarios.select(btn.text),self.deshabilitar())) 
            self.ids.drpUsuarios.add_widget(btn) 

        self.ids.btnMain.bind(on_release = self.ids.drpUsuarios.open) 
        self.ids.drpUsuarios.bind(on_select = lambda instance, x: setattr(self.ids.btnMain, 'text', x))        

    def deshabilitar(self):  
        self.ids.btnEditar.disabled=False
        self.ids.btnEliminar.disabled=False

    def selectUsuario(self,id):
        self.id = int(id)
        self.user = conexion().selectId(self.id, 'Usuarios') 

    def openPopup(self, titulo):
        #armado de popup 
        contenido = BoxLayout(orientation='vertical')
        #campos de llenado
        if self.id != 0:
            user = TextInput(hint_text="Nombre de usuario",text=self.user[0][1], font_size =25.0, multiline=False)
        else:
            user = TextInput(hint_text="Nombre de usuario", font_size =25.0, multiline=False)

        contr = TextInput(hint_text="Contraseña", password = True, font_size =25.0, multiline=False)
        contr2 = TextInput(hint_text="Repetir contraseña", password = True, font_size =25.0, multiline=False)
        but = BoxLayout(orientation='horizontal')
        but.add_widget(Button(text="Cancelar",on_press = lambda *args: popup.dismiss(), background_normal= 'normal.png', background_color= (1, .745, .039, 1), font_size =25.0))
        but.add_widget(Button(text="Guardar" ,on_press = lambda *args: self.guardarUser(user.text, contr.text, contr2.text, popup), background_normal= 'normal.png', background_color= (1, .745, .039, 1), font_size =25.0))
        tipos = BoxLayout() 
        tipos.add_widget(ToggleButton(text="Administrador",group = 'tipo', on_press = lambda btn: self.selectTipo("admin"), background_normal= 'normal.png', background_color= (1, .745, .039, 1), font_size =25.0)) 
        tipos.add_widget(ToggleButton(text="Caja", group = 'tipo', on_press = lambda btn: self.selectTipo("caja"), background_normal= 'normal.png', background_color= (1, .745, .039, 1), font_size =25.0))
        tipos.add_widget(ToggleButton(text="Caja-pagos", group = 'tipo', on_press = lambda btn: self.selectTipo("caja-pagos"), background_normal= 'normal.png', background_color= (1, .745, .039, 1), font_size =25.0))
        contenido.add_widget(user)
        contenido.add_widget(contr)
        contenido.add_widget(contr2)
        contenido.add_widget(tipos)
        contenido.add_widget(but)
        popup = Popup(title= titulo, content= contenido, size_hint=(None,None),auto_dismiss=False, size=(550, 300), background='Fondop.png', separator_color=(1, .745, .039, 1), title_size=25.0, separator_height=5.0)
        popup.open()
        pass

    def btnEditar(self):
        if len(self.user) == 0 :
            contenido = BoxLayout(orientation='vertical')
            contenido.add_widget(Label(text=str("Seleccione un usuario de la lista.")))
            contenido.add_widget(Button(text='Aceptar', on_press = lambda *args: popup.dismiss()), background_normal= 'normal.png', background_color= (1, .745, .039, 1), font_size =25.0)
            popup = Popup(title="Mensaje", content= contenido, size_hint=(None,None),auto_dismiss=False, size=(450, 130), background='Fondop.png', separator_color=(1, .745, .039, 1), title_size=25.0, separator_height=5.0)
            popup.open()
        else:
            self.openPopup("Editar el usuario")
        
        # param = [usuario_text, "admin", pass_text]
        # cone.insert(param,"Usuarios")
        pass

    def btnEliminar(self):
        if len(self.user) == 0 :
            contenido = BoxLayout(orientation='vertical')
            contenido.add_widget(Label(text=str("Seleccione un usuario de la lista.", background_normal= '', font_size =25.0)))
            contenido.add_widget(Button(text='Aceptar', on_press = lambda *args: popup.dismiss(), background_normal= 'normal.png', background_color= (1, .745, .039, 1), font_size =25.0))
            popup = Popup(title="Mensaje", content= contenido, size_hint=(None,None),auto_dismiss=False, size=(450, 130), background='Fondop.png', separator_color=(1, .745, .039, 1), title_size=25.0, separator_height=5.0)
            popup.open()
        else:    
            cont = BoxLayout(orientation='vertical')
            buttons = BoxLayout()
            cont.add_widget(Label(text='¿ Desea eliminar el usuario "'+self.user[0][1]+'" ?', font_size =25.0))
            buttons.add_widget(Button(text='si', on_press = lambda btn: self.elimina(mensj), background_normal= 'normal.png', background_color= (1, .745, .039, 1), font_size =25.0) )
            buttons.add_widget(Button(text='no',on_press = lambda *args: mensj.dismiss(), background_normal= 'normal.png', background_color= (1, .745, .039, 1), font_size =25.0) )
            cont.add_widget(buttons)
            mensj = Popup(title="Confirmar", content= cont,auto_dismiss=False, size_hint=(None,None), size=(480, 150), background='Fondop.png', separator_color=(1, .745, .039, 1), title_size=25.0, separator_height=5.0)
            mensj.open()
        
        # param = [usuario_text, "admin", pass_text]
        # cone.insert(param,"Usuarios")
        pass
    
    def elimina(self,popup):
        conexion().delete(self.id, 'Usuarios')
        popup.dismiss()
        self.cargarDrp()
        pass

    def btnNuevo(self):
        self.id = 0
        self.openPopup("Nuevo usuario")
        pass

    def selectTipo(self,tipo) :
        self.tipo = tipo
        pass

    def guardarUser(self, user, contr, contr2, popup):
        if contr == contr2 and self.id == 0:
            conexion().insert([user, self.tipo , contr], 'Usuarios')
            popup.dismiss()
            self.cargarDrp()
        elif contr == contr2 :
            conexion().update([user, self.tipo , contr, self.id], 'Usuarios')
            popup.dismiss()
            self.cargarDrp()
        else:
            contenido = BoxLayout(orientation='vertical')
            contenido.add_widget(Label(text=str("Las contraseñas ingresadas deben ser idénticas"), font_size =25.0))
            contenido.add_widget(Button(text='Aceptar', on_press = lambda *args: popup.dismiss(), background_normal= 'normal.png', background_color= (1, .745, .039, 1), font_size =25.0))
            popup = Popup(title="Mensaje", content= contenido, size_hint=(None,None),auto_dismiss=False, size=(450, 130), background='Fondop.png', separator_color=(1, .745, .039, 1), title_size=25.0, separator_height=5.0)
            popup.open()
        pass

	# def btnNuevo(self):
    #     s = Popup(title="Mensaje", content= Label(text=str("Seleccione un "+self.str_seleccion+" de la lista e ingrese monto.")), size_hint=(None,None), size=(500, 90))
    #     popup.open()
    #     pass

class UsuarioApp(App):
    def build(self):
		  		return Usuario() 

if __name__ == "__main__":
	UsuarioApp().run()
