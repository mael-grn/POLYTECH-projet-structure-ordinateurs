            XOR R1 R1 R1
            XOR R2 R2 R2
            XOR R3 R3 R3
            XOR R7 R7 R7
            JMP Suivant
            ADDi R7 R7 99
Suivant:    ADDi R1 R1 4
            ADDi R2 R2 13
            JINF R1 R2 Inf
            ADDi R7 R7 99
Inf:        ADD R1 R1 R2
            JSUP R1 R2 Sup
            ADDi R7 R7 99
Sup:        JNEQ R1 R2 Neq
            ADDi R7 R7 99
Neq:        ADDi R3 R3 13
            JEQU R2 R3 Equ
            ADDi R7 R7 99
Equ:        ADDi R7 R7 42
