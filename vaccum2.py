import numpy as np
from matplotlib import pyplot as plt
from enum import Enum

class Acao(Enum):
    ACIMA = 1
    ABAIXO = 2
    ESQUERDA = 3
    DIREITA = 4 
    ASPIRAR = 5
    NOOP = 6

class Bloco(Enum):
    PAREDE = 1
    SUJO = 2
    LIMPO = 3
    ASPIRADOR = 4

def agenteReativoSimples(percepcao):
    return Acao.ACIMA

def exibir(I):
    plt.imshow(I, 'gray')
    plt.show(block=False)
    plt.pause(0.5) 
    plt.clf()    

def gerarMundo():
    rows  = 4
    cols = 4
    low = 2
    high = 4
    step = 1

    matriz = np.random.choice([x for x in range(low, high, step)], rows*cols)
    matriz.resize(rows, cols)
    
    matriz = [(1, 1, 1, 1, 1, 1),
              (1, matriz[0][0], matriz[0][1], matriz[0][2], matriz[0][3], 1),
              (1, matriz[1][0], matriz[1][1], matriz[1][2], matriz[1][3], 1),
              (1, matriz[2][0], matriz[2][1], matriz[2][2], matriz[2][3], 1),
              (1, matriz[3][0], matriz[3][1], matriz[3][2], matriz[3][3], 1),
              (1, 1, 1, 1, 1, 1)]            
    return matriz

class Aspirador:

    LinhaAspirador = 0
    ColunaInicialAspirador = 0
    Pontos = 0
    Mundo = ()

    def acionar(self, mundo):
        self.Mundo = mundo
        
        while self.temSujeira():
            plt.pause(0.001)
            acao = self.perceberMundo()
            self.mover(acao)
            self.aspirarBloco()

    def mover(self, acao):
        self.Pontos += 1
        print("Pontos atuais: %", self.Pontos)
        if acao == Acao.ABAIXO:
            print(acao)
            if (self.LinhaAspirador+1 == 5):
                self.VoltaCompleta = True
                return
            linha = list(self.Mundo[self.LinhaAspirador+1])
            linha[1] = Bloco.ASPIRADOR.value
            linha = tuple(linha)
            self.Mundo[self.LinhaAspirador+1] = linha
            self.LinhaAspirador = self.LinhaAspirador+1
            self.ColunaAspirador = 1
            
        elif acao == Acao.ACIMA:
            print(acao)
            linha = list(self.Mundo[self.LinhaAspirador+1])
            linha[1] = Bloco.ASPIRADOR.value
            linha = tuple(linha)
            self.Mundo[self.LinhaAspirador-1] = linha
            self.LinhaAspirador = self.LinhaAspirador+1
            self.ColunaAspirador = 1
        elif acao == Acao.DIREITA:
            print(acao)
            linha = list(self.Mundo[self.LinhaAspirador])
            linha[self.ColunaAspirador-1] = Bloco.ASPIRADOR.value
            linha = tuple(linha)
            self.LinhaAspirador = self.LinhaAspirador
            self.ColunaAspirador = self.ColunaAspirador+1
            self.Mundo[self.LinhaAspirador] = linha
        elif acao == Acao.ESQUERDA:
            print(acao)
            if (self.Mundo[self.LinhaAspirador][self.ColunaAspirador+1] == Bloco.PAREDE.value):
                self.VoltaCompleta = True
                return
            linha = list(self.Mundo[self.LinhaAspirador])
            linha[self.ColunaAspirador+1] = Bloco.ASPIRADOR.value
            linha = tuple(linha)
            self.LinhaAspirador = self.LinhaAspirador
            self.ColunaAspirador = self.ColunaAspirador+1
            self.Mundo[self.LinhaAspirador] = linha
        elif acao == Acao.ASPIRAR:
            print(acao)
        else:
            print("Acao nao implementada")

    def temSujeira(self):
        #if Bloco.SUJO.value in self.Mundo
        for i in range (1, 6):
            linhaTuple = self.Mundo[i]
            for j in linhaTuple:
                if j == Bloco.SUJO.value:
                    print("Movendo-se para a sujeira ",i, j)
                    return True
        return False

    def perceberMundo(self): 
        for i in range (1, 6):
            linhaTuple = self.Mundo[i]
            for j in linhaTuple:
                if j == Bloco.SUJO.value:
                    if (self.LinhaAspirador - i) > 0:
                        return Acao.ACIMA
                    elif (self.LinhaAspirador - i) < 0:
                        return Acao.ABAIXO
                    elif (self.ColunaAspirador - j) > 0:
                        return Acao.ESQUERDA
                    elif (self.ColunaAspirador - j < 0):
                        return Acao.DIREITA
        return Acao.NOOP 


    def aspirarBloco(self):
        print('Aspirando')
        if (self.Mundo[self.LinhaAspirador][self.ColunaAspirador] == Bloco.PAREDE.value):
            return
        linha = list(self.Mundo[self.LinhaAspirador])
        linha[self.ColunaAspirador] = Bloco.LIMPO.value
        linha = tuple(linha)
        self.Mundo[self.LinhaAspirador] = linha        
    
def main():    

    plt.show()
    plt.pause(0.001)
    mundo = gerarMundo()
    exibir(mundo)
    aspirador = Aspirador()
    aspirador.acionar(mundo)
    exit()

main()