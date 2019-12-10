#
# ------------------------------------------------ #
# Autor: Vinicius Alves de Araujo - Mat.: 0011941
# ------------------------------------------------ #
#

import Fita
import Bloco
import Transicao
import BlocoTransicao
from time import sleep

class MaqTuring:
    MODO_RESUME     = 0
    MODO_VERBOSE    = 1
    MAX_STEPS       = 500
    DELIMITADOR     = ['(', ')']

    # Construtor
    def __init__(self, config):
        self.pilha          = []          # Para salvar uma pilha de execucao de blocos
        self.blocos         = []
        self.alfabeto       = ['*', '_']
        self.modo           = config[0]   # Modo de funcionamento da maquina
        self.passos         = config[1]   # Limita a quantidade de passos maximos que a maquina pode executar
        self.delimitador    = config[2]   # Demilimitadores da fita da maquina
        self.blocoAtual     = None        # Bloco que esta para ser processado
        self.ultimosEstados = []          # Salva o ultimo estado em que a maquina passou
        self.listBlocos     = []
        self.inicio         = False
        self.fita = Fita.Fita(self.delimitador)
    
    # Verifica se a entrada eh valida e carrega para o cabecote
    def entradaValida(self, entrada):
        for c in entrada:
            if(c in self.alfabeto):
                continue
            else:
                print("> A entrada possui simbolos invalidos.")
                return False
        self.fita.palavra = entrada
        return True
    
    # Seta as novas configuracoes da maquina apos a ocorrencia de parada
    def resetarConfiguracoes(self, config):
        self.modo             = config[0]
        self.passos           = config[1]
        self.fita.delimitador = config[2]

    # Verifica a existencia de um bloco com o nome passado e o retorna
    def retornaBloco(self, nome):
        for b in self.blocos:
            if(b.nome == nome):
                return b
        
        return None

    # Adiciona um novo bloco para a maquina
    def addBloco(self, nomeBloco, estInicial):
        bloco = self.retornaBloco(nomeBloco)

        if(bloco != None):
            bloco.inicial     = estInicial
            bloco.estadoAtual = [[estInicial]]
        else:
            # Cria um bloco novo
            bloco = Bloco.Bloco(nomeBloco)
            bloco.inicial     = estInicial
            bloco.estadoAtual = [[estInicial]]

            self.blocos.append(bloco)
            return bloco

    # Adiciona uma nova transicao para a maquina
    def addTransicao(self, idTransicao, partida, simboloAtual, destino, simboloNovo, movimento, nome, pause):
        blocoLocal = self.retornaBloco(nome)

        # Adiciona o simbolo no alfabeto da maquina
        if(not(simboloAtual in self.alfabeto)):
            self.alfabeto.append(simboloAtual)
        
        blocoLocal.addEstado(partida)
        blocoLocal.addEstado(destino)
        blocoLocal.addAlfabetoLeitura(simboloAtual)
        blocoLocal.addAlfabetoEscrita(simboloNovo)

        if(movimento == 'e'):
            nvTransicao = Transicao.Transicao(idTransicao, partida, simboloAtual, destino, simboloNovo, self.fita.MOV_ESQUERDA, pause)
        elif(movimento == 'd'):
            nvTransicao = Transicao.Transicao(idTransicao, partida, simboloAtual, destino, simboloNovo, self.fita.MOV_DIREITA, pause)
        else:
            nvTransicao = Transicao.Transicao(idTransicao, partida, simboloAtual, destino, simboloNovo, self.fita.MOV_IMOVEL, pause)
        
        blocoLocal.addTransicao(nvTransicao)

    # Adicona um novo bloco de transicao
    def addBlocoTransicao(self, inicial, retornoBloco, nomeBloco, destino):
        blocoLocal = self.retornaBloco(nomeBloco)
        destBloco =  self.retornaBloco(destino)

        # Se o bloco destino nao foi criado, cria o bloco
        if(destBloco == None):
            destBloco = self.addBloco(destino, '###')
        
        nvTransicao = BlocoTransicao.BlocoTransicao(inicial, retornoBloco, blocoLocal, destBloco)
        blocoLocal.addBlocoTransicao(nvTransicao)
    
    # Executa apenas um passo do simulador da maquina
    def executaPasssos(self):
        if((self.fita.cabecote == -1) and (self.inicio == False)):
            # Para escrever uma vez antes de executar qualquer passo ou movimento na maquina
            if(self.modo == self.MODO_VERBOSE):
                for b in range(0, len(self.listBlocos), 1):
                    for t in range(0, len(self.listBlocos[b].estadoAtual), 1):
                        for e in range(0, len(self.listBlocos[b].estadoAtual[t]), 1):
                            print(self.fita.estadoFita(self.listBlocos[b].nome, self.listBlocos[b].estadoAtual[t][e]))
            
            self.fita.moverFita(self.fita.MOV_DIREITA)
            self.inicio = True
            return 0
        
        # Lista para salvar os blocos
        lBlocos = []
        
        # Transacao de bloco
        for b in range(0, len(self.listBlocos), 1):
            nvBloco = self.listBlocos[b].passosBloco(self.fita, self.pilha)
            print(nvBloco)

            # Lista para salvar os blocos
            lAuxBlocos = []

            # Para cada novo bloco na fila de execucao
            for blc in range(0, len(nvBloco), 1):
                # Nao levou a nenhum novo bloco
                if(nvBloco[blc] == None):
                    # Verifica se existe algum bloco para poder retornar
                    if(len(self.pilha) == 0):
                        print('\nAVISO: Não há mais transicoes para processar.\n')

                        # Significa que eh apenas um nvBloco e nao um conjunto de nvBlocos
                        if(len(nvBloco) == 1):
                            self.listBlocos = lAuxBlocos
                            return 1
                    else:
                        # Tenta retornar ate o bloco que o chamou
                        (bloco, estado) = self.pilha.pop()
                        lAuxBlocos.append(bloco)
                # Verifica se eh para parar a execucao
                elif(nvBloco[blc] == 'pare'):
                    return 1
                # Verifica se eh para pausar a execucao, da a oportunidade de reconfigurar a maquina
                elif(nvBloco[blc] == 'pause'):
                    # Foi optado por dar a oportunidade de reconfigurar a maquina na primeira transicao
                    # Para continuar com as mesmas configuracoes, basta apertar ENTER
                    print('\nAVISO: Execução pausada.\n')
                    self.listBlocos = lAuxBlocos
                    return 2
                else:
                    lAuxBlocos.append(nvBloco[blc])

                self.ultimosEstados.append(self.listBlocos[b].estadoAtual)
            
            for pos in range(0, len(lAuxBlocos), 1):
                lBlocos.append(lAuxBlocos[pos])
        
        self.listBlocos = lBlocos
        return 0

    # Procedimento padrao para a execucao da maquina
    def execucao(self):
        # Verifica se o bloco a ser analisado
        if(self.listBlocos == []):
            main = self.retornaBloco('............main')

            # Verifica se existe o bloco main
            if(main == None):
                print('\nERRO: Bloco "main" não especificado.')
                return True
            
            self.listBlocos.append(main)
            
        # Inicia a execucao
        parar = None

        for i in range(0, (self.passos+1), 1):
            # Realiza um passo
            parar = self.executaPasssos()
            
            # Termina
            if(parar == 1):
                exit()
            # Pausa para dar oportunidade de reconfigurar a maquina
            elif(parar == 2):
                break
            # Excedeu o limite de passos
            elif(i == self.passos):
                parar = 2 # Pausa para dar a oportunidade de reconfigurar a maquina

            # Execucao modo verbose, mostra passo a passo da execucao da maquina 
            if(self.modo == self.MODO_VERBOSE):
                sleep(0.05)
            
        # Execucao resume, mostra apenas o ultimo passo de execucao da maquina
        if(self.modo == self.MODO_RESUME):
            for b in range(0, len(self.listBlocos), 1):
                for t in range(0, len(self.ultimosEstados), 1):
                    for e in range(0, len(self.self.ultimosEstados[t]), 1):
                        print(self.fita.estadoFita(self.listBlocos[b].nome, self.ultimosEstados[t][e]))
           
        # Caso ocorra uma pausa, retorna execucao falsa do simulador
        if(parar == 2):
            return False
            
        return True
