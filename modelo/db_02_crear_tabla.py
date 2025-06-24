import sqlite3

def crear_tabla(
        nombre_base, 
        nombre_tabla, 
        campos):
    campos = ', '.join(campos)
    sql = f"CREATE TABLE if not exists {nombre_tabla} ({campos});"
    try:
        con = sqlite3.connect(nombre_base)
        cursor = con.cursor()
        cursor.execute(sql)
        con.commit()
        print(f"Tabla '{nombre_tabla}' creada exitosamente.")
        con.close()
    except Exception as e:
        print(f"Error al crear la tabla: {e}")
        con.commit()
        con.close()