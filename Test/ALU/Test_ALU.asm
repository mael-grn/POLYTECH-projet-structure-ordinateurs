    XOR R0 R0 R0
    XOR R1 R1 R1
    XOR R2 R2 R2
    XOR R3 R3 R3
    XOR R4 R4 R4
    XOR R5 R5 R5
    XOR R6 R6 R6
    XOR R7 R7 R7
    ADDi R0 R0 5        #R0 = 5
    SUBi R1 R1 1        #R1 = -1
    ADD R2 R0 R1        #R2 = 4
    SUB R3 R0 R1        #R3 = 6
    AND R4 R2 R3        #R4 = 4
    OR R5 R2 R3         #R5 = 6
    XOR R6 R2 R3        #R6 = 2
    SL R0 R0 R6         #R0 = 20
    SR R0 R0 R6         #R0 = 5
    MOD R7 R6 R3        #R7 = 2