#
# ------------------------------------------------ #
# Autor: Vinicius Alves de Araujo - Mat.: 0011941
# ------------------------------------------------ #
#

class Transicao:

    # Construtor
    def __init__(self, idTransicao, epartida, satual, edestino, snovo, movimento, pause):
        self.id             = idTransicao
        self.estado_partida = epartida
        self.simbolo_atual  = satual
        self.estado_destino = edestino 
        self.simbolo_novo   = snovo
        self.movimento      = movimento
        self.pause          = pause

    # Para evitar de adicionar a mesma transicao mais de uma vez na maquina
    def equals(self, transicao):
        if((self.estado_partida == transicao.estado_partida) and
            (self.estado_destino == transicao.estado_destino) and
            (self.simbolo_atual == transicao.simbolo_atual) and
            (self.simbolo_novo == transicao.simbolo_novo) and
            (self.movimento == transicao.movimento)):
            return True
        
        return False

    # Criar funcao que verifica transicoes equivalentes com multiplos caminhos