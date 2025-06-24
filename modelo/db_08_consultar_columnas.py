import sqlite3

def obtener_columnas(nombre_base, nombre_tabla):
    try:
        con = sqlite3.connect(nombre_base)
        cursor = con.cursor()
        cursor.execute(f"PRAGMA table_info({nombre_tabla});")
        columnas = cursor.fetchall()
        # Extraer solo los nombres de las columnas
        nombres_columnas = [columna[1] for columna in columnas]
        con.commit()
        con.close()
        return nombres_columnas
    except Exception as e:
        print(f"Error al obtener las columnas de la tabla '{\
            nombre_tabla}': {e}")
        con.commit()
        con.close()
        return []