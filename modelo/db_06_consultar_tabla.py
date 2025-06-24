import sqlite3

def consultar_tabla(
        nombre_base,
        nombre_tabla,
        id = None):
    if id is None:
        print("No se especificó un ID para consultar.")
        try:
            con = sqlite3.connect(nombre_base)
            cursor = con.cursor()

            sql = f"SELECT * FROM {nombre_tabla};"
            cursor.execute(sql)
            registros = cursor.fetchall()
            for registro in registros:
                print(f"Registro leido: {registro}")
            con.commit()
            con.close()
            return registros
        except Exception as e:
            print(f"Error al consultar la tabla: {e}")
            con.commit()
            con.close()
            return None
    else:
        try:
            con = sqlite3.connect(nombre_base)
            cursor = con.cursor()
            sql = f"SELECT * FROM {nombre_tabla} WHERE id = ?;"
            data = (id,)
            cursor.execute(sql, data)
            registros = cursor.fetchall()
            for registro in registros:
                print(f"Registro leido: {registro}")
            con.commit()
            con.close()
            return registros
        except Exception as e:
            print(f"Error al consultar la tabla: {e}")
            con.commit()
            con.close()
            return []