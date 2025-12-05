MAIN:   ADDI R0, R0, 1
        CALL INC2
        JMP END
INC2:   ADDI R0, R0, 1
        ADDI R0, R0, 1
        RET
END:    JMP END