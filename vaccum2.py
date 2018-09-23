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
              (1, 4, matriz[0][1], matriz[0][2], matriz[0][3], 1),
              (1, matriz[1][0], matriz[1][1], matriz[1][2], matriz[1][3], 1),
              (1, matriz[2][0], matriz[2][1], matriz[2][2], matriz[2][3], 1),
              (1, matriz[3][0], matriz[3][1], matriz[3][2], matriz[3][3], 1),
              (1, 1, 1, 1, 1, 1)]            
    return matriz

class Aspirador:

    LinhaAspirador = 1
    ColunaAspirador = 1
    Pontos = 0
    Mundo = ()
    LinhaObjetivo = -1
    ColunaObjetivo = -1

    def acionar(self, mundo):
        self.Mundo = mundo
        
        while self.temSujeira():
            acao = self.perceberMundo()
            self.mover(acao)
            plt.pause(0.1)
            exibir(self.Mundo)
            self.aspirarBloco()

    def mover(self, acao):
        self.Pontos += 1
        print("Minha posicao: ", self.LinhaAspirador, self.ColunaAspirador)
        print("Pontos atuais: ", self.Pontos)
        print("Movendo-se para ", acao)
        
        linha = list(self.Mundo[self.LinhaAspirador])
        linha[self.ColunaAspirador] = Bloco.LIMPO.value
        linha = tuple(linha)
        self.Mundo[self.LinhaAspirador] = linha

        if acao == Acao.ABAIXO:
            self.LinhaAspirador = self.LinhaAspirador + 1
            linha = list(self.Mundo[self.LinhaAspirador])
            linha[self.ColunaAspirador] = Bloco.ASPIRADOR.value
            linha = tuple(linha)
            self.Mundo[self.LinhaAspirador] = linha            
        elif acao == Acao.ACIMA:
            self.LinhaAspirador = self.LinhaAspirador - 1
            linha = list(self.Mundo[self.LinhaAspirador])
            linha[self.ColunaAspirador] = Bloco.ASPIRADOR.value
            linha = tuple(linha)
            self.Mundo[self.LinhaAspirador] = linha            
        elif acao == Acao.DIREITA:
            self.ColunaAspirador = self.ColunaAspirador + 1
            linha = list(self.Mundo[self.LinhaAspirador])
            linha[self.ColunaAspirador] = Bloco.ASPIRADOR.value
            linha = tuple(linha)            
            self.Mundo[self.LinhaAspirador] = linha
        elif acao == Acao.ESQUERDA:
            self.ColunaAspirador = self.ColunaAspirador - 1
            linha = list(self.Mundo[self.LinhaAspirador])
            linha[self.ColunaAspirador] = Bloco.ASPIRADOR.value
            linha = tuple(linha)            
            self.Mundo[self.LinhaAspirador] = linha    
        else:
            print("Acao nao implementada")

    def temSujeira(self):
        for i in range (1, 6):
            linhaTuple = self.Mundo[i]
            for j in linhaTuple:
                if j == Bloco.SUJO.value:
                    print("Movendo-se para a sujeira ",i, j)
                    return True
        return False

    def perceberMundo(self): 
        for i in range (0, 5):
            linhaTuple = self.Mundo[i]
            for j in range (0, 5):
                if linhaTuple[j] == Bloco.SUJO.value and self.ehBlocoDefinidoComoObjetivo(i, j):
                    self.definirObjetivo(i, j)
                    if (self.LinhaAspirador - i) > 0:
                        return Acao.ACIMA
                    elif (self.LinhaAspirador - i) < 0:
                        return Acao.ABAIXO
                    elif (self.ColunaAspirador - j) > 0:
                        return Acao.ESQUERDA
                    elif (self.ColunaAspirador - j < 0):
                        return Acao.DIREITA
        return Acao.NOOP 

    def definirObjetivo(self, linha, coluna):
        self.LinhaObjetivo = linha
        self.ColunaObjetivo = coluna

    def ehBlocoDefinidoComoObjetivo(self, linha, coluna):
        objetivoJaDefinido = self.LinhaObjetivo > -1
        ehBlocoDefinidoComoObjetivo = self.LinhaObjetivo == linha and self.ColunaObjetivo == coluna
        return ehBlocoDefinidoComoObjetivo or (not objetivoJaDefinido)

    def aspirarBloco(self):
        print('Aspirando')
        linha = list(self.Mundo[self.LinhaAspirador])
        linha[self.ColunaAspirador] = Bloco.LIMPO.value
        linha = tuple(linha)
        self.Mundo[self.LinhaAspirador] = linha
        if (self.ColunaAspirador == self.ColunaObjetivo) and (self.LinhaAspirador == self.LinhaObjetivo):
            self.LinhaObjetivo = -1
            self.ColunaObjetivo = -1    
    
def main():
    plt.show()
    plt.pause(0.001)
    mundo = gerarMundo()
    exibir(mundo)
    aspirador = Aspirador()
    aspirador.acionar(mundo)
    exit()

main()