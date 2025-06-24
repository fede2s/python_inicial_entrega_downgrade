import re

def validar_clave(clave):
    """
    las claves deben ser patron numerico
    Al menos 1 numero
    Menos de 10 numeros porque el integer de SQL 
    llega a 2.147.483.647
    """
    patron = re.compile('[0-9]{1,10}')
    if patron.match(clave):
        return True
    else:
        return False