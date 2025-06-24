import sqlite3

def borrar_registro(
        nombre_base,
        nombre_tabla,
        id):
    sql = f"DELETE FROM {nombre_tabla} WHERE id = ?"
    data = (id,)
    con = sqlite3.connect(nombre_base)
    cursor = con.cursor()
    cursor.execute(sql, data)
    con.commit()
    con.close()
    


