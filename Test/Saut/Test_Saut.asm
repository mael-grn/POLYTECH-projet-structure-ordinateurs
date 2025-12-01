    XOR R0 R0 R0
    XOR R1 R1 R1
    XOR R2 R2 R2
    XOR R3 R3 R3
    XOR R4 R4 R4        #Registre de test, si R4 = 99 à la fin, alors il y a un pb
    ADDi R0 R0 1
    JMP A               #True
    ADDi R4 R4 99
A:  JEQU R1 R2 B        #True
C:  ADDi R4 R4 99
B:  JINF R0 R1 C        #False (ne soit pas aller en C)
    JSUP R0 R1 D
    ADDi R4 R4 99
D:  JINF R1 R0 E        #True
    ADDi R4 R4 99
E:  JNEQ R0 R1 F        #True
    ADDi R4 R4 99
F:  ADDi R3 R3 2