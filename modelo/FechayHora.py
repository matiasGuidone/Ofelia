from datetime import datetime

class FechayHora:
    formato = "%d-%m-%y  %H:%M:%S"
    now=datetime.now()
    ahoraString =" "
    
    def _init_(self):
        self.now=datetime.now()

    def formatos(self, nF):      
        #Los Parámetros son:
        # 0=Año , 1=mes, 2=día, 3=hora, 4=minuto, 5=segundo
        # 6=mes/año, 7=dia/mes, 8=día-hora, 9=hora:minuto
        # 10=dia/mes/año, 11=hora:minuto:segundo     
        # 12=dia/mes/año - hora:minuto:segundo     
        if nF==0:
            self.formato = "%y"
        elif nF==1:            
            self.formato = "%m"
        elif nF==2:            
            self.formato = "%d"
        elif nF==3:            
            self.formato = "%H"
        elif nF==4:            
            self.formato = "%M"
        elif nF==5:            
            self.formato = "%S"
        elif nF==6:            
            self.formato = "%m-%y"
        elif nF==7:            
            self.formato = "%d-%m"
        elif nF==8:            
            self.formato = "%d - %H"
        elif nF==9:            
            self.formato = "%H:%M"
        elif nF==10:            
            self.formato = "%d-%m-%y"
        elif nF==11:            
            self.formato = "%H:%M:%S"
        elif nF==12:            
            self.formato = "%d-%m-%y  %H:%M:%S"
        cadena1 = self.now.strftime(self.formato)  
        return cadena1

    def resetear(self):
        self.now=datetime.now()

    def getAhoraGuardo(self):   
    # Prepara la cadena para guardar
        self.now=datetime.now()
        return self.now.strftime(self.formatos(12))

    def getFechaFormateada(self, fecha):
        ano='20'+fecha[6:8]
        mes=fecha[3:5]
        dia=fecha[0:2]
        fec = datetime(int(ano), int(mes), int(dia), 0, 0, 0)
        dia_sem = fec.weekday()
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        semana=['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo']
        return semana[dia_sem]+" "+dia+" de "+meses[int(mes)]+" del "+ano
        pass
