IR_type = {
    'UAL' : '00',
    'MEM' : '01',
    'CRTL' : '11',
}

IR_UAL = {
    'ADD' : '000',
    'SUB' : '001',
    'AND' : '010',
    'OR' : '011',
    'XOR' : '100',
    'SL' : '101',
    'SR' : '110',
    'MOD' : '111',
}

REG = {
    'R0' : '000',
    'R1' : '001',
    'R2' : '010',
    'R3' : '011',
    'R4' : '100',
    'R5' : '101',
    'R6' : '110',
    'R7' : '111'
}

def decimal_vers_binaire(valeur, nb_bits):
    """
    Convertit une valeur décimale en binaire sur nb_bits bits, sans utiliser format() ni bin().
    Gère aussi les valeurs négatives en complément à deux.
    """
    # Gestion du complément à deux si valeur négative
    if valeur < 0:
        valeur = (1 << nb_bits) + valeur
    
    bits = []
    
    for i in range(nb_bits):
        bits.append(valeur % 2)
        valeur //= 2
    
    # On inverse les bits
    bits.reverse()
    
    # Conversion en chaîne
    return ''.join(str(bit) for bit in bits)


def binaire_vers_hexadecimal(valeur):
    """Convertit une chaîne binaire en hexadécimal"""
    decimal = 0
    longueur = len(valeur)
    for i in range(longueur):
        bit = int(valeur[longueur - 1 - i])
        decimal += bit * (2 ** i)
    return hex(decimal)[2:].upper().zfill(8)




def assembler_ligne(ligne):
    """Assemble une ligne UAL en hexadecimal"""
    ligne = ligne.strip()
    if not ligne or ligne.startswith('#'):
        return None  # commentaire ou ligne vide
    

    parts = ligne.replace(',', '').split()
    instr = parts[0].upper()

    immediat = instr.endswith('I')
    op = instr[:-1] if immediat else instr

    if op not in IR_UAL:
        raise ValueError(f"Instruction inconnue : {op}")

    type_bits = IR_type['UAL']
    op_bits = IR_UAL[op]
    imm_bit = '1' if immediat else '0'

    rd = REG[parts[1].upper()]
    rs1 = REG[parts[2].upper()]
    rs2 = REG[parts[3].upper()] if not immediat else '000'
    const_bits = decimal_vers_binaire(int(parts[3]), 16) if immediat else '0'*16

    # Construction des bits
    bits = const_bits + '0' + rs2 + rs1 + rd + imm_bit + op_bits + type_bits 
    bits = bits.ljust(32, '0')

    # Inversion pour Logisim
    return binaire_vers_hexadecimal(bits)

def assembler_fichier(entree, sortie):
    with open(entree, 'r') as fin, open(sortie, 'w') as fout:
        fout.write('v2.0 raw' + '\n')
        for ligne in fin:
            try:
                binaire = assembler_ligne(ligne)
                if binaire:
                    fout.write(binaire + '\n')
            except Exception as e:
                print(f"Erreur ligne '{ligne.strip()}': {e}")


assembler_fichier("entree.asm", "sortie.raw")
print("Assemblage terminé")
