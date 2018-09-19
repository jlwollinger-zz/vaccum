import numpy as np
from matplotlib import pyplot as plt
from enum import Enum


class Acao(Enum):
    ACIMA = 1
    ABAIXO = 2
    ESQUERDA = 3
    DIREITA = 4 
    ASPIRAR = 5

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

def gerarMundo(linhaInicialAspirador, colunaInicialAspirador):
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

    linhaAspirador = 0
    colunaInicialAspirador = 0
    voltaCompleta = False

    def aspirar(self, mundo, linhaInicialAspirador, colunaInicialAspirador):
        self.linhaAspirador = linhaInicialAspirador
        self.colunaAspirador = colunaInicialAspirador
        
        while not self.voltaCompleta:
            plt.pause(0.001)
            self.limparBloco(mundo)
            self.moverParaProximoBloco(mundo)                                    
            exibir(mundo)
                
    def moverParaProximoBloco(self, mundo):        
        if (mundo[self.linhaAspirador][self.colunaAspirador+1] == Bloco.PAREDE.value):
            if (self.linhaAspirador + 1 == 5):
                self.voltaCompleta = True
                return

            linha = list(mundo[self.linhaAspirador+1])
            linha[1] = Bloco.ASPIRADOR.value
            linha = tuple(linha)
            mundo[self.linhaAspirador+1] = linha
            self.linhaAspirador = self.linhaAspirador + 1
            self.colunaAspirador = 1
        else:
            linha = list(mundo[self.linhaAspirador])
            linha[self.colunaAspirador+1] = Bloco.ASPIRADOR.value
            linha = tuple(linha)
            self.linhaAspirador = self.linhaAspirador
            self.colunaAspirador = self.colunaAspirador+1
            mundo[self.linhaAspirador] = linha
        
    def limparBloco(self, mundo):    
        if (mundo[self.linhaAspirador][self.colunaAspirador] == Bloco.PAREDE.value):
            return
        linha = list(mundo[self.linhaAspirador])
        linha[self.colunaAspirador] = Bloco.LIMPO.value
        linha = tuple(linha)
        mundo[self.linhaAspirador] = linha

def main():    

    linhaInicialAspirador = 0
    colunaInicialAspirador = 2

    plt.show()
    mundo = gerarMundo(linhaInicialAspirador, colunaInicialAspirador)
    
    mundo = gerarMundo(linhaInicialAspirador, colunaInicialAspirador)
    exibir(mundo)
    aspirador = Aspirador()
    aspirador.aspirar(mundo, linhaInicialAspirador, colunaInicialAspirador)
    

if __name__ == "__main__":
    main()
