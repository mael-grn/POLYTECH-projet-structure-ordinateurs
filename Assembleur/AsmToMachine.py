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

CRTL = {
    'JMP' : '000',
    'JEQU' : '001',
    'JNEQ' : '010',
    'JSUP' : '011',
    'JINF' : '100',
}

def decimal_vers_binaire(valeur, nb_bits):
    """
    Convertit une valeur décimale en binaire sur n bits bits.
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


def detecter_labels(fichier_entree):
    """
    Détecte les labels dans le fichier assembleur puis envoie un dictionnaire sous la forme {label: adresse_instruction}
    """
    labels = {}
    adresse = 0  # adresse de l'instruction

    with open(fichier_entree, 'r') as fin:
        for ligne in fin:
            ligne = ligne.strip()
            if not ligne or ligne.startswith('#'):
                continue

            # Si un label est défini au début de la ligne
            if ':' in ligne:
                parts = ligne.split(':', 1)
                label = parts[0].strip()
                reste = parts[1].strip()

                if label in labels:
                    raise ValueError(f"Label déjà défini : {label}")

                labels[label] = adresse  # le label pointe vers l’adresse actuelle

                # S’il y a une instruction après le label, elle compte aussi
                if reste:
                    adresse += 1
            else:
                # ligne d’instruction sans label
                adresse += 1

    return labels


labels = detecter_labels("entree.asm")

def assembler_ligne(ligne):
    """Assemble une ligne UAL ou CRTL en hexadecimal"""
    ligne = ligne.strip()
    if not ligne or ligne.startswith('#') or ligne.endswith(':'):
        return None  # commentaire, ligne vide ou label
    
    if ':' in ligne:
            parts = ligne.split(':', 1)
            # On garde seulement la partie après le label
            ligne = parts[1].strip()
            if not ligne:
                return None 
        
    parts = ligne.replace(',', '').split()
    instr = parts[0].upper()

# Type contrôle (JMP, JEQU, etc.)
    if instr in CRTL:
        type_bits = IR_type['CRTL']
        op_bits = CRTL[instr]

        if instr == 'JMP':
            rs1 = '000'
            rs2 = '000'
            label = parts[1]
        else:
            if len(parts) < 4:
                raise ValueError(f"Instruction de saut incomplète : {ligne}")
            rs1 = REG[parts[1].upper()]
            rs2 = REG[parts[2].upper()]
            label = parts[3]

        if label not in labels:
            raise ValueError(f"Label inconnu : {label}")

        adresse_label = labels[label]
        adresse_bits = decimal_vers_binaire(adresse_label, 16)

        bits = adresse_bits + '0000' + rs2 + rs1 + '0' + op_bits + type_bits
        bits = bits.ljust(32, '0')
        return binaire_vers_hexadecimal(bits)
    
# Type UAL (ADD, SUB, etc.)
    if instr in IR_UAL or instr.endswith('I'):
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
        compteur = 0
        for ligne in fin:
            compteur += 1
            try:
                binaire = assembler_ligne(ligne)
                if binaire:
                    fout.write(binaire + '\n')
            except Exception as e:
                print(f"Erreur ligne '{ligne.strip()}': {e}")
        compteur = decimal_vers_binaire(compteur, 16)
        compteur = binaire_vers_hexadecimal(compteur)
        compteur = compteur[4:]
        fout.write(compteur + "0003")


assembler_fichier("entree.asm", "sortie.raw")
print("Assemblage terminé")
