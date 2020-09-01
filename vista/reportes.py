from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button 
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.config import Config
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton 
from kivy.properties import ObjectProperty
import xlwt
import platform

import sys, os
sys.path.append(os.getcwd())
from modelo.conexion import conexion 
from modelo.FechayHora import FechayHora 
Config.set("graphics", "window_state",  'maximized')
 
class SaveDialog(FloatLayout):
    archivo = FechayHora().formatos(10)+'.xls'
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)

class Reportes(BoxLayout):
    fecha = FechayHora().formatos(10)
    popup = Popup()
    tipo = ''
#eventos de los botones toggle de arriba cada uno busca en la base los resultados correspondientes con cada tipo de gasto
    def btnDiario(self):
        self.openPopup('diario')
        pass

    def btnMensual(self):
        self.openPopup('mensual')
        pass

    def btnCancelado(self):
        self.openPopup('cancelado')
        pass
    
    def openPopup(self, tipo):
        # #armado de popup 
        contenido = BoxLayout(orientation='vertical')
        but = BoxLayout(orientation='horizontal')
        if tipo == 'diario':
            titulo = 'Reporte diario de movimientos'
            controles = BoxLayout(orientation='horizontal')
            txtfecha = TextInput( hint_text="dd-mm-yy", text=FechayHora().formatos(10) ,multiline=False, font_size=25.0 )
            controles.add_widget(txtfecha)
            but.add_widget(Button(text="Generar" ,on_press = lambda *args: self.ventanaGuardar(txtfecha.text, self.popup,'diario'), background_normal= 'normal.png', background_color= (1, .745, .039, 1), font_size =25.0))
        elif tipo == 'mensual':
            titulo = 'Reporte mensual de movimientos'
            controles = BoxLayout(orientation='horizontal')
            txtfecha = TextInput( hint_text="mm-yy", text=FechayHora().formatos(6) ,multiline=False, font_size=25.0 )
            controles.add_widget(txtfecha)
            but.add_widget(Button(text="Generar" ,on_press = lambda *args: self.ventanaGuardar(txtfecha.text, self.popup,'mensual'), background_normal= 'normal.png', background_color= (1, .745, .039, 1), font_size =25.0))
        elif tipo == 'cancelado':
            titulo = 'Reporte cancelados'
            controles = BoxLayout(orientation='horizontal')
            txtfecha = TextInput( hint_text="dd-mm-yy", text=FechayHora().formatos(10) ,multiline=False, font_size=25.0 )
            controles.add_widget(txtfecha)
            but.add_widget(Button(text="Generar" ,on_press = lambda *args: self.ventanaGuardar(txtfecha.text, self.popup,'cancelado'), background_normal= 'normal.png', background_color= (1, .745, .039, 1), font_size =25.0))
                   
        but.add_widget(Button(text="Cancelar",on_press = lambda *args: popup.dismiss(),  height = 40, background_normal= 'normal.png', background_color= (1, .745, .039, 1), font_size =25.0))
        
        contenido.add_widget(controles)
        contenido.add_widget(but)
        self.popup = Popup(title = titulo, content= contenido, size_hint=(None,None),auto_dismiss=False, size=(460, 150), background='Fondop.png', separator_color=(1, .745, .039, 1), title_size=25.0, separator_height=5.0)
        self.popup.open()
        pass
    
    def cerrar_popup(self):
        self.popup.dismiss()

    def ventanaGuardar(self, fecha, popup, tipo):
        self.fecha = fecha
        self.popup.dismiss()
        self.tipo = tipo
        content = SaveDialog(save = self.save, cancel=self.cerrar_popup)
        
        self.popup = Popup(title="Guardar archivo", content=content,
                            size_hint=(0.9, 0.9))
        self.popup.open()

    def save(self, url, text):
        if self.tipo == 'diario':
            datos = conexion().getReporteDiario(self.fecha)
            # print(datos)
            style_cabecera = xlwt.easyxf('font: colour black, bold on')
            wb = xlwt.Workbook()
            ws = wb.add_sheet('Reporte diario',cell_overwrite_ok=True)
            ws.write(0, 0, 'Reporte diario', style_cabecera)
            ws.write(1, 0, 'Fecha', style_cabecera)
            ws.write(1, 1, 'Hora', style_cabecera)
            ws.write(1, 2, 'Turno', style_cabecera)
            ws.write(1, 3, 'Monto de ingreso', style_cabecera)
            ws.write(1, 4, 'Monto de egreso', style_cabecera)
            ws.write(1, 5, 'Detalle', style_cabecera)
            total_ingreso = 0
            total_egreso = 0
            for i in range(len(datos)):  
                for n in range(len(datos[i])):
                    ws.write(i+2, n, datos[i][n])
                    if n == 3 and datos[i][n] != '':
                        total_ingreso += float(datos[i][n])
                    elif n == 4 and datos[i][n] != '':
                        total_egreso += float(datos[i][n])
            ws.write(len(datos)+3, 0, 'Total ingresos', style_cabecera)
            ws.write(len(datos)+3, 1, total_ingreso, style_cabecera)
            ws.write(len(datos)+4, 0, 'Total egresos', style_cabecera)
            ws.write(len(datos)+4, 1, total_egreso, style_cabecera)
            
            # file_nombre = 'repo_diario'+FechayHora().formatos(12)+'.xls'

            wb.save(url+'/'+text) 
            self.cerrar_popup()

        elif self.tipo == 'mensual':
            datos = conexion().getReporteMensual(self.fecha)
            # print(datos)
            style_cabecera = xlwt.easyxf('font: colour black, bold on')
            wb = xlwt.Workbook()
            ws = wb.add_sheet('Reporte mensual',cell_overwrite_ok=True)
            ws.write(0, 0, 'Reporte mensual', style_cabecera)
            ws.write(1, 0, 'Dia', style_cabecera)
            ws.write(1, 1, 'Turno mañana', style_cabecera)
            ws.write(1, 2, 'Turno tarde', style_cabecera)
            ws.write(1, 3, 'Total diario', style_cabecera)
            ws.write(1, 4, 'Porcentaje 3%', style_cabecera)
            ws.write(1, 5, 'Gastos', style_cabecera)
            total_mensual = 0
            porcentaje = 0
            for i in range(len(datos)):  
                for n in range(len(datos[i])):
                    if n == 0:
                        ws.write(i+2, n, FechayHora().getFechaFormateada(datos[i][n]))
                    else:    
                        ws.write(i+2, n, datos[i][n])

                    if n == 3 and datos[i][n] != '':
                        total_mensual += float(datos[i][n])
                    elif n == 4 and datos[i][n] != '':
                        porcentaje += float(datos[i][n])

            ws.write(len(datos)+3, 0, 'Total mensual', style_cabecera)
            ws.write(len(datos)+3, 1, total_mensual, style_cabecera)
            ws.write(len(datos)+4, 0, 'Total porc. 3%', style_cabecera)
            ws.write(len(datos)+4, 1, porcentaje, style_cabecera)
            
            # file_nombre = 'repo_diario'+FechayHora().formatos(12)+'.xls'

            wb.save(url+'/'+text) 
            self.cerrar_popup()

        elif self.tipo == 'cancelado':
            datos = conexion().getReporteCancelados(self.fecha)
            # print(datos)
            style_cabecera = xlwt.easyxf('font: colour black, bold on')
            wb = xlwt.Workbook()
            ws = wb.add_sheet('Reporte de cancelados',cell_overwrite_ok=True)
            ws.write(0, 0, 'Reporte de cancelados', style_cabecera)
            ws.write(1, 0, 'Descripción', style_cabecera)
            ws.write(1, 1, 'Hora de borrado', style_cabecera)
            ws.write(1, 2, 'Hora de venta', style_cabecera)
            ws.write(1, 3, 'Monto', style_cabecera)
            ws.write(1, 4, 'Usuario en caja', style_cabecera)
             
            for i in range(len(datos)):  
                for n in range(len(datos[i])):
                    ws.write(i+2, n, datos[i][n])
                     
            
            # file_nombre = 'repo_diario'+FechayHora().formatos(12)+'.xls'

            wb.save(url+'/'+text) 
            self.cerrar_popup()

        pass
 


   


class ReportesApp(App):
    def build(self):
		  		return Reportes() 

if __name__ == "__main__":
	ReportesApp().run()

