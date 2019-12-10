#
# ------------------------------------------------ #
# Autor: Vinicius Alves de Araujo - Mat.: 0011941
# ------------------------------------------------ #
#

class Bloco:

    # Construtor
    def __init__(self, nome):
        self.nome           = nome
        self.inicial        = None
        self.estadoAtual    = []
        self.fitaAntiga     = []
        self.noAlfabeto     = ['*', '_']    # Pode ler da fita
        self.outAlfabeto    = []            # Pode escrever na fita
        self.estados        = []
        self.finais         = []
        self.transicoes     = []
        self.blocoTransicao = []
    
    # Adiciona um novo estado para o bloco
    def addEstado(self, estado):
        if(not(estado in self.estados)):
            self.estados.append(estado)
    
    # Adiciona simbolo no alfabeto pode ler da fita
    def addAlfabetoLeitura(self, simbolo):
        if(not(simbolo in self.noAlfabeto)):
            self.noAlfabeto.append(simbolo)

    # Adiciona simbolo no alfabeto que pode escrever na fita
    def addAlfabetoEscrita(self, simbolo):
        if(not(simbolo in self.outAlfabeto)):
            self.outAlfabeto.append(simbolo)

    # Adiciona transicao 
    def addTransicao(self, transicao):
        igual = False

        for t in self.transicoes:
            if(t.equals(transicao)):
                igual = True

        if(not igual):
            self.transicoes.append(transicao)
    
    # Adiciona bloco de transicao
    def addBlocoTransicao(self, transicao):
        igual = False

        for t in self.blocoTransicao:
            if(t.equals(transicao)):
                igual = True

        if(not igual):
            self.blocoTransicao.append(transicao)

    def passosBloco(self, fita, pilha):
        # Pega o simbolo atual na fita
        simb = fita.simboloNoCabecote()
        # Uma lista para salvar todas as transicoes validas com estado atual e com o simbolo na fita atual.
        # Cria uma fila de execucao, ordem de leitura, das primeiras transicoes encontradas para as ultimas
        filaExecucao = []
        
        # Apenas para saber se a fila de execucao e os estados atuais contem a mesma quantidades de elementos
        tamListAtuais = 0

        # Para salvar os estados atuais
        listAtuais = []
        k = -1

        # Para cada estado atual
        for i in range(0, len(self.estadoAtual), 1):
            # Para salvar os estados atuais
            listAuxAtuais = []

            for j in range(0, len(self.estadoAtual[i]), 1):
                # Pula quando nao ha um estado None, nao ha mais transicoes para esse ramo
                if(self.estadoAtual[i][j] == 'None'):
                    break

                # Verifica se o bloco eh para parar a execucao
                if(self.estadoAtual[i][j] == 'pare'):
                    filaExecucao.append('pare')
                    listAuxAtuais.append(self.inicial)
            
                # Verifica se eh para retornar a execucao ao bloco anterior
                if(self.estadoAtual[i][j] == 'retorne'):
                    filaExecucao.append(None)
                    listAuxAtuais.append(self.inicial)

                auxAntiga = self.fitaAntiga
                # Procura todas as transicoes possiveis no estado atual e com o simbolo na fita atual - Transicoes
                for transicao in self.transicoes:
                    if((transicao.estado_partida == self.estadoAtual[i][j]) and ((transicao.simbolo_atual == simb) or (transicao.simbolo_atual == '*'))):
                        # Se tiver exclamacao
                        if(transicao.pause):
                            filaExecucao.append('pause')
                        else:
                            filaExecucao.append(self)
                        
                        # Fork
                        if(listAuxAtuais != []):
                            print('\n\t» Forking «')

                            if(auxAntiga != []):
                                #print(auxAntiga)
                                #print(k)
                                (fitaAnterior, posicao) = self.fitaAntiga[k]
                                fita.cabecote = posicao
                                print('FA: ',fitaAnterior)
                                #print(fitaAnterior)
                                auxAntiga[k] = (fitaAnterior, posicao)
                            else:
                                print(fita.estadoFita(self.nome, self.estadoAtual[i][j]))
                                auxAntiga.append((fita.estadoFita(self.nome, self.estadoAtual[i][j]), fita.cabecote))
                            
                        proximoEstado = transicao.estado_destino

                        if(proximoEstado != '*'):
                            # * significa que não muda de estado
                            listAuxAtuais.append(transicao.estado_destino)

                        # Salva como nova fita antiga
                        if(auxAntiga == []):
                            auxAntiga.append((fita.estadoFita(self.nome, self.estadoAtual[i][j]), fita.cabecote))
                        else:
                            auxAntiga[k] = (fita.estadoFita(self.nome, self.estadoAtual[i][j]), fita.cabecote)
                            k += 1
                        
                        # Escreve o caractere na fita
                        fita.cabecoteDaFita(transicao.simbolo_novo)
                        # Move cabecote
                        fita.moverFita(transicao.movimento)

                        # Apenas para mostrar as transicoes encontradas para o estado atual
                        print('>> ',transicao.estado_partida,' ',transicao.simbolo_atual,' ',proximoEstado,' ',transicao.movimento)
                        print(fita.estadoFita(self.nome, self.estadoAtual[i][j]))
                
                self.fitaAntiga = auxAntiga

                # Procura todas as transicoes possiveis no estado atual e com o simbolo na fita atual - Transicoes de Blocos
                for trBloco in self.blocoTransicao:
                    if(trBloco.estadoInicial == self.estadoAtual[i][j]):
                        # Empilha o bloco chamador e o estado de retorno
                        pilha.append((self, trBloco.retorno))
                        filaExecucao.append(trBloco.destino)

                        # Apenas para mostrar as transicoes de bloco encontradas para o estado atual
                        print('>> ',trBloco.estadoInicial,' ',trBloco.destino.nome,' ',trBloco.retorno)
                
                listAuxAtuais.append('None')

            listAtuais.append(listAuxAtuais)
        
        self.estadoAtual = listAtuais
        return filaExecucao
