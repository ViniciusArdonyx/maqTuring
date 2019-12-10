; MT nao deterministica que aceita a linguagem b*ab* ou c*ac*
; retirado do material Cap4: Máquinas de Turing

bloco main 1
01 b -- B d 01
01 c -- C d 01
01 a -- B d 02
01 a -- C d 04

02 b -- B d 02
02 _ -- _ e 03

03 B -- b e 03
03 _ -- * d 06 

04 c -- C d 04
04 _ -- _ e 05

05 C -- c e 05
05 _ -- * d 06

06 sim pare
fim ; main

bloco moveFim 1
01 _ -- * e retorne
01 * -- * d 01
fim ; moveFim

; aceitou a palavra
bloco sim 1
01 moveFim 02
02 * -- * d 03
03 * -- _ d 04
04 * -- S d 05
05 * -- I d 06
06 * -- M d retorne
fim ; sim
