import sqlite3

def listar_tablas(nombre_base):
    con = sqlite3.connect(nombre_base)
    cursor = con.cursor()
    #sql= "SHOW TABLES FROM base.db;"
    sql="SELECT name FROM sqlite_master WHERE type='table';"
    cursor.execute(sql)
    tablas = cursor.fetchall()
    for tabla in tablas:
        print(f"Tabla: {tabla[0]}")
    con.commit()
    con.close()
    return tablas