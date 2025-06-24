import sqlite3

def insertar_datos(
        nombre_base,
        nombre_tabla,
        datos):
    con = sqlite3.connect(nombre_base)
    cursor = con.cursor()
    if len(datos) == 0:
        print("No hay datos para insertar.")
        con.commit()
        con.close()
        return
    #armo la cantidad de placeholders necesarios para la cantidad de
    #datos
    placeholders = ', '.join(['?'] * len(datos))
    print(datos)
    print(placeholders)
    sql = f"INSERT INTO {nombre_tabla} VALUES ({placeholders})"
    cursor.execute(sql, datos)
    con.commit()
    con.close()
