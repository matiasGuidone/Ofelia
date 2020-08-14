from datetime import datetime

class FechaYHora:
    ahora=[ 0, 0, 0, 0, 0, 0 ]
    ahoraString=""

    def _init_(self):
        self.ahora[0]=2020
        self.ahora[1]=8
        self.ahora[2]=13
        self.ahora[3]=23
        self.ahora[4]=25
        self.ahora[5]=42

    def resetear(self):
        now=datetime.now()
        self.ahora[0]=now.year
        self.ahora[1]=now.month
        self.ahora[2]=now.day
        self.ahora[3]=now.hour
        self.ahora[4]=now.minute
        self.ahora[5]=now.second

    def getAhoraGuardo(self):   
        self.ahoraString=""     
        i=0
        for i in range(len(self.ahora)):
            self.ahoraString=self.ahoraString + str(self.ahora[i]) + "/" 
            i+=1
        self.ahoraString=self.ahoraString[len(self.ahoraString)-1,len(self.ahoraString)]
        return self.ahoraString
    
    #toma una fecha en string y devuelve dato según parámetro
    def dameDato(self, stringFecha, enteroDato):
        #Los Parámetros son:
        # 0=Año , 1=mes, 2=día, 3=hora, 4=minuto, 5=segundo
        # 6=mes/año, 7=dia/mes, 8=día-hora, 9=hora:minuto
        # 10=dia/mes/año, 11=hora:minuto:segundo     
        # 12=dia/mes/año - hora:minuto:segundo             
        i=0      
        cont=0
        aux=""  
        aux2=""
        self.ahora[0]=int(stringFecha[0,4])
        aux=stringFecha[0,5]     
        cont+=1
        for i in range(len(aux)):            
            if aux[i]=="/":
                aux=aux[0,1] 
                self.ahora[cont]=int(aux2)
                cont+=1
                aux2=""
            else:
                aux2+=aux[i]
            i+=1
        cont=enteroDato
        if cont in range(6):
            return self.ahora[cont]
        elif cont in range(6,8):
            return self.ahora[cont-5] + "/" + self.ahora[cont-6]
        elif cont==8:
            return self.ahora[2] + "-" + self.ahora[3]
        elif cont==9:
            return self.ahora[3] + ":" + self.ahora[4]
        elif cont==10:
            return self.ahora[2] + "/" + self.ahora[1] + "/" + self.ahora[0]
        elif cont==11:
            return self.ahora[3] + ":" + self.ahora[4] + ":" + self.ahora[5]
        elif cont==12:
            return self.ahora[2] + "/" + self.ahora[1] + "/" + self.ahora[0] + " - " +self.ahora[3] + ":" + self.ahora[4] + ":" + self.ahora[5]
            