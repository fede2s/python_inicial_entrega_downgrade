import sqlite3

def crear_base(nombre_base):
    con = sqlite3.connect(nombre_base)
    con.commit()
    con.close()