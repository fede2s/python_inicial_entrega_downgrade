import sqlite3
import modelo.db_08_consultar_columnas as lib_col

def actualizar_registro(
        nombre_base,
        nombre_tabla,
        id,
        nuevos_datos):
    #armo la cantidad de placeholders necesarios para la cantidad de
    #campos
    sql = f"UPDATE {nombre_tabla} SET "

    nombres_columnas = lib_col.obtener_columnas(
        nombre_base,
        nombre_tabla
    )
    campos = nombres_columnas[1:]
    nombreid = nombres_columnas[0]
    
    for campo in campos:
        sql += f"{campo} = ?, "

    sql = sql[:-2]  # Elimino la última coma y espacio
    sql += " WHERE id = ?"

    data = tuple(nuevos_datos + (id,))
    con = sqlite3.connect(nombre_base)
    cursor = con.cursor()
    cursor.execute(sql, data)
    con.commit()
    con.close()