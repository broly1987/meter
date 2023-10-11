import random


class Maquina():


    lockname=[]
    rtp={}
    juego={}

    def __init__(self,maquinas):
        self.maquinas=maquinas

    def __str__(self):
        return 'Iniciando programa'


    def agrega_maquina(self):



        return self.maquinas


result =[]
nuevas_maquinas = int(input('ingresa las nuevas maquinas'))
toda = Maquina(nuevas_maquinas)
resultado =toda.agrega_maquina()
result.append(resultado)

print(result)


