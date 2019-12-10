#
# ------------------------------------------------ #
# Autor: Vinicius Alves de Araujo - Mat.: 0011941
# ------------------------------------------------ #
#

class Fita:
    MOV_ESQUERDA = 'e'
    MOV_DIREITA  = 'd'
    MOV_IMOVEL   = 'i'

    # Construtor
    def __init__(self, delimitador):
        self.palavra     = ''
        self.cabecote    = -1          # Posicao do cabecote da fita
        self.delimitador = delimitador # Delimitador de inicio de fita

    # Retorna o simbolo atual no cabecote da fita
    def simboloNoCabecote(self):
        if((self.cabecote < 0) or (self.cabecote >= len(self.palavra))):
            return '_'
        else:
            return self.palavra[self.cabecote]

    # Escreve o caracter no cabecote da fita / Move o cabecote ate o caracter
    def cabecoteDaFita(self, caracter):
        if(caracter == '*'):
            return
        
        result = self.palavra[:self.cabecote] + caracter + self.palavra[(self.cabecote + 1):]
        self.palavra = result
        return

        '''if(self.cabecote >= 0):
            result = self.palavra[:self.cabecote] + caracter + self.palavra[(self.cabecote+1):]
        else:
            result = caracter + self.palavra[0:]
            self.cabecote += 1'''
        
        return result

    # Atualiza a posicao do cabecote da fita conforme for o movimento realizado
    def moverFita(self, movimento):
        if(movimento == self.MOV_DIREITA):
            self.cabecote += 1
        elif(movimento == self.MOV_ESQUERDA):
            self.cabecote -= 1
    
    # Procedimento para retornar o que imprimir da fita
    def estadoFita(self, bloco, estado):
        if(estado == 'retorne'):
            estado = 'rtrn'
        
        result = bloco + '.' + estado + ': '
        resultadoFita = ''
        tamPalavra = len(self.palavra)

        if(self.cabecote >= 0):
            caracteSelec = self.palavra[self.cabecote:(self.cabecote+1)]
            
            if(caracteSelec == ''):
                caracteSelec = '_'

            resultadoFita = self.palavra[:self.cabecote] + self.delimitador[0] + caracteSelec
            resultadoFita += self.delimitador[1] + self.palavra[(self.cabecote+1):]

            if(caracteSelec == '_'):
                tamPalavra += 1

            qtd = (20 - self.cabecote)

            # Ajustando para imprimir a fita
            if(qtd < 0):
                resultadoFita = resultadoFita[(self.cabecote-20):]
            else:
                for i in range(0, qtd):
                    resultadoFita = '_' + resultadoFita

            qtd = 20 - tamPalavra + self.cabecote

            if(qtd < 0):
                resultadoFita = resultadoFita[:(-(tamPalavra - 20 - self.cabecote))]
            else:
                # Adicionar '_'
                for i in range(0, qtd):
                    resultadoFita = resultadoFita + '_'
        else:
            # Indice do cabecote menor que zero
            resultadoFita = self.palavra
            qtd = 20 + self.cabecote + 1

            for i in range(0, qtd):
                resultadoFita = '_' + resultadoFita

            indice = 0
            resultadoFita = resultadoFita[:qtd] + self.delimitador[0] + '_'
            resultadoFita += self.delimitador[1] + self.palavra
            qtd = 20 - tamPalavra + self.cabecote

            # Ajustando para imprimir a fita
            if(qtd < 0):
                resultadoFita = resultadoFita[:(-(tamPalavra - 20 - self.cabecote))]
            else:
                # Adicionar '_'
                for i in range(0, qtd):
                    resultadoFita = resultadoFita + '_'

        result += resultadoFita
        return result