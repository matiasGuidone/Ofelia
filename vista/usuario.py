from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button 
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
import sys, os
sys.path.append(os.getcwd())
from modelo.conexion import conexion 
# configuration
from kivy.config import Config
Config.set("graphics", "width",  540)
Config.set("graphics", "height", 300)

class Box(BoxLayout):
    pass
    id = 0
    tipo = ''
    user = []
   
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        datos = conexion().selectAll("Usuarios")
        dropdown = self.ids.drpUsuarios  
        dropdown.clear_widgets()   
        for index in range(len(datos)): 
            btn = Button(text = '% d - ' % index + str(datos[index][1]), size_hint_y = None, id = str(datos[index][0]), height = 40) 
            
            btn.bind(on_press = lambda btn: self.selectUsuario(btn.id))
            btn.bind(on_release = lambda btn: dropdown.select(btn.text)) 
            dropdown.add_widget(btn) 

        mainbutton = self.ids.btnMain
        mainbutton.bind(on_release = dropdown.open) 
        dropdown.bind(on_select = lambda instance, x: setattr(mainbutton, 'text', x))
        pass

    def selectUsuario(self,id):
        self.id = int(id)
        self.user = conexion().selectId(self.id, 'Usuarios') 
        pass

    def openPopup(self, titulo):
        #armado de popup 
        contenido = BoxLayout(orientation='vertical')
        #campos de llenado
        if self.id != 0:
            user = TextInput(hint_text="Nombre de usuario",text=self.user[0][1])
        else:
            user = TextInput(hint_text="Nombre de usuario")

        contr = TextInput(hint_text="Contraseña", password = True)
        contr2 = TextInput(hint_text="Repetir contraseña", password = True)
        but = BoxLayout(orientation='horizontal')
        but.add_widget(Button(text="Cancelar",on_press = lambda *args: popup.dismiss()))
        but.add_widget(Button(text="Guardar" ,on_press = lambda *args: self.guardarUser(user.text, contr.text, contr2.text)))
        tipos = BoxLayout() 
        tipos.add_widget(ToggleButton(text="Administrador",group = 'tipo', on_press = lambda btn: self.selectTipo("admin"))) 
        tipos.add_widget(ToggleButton(text="Caja", group = 'tipo', on_press = lambda btn: self.selectTipo("caja")))
        tipos.add_widget(ToggleButton(text="Caja-pagos", group = 'tipo', on_press = lambda btn: self.selectTipo("caja-pagos")))
        contenido.add_widget(user)
        contenido.add_widget(contr)
        contenido.add_widget(contr2)
        contenido.add_widget(tipos)
        contenido.add_widget(but)
        popup = Popup(title= titulo, content= contenido, size_hint=(None,None), size=(450, 300))
        popup.open()
        pass

    def btnEditar(self):
        self.openPopup("Editar el usuario")
        
        # param = [usuario_text, "admin", pass_text]
        # cone.insert(param,"Usuarios")
        pass

    def btnEliminar(self):
        cont = BoxLayout()
        cont.add_widget(Label(text='¿ Desea eliminar el usuario "'+self.user[0][1]+'" ?'))
        cont.add_widget(Button(text='si', on_press = lambda btn: self.elimina() ))
        cont.add_widget(Button(text='no',on_press = lambda *args: mensj.dismiss() ))
        
        mensj = Popup(title="Confirmar", content= cont, size_hint=(None,None), size=(330, 150))
        mensj.open()
        
        # param = [usuario_text, "admin", pass_text]
        # cone.insert(param,"Usuarios")
        pass
    
    def elimina(self):
        conexion().delete(self.id, 'Usuarios')
        pass

    def btnNuevo(self):
        self.id = 0
        self.openPopup("Nuevo usuario")
        pass

    def selectTipo(self,tipo) :
        self.tipo = tipo
        pass

    def guardarUser(self, user, contr, contr2):
        if contr == contr2 and self.id == 0:
            conexion().insert([user, self.tipo , contr], 'Usuarios')
        elif contr == contr2 :
            conexion().update([user, self.tipo , contr, self.id], 'Usuarios')
        else:
            mensj = Popup(title="Error", content= Label(text='Asegurese de que las contraseñas ingresadas sean idénticas'), size_hint=(None,None), size=(330, 150))
            mensj.open()
        pass

	# def btnNuevo(self):
    #     s = Popup(title="Mensaje", content= Label(text=str("Seleccione un "+self.str_seleccion+" de la lista e ingrese monto.")), size_hint=(None,None), size=(500, 90))
    #     popup.open()
    #     pass

class UsuarioApp(App):
    def build(self):
		  		return Box() 

if __name__ == "__main__":
	UsuarioApp().run()