#
# ------------------------------------------------ #
# Autor: Vinicius Alves de Araujo - Mat.: 0011941
# ------------------------------------------------ #
#

import sys
import Inout
import MaqTuring

def main():
    titulo = 'Simulador de Maquna de Turing com Oráculo version 1.0.\nDesenvolvido como trabalho prático para a disciplina de Teoria da Computacao.\nVinícius Alves de Araújo, IFMG, 2019.\n'
    print(titulo)

    # Analisa a entrada no terminal e verifica as configuracoes para a maquina
    entrada = Inout.Inout()
    config = entrada.configEntrada(sys.argv)

    # Nao houve configuracao alguma para a maquina, logo termina a execucao do programa
    if(config == None):
        exit()
    
    # Cria a simulacao do funcionamento da maquina de turing com oraculo
    simTuring = MaqTuring.MaqTuring(config)
    entrada.arquivoEntrada(simTuring)

    palavra = input('Forneça a palavra: ')

    # Verifica se a entrada e valida para continuar a execucao do programa
    if(not(simTuring.entradaValida(palavra))):
        exit()
    
    executa = True
    
    while executa:
        executa = simTuring.execucao()
        if(not executa):
            config = entrada.reconfigEntrada(config)
            simTuring.resetarConfiguracoes(config)
            executa = True

if __name__ == '__main__':
    main()