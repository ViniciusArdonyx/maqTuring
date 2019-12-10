#
# ------------------------------------------------ #
# Autor: Vinicius Alves de Araujo - Mat.: 0011941
# ------------------------------------------------ #
#

import MaqTuring
from os import path

class Inout:

    # Construtor
    def __init__(self):
        self.mt = None
        self.arquivo = None
        self.nomeArquivo = None
    
    # Verifica os delimitadores no cabecote
    def verifacaCabecote(self, delimitador):
        # Delimitador so pode ter dois caracteres
        if(len(delimitador) != 2):
            return None
        
        return [delimit[0], delimit[1]]

    # Verifica a entrada passada pelo terminal
    def configEntrada(self, argv):
        if(len(argv) < 2):
            print('\nERRO: entrada no terminal incorreta.')
            return None
        else:
            # O arquivo de analisa eh a ultima informacao
            self.nomeArquivo = argv[len(argv)-1]

            # Verifica se o arquivo existe
            if(not (path.exists(self.nomeArquivo))):
                print('\nERRO: Arquivo inexistente.')
                return
            
            # Configuracao padrao para o funcionamento da maquina
            none = [None, None, None] # Apenas para utilizar as constantes da classe da maquina
            config = [MaqTuring.MaqTuring(none).MODO_VERBOSE, MaqTuring.MaqTuring(none).MAX_STEPS, MaqTuring.MaqTuring(none).DELIMITADOR]

            achouCabecote = False
            achouPassos = False

            # Verifica os argumentos
            for i in range(1, (len(argv)-1), 1):
                if(((argv[i] == "-resume") or (argv[i] == "-r")) and (achouCabecote == False) and (achouPassos == False)):
                    config[0] = MaqTuring.MaqTuring(none).MODO_RESUME
                elif(((argv[i] == "-verbose") or (argv[i] == "-v")) and (achouCabecote == False) and (achouPassos == False)):
                    config[0] = MaqTuring.MaqTuring(none).MODO_VERBOSE
                elif(((argv[i] == "-head") or (argv[i] == "-h")) and (achouCabecote == False) and (achouPassos == False)):
                    achouCabecote = True
                elif(((argv[i] == "-step") or (argv[i] == "-s")) and (achouCabecote == False) and (achouPassos == False)):
                    achouPassos = True
                elif(achouPassos):
                    config[1] = int(argv[i])
                    achouPassos = False
                elif(achouCabecote):
                    delim = self.verifacaCabecote(argv[i])

                    if(delim == None):
                        print("\nDelimitador " + argv[i] + " invalido.")
                        return None
                
                    config[2] = delim
                    achouCabecote = False
            
            return config
    
    # Disponibiliza a oportunidade de reconfigurar a maquina quando atinge o maximo de passos (step's)
    def reconfigEntrada(self, config):
        print('\nAVISO: foi alcançando o limite de passos.\n'+'Aperte enter para continuar ou configure a máquina para continuar a execução:')
        print('-v ou -verbose\n'+'\n-r ou -resume\n'+'\n-s # ou -step #\n'+'\n-h "[]" ou -head "[]"\n')
        entrada = input('Configuração: ')
        print()

        ent = entrada.split()

        # Configuracao padrao para o funcionamento da maquina
        none = [None, None, None] # Apenas para utilizar as constantes da classe da maquina
        # Busca as configuracoes anteriores
        reConfig = [config[0], config[1], config[2]]

        achouPassos = False
        achouCabecote = False

        # Verifica os argumentos
        for i in range(0, len(ent), 1):
            if(((ent[i] == "-resume") or (ent[i] == "-r")) and (achouCabecote == False) and (achouPassos == False)):
                reConfig[0] = MaqTuring.MaqTuring(none).MODO_RESUME
            elif(((ent[i] == "-verbose") or (ent[i] == "-v")) and (achouCabecote == False) and (achouPassos == False)):
                reConfig[0] = MaqTuring.MaqTuring(none).MODO_VERBOSE
            elif(((ent[i] == "-head") or (ent[i] == "-h")) and (achouCabecote == False) and (achouPassos == False)):
                achouCabecote = True
            elif(((ent[i] == "-step") or (ent[i] == "-s")) and (achouCabecote == False) and (achouPassos == False)):
                achouPassos = True
            elif achouPassos:
                reConfig[1] = int(ent[i])
                achouPassos = False
            elif achouCabecote:
                delim = [ent[1], ent[2]]
                reConfig[2] = delim
                achouCabecote = False
        
        return reConfig

    # Formata o nome do bloco conforme especificado, colocando '.''s
    def formatarBloco(self, nome):
        for i in range(0, (16 - len(nome)), 1):
            nome = "." + nome
        
        return nome

    # Formata o nome do estado conforme especificado
    def formatarEstado(self, estado):
        if(estado == 'retorne'):
            return 'retorne'
        elif(estado == 'pare'):
            return 'pare'
        
        try:
            strEstado = str(int(estado))
            
            for i in range(0, (4 - len(strEstado))):
                strEstado = '0' + strEstado
            
            return strEstado
        except ValueError:
            print('\nERRO: (' + estado + '). Nome de estado invalido.')

    # Formata e adiciona o bloco na maquina
    def adicionarBloco(self, maquina, itensLinha):
        nome = self.formatarBloco(itensLinha[1])
        inicial = self.formatarEstado(itensLinha[2])
        maquina.addBloco(nome, inicial)

        return nome

    # Adiciona transicao ou um bloco de transicao
    def adicionarTransicao(self, maquina, itensLinha, bloco, idTransicao):
        if(itensLinha[2] == "--"):
            partida = self.formatarEstado(itensLinha[0])
            simboloAtual = itensLinha[1]
            simboloNovo = itensLinha[3]
            movimento = itensLinha[4]
            destino = self.formatarEstado(itensLinha[5])

            pause = False

            if(len(itensLinha) > 6):
                pare = itensLinha[6]

                if(pare == "!"):
                    pause = True
            
            maquina.addTransicao(idTransicao, partida, simboloAtual, destino, simboloNovo, movimento, bloco, pause)
        else:
            inicial = self.formatarEstado(itensLinha[0])
            destino = self.formatarBloco(itensLinha[1])
            retornoBloco = self.formatarEstado(itensLinha[2])

            maquina.addBlocoTransicao(inicial, retornoBloco, bloco, destino)

    # Interpreta o arquivo passado, identificando blocos, transicoes e etc
    def arquivoEntrada(self, maquina):
        blocoAtual = ''
        idTransicao = -1 

        try:
            self.arquivo = open(self.nomeArquivo, 'r')

            for linha in self.arquivo:
                # Transforma toda a linha em um vetor com informacoes que estavam na linha separados por espaco
                itensLinha = linha.split()

                # Ignora comentarios ou linhas vazia
                if((len(itensLinha) == 0) or (itensLinha[0] == ';')):
                    continue
                # Inicio de um novo bloco
                elif(itensLinha[0] == 'bloco'):
                    blocoAtual = self.adicionarBloco(maquina, itensLinha)
                # Fim do bloco
                elif itensLinha[0] == 'fim':
                    continue
                # transicao
                else:
                    idTransicao += 1
                    self.adicionarTransicao(maquina, itensLinha, blocoAtual, idTransicao)
        except IOError:
            print('\nERRO: Não foi possível abrir o arquivo.')
