#
# ------------------------------------------------ #
# Autor: Vinicius Alves de Araujo - Mat.: 0011941
# ------------------------------------------------ #
#

class BlocoTransicao:

     # Construtor
    def __init__(self, estadoInicial, retorno, partida, destino):
        self.estadoInicial = estadoInicial
        self.retorno       = retorno
        self.partida       = partida
        self.destino       = destino
    
    # Para evitar de adicionar o mesmo bloco de transicao mais de uma vez na maquina
    def equals(self, transicao):
        if((self.estadoInicial == transicao.estadoInicial) and
            (self.retorno == transicao.retorno) and
            (self.partida.name == transicao.partida.name) and
            (self.destino.name == transicao.destino.name)):
            return True
        
        return False
    
    # Criar funcao que verifica transicoes equivalentes com multiplos caminhos
