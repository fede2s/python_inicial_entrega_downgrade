import flet

import sqlite3

def crear_base(nombre_base):
    con = sqlite3.connect(nombre_base)
    con.commit()
    con.close()

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



def actualizar_registro(
        nombre_base,
        nombre_tabla,
        id,
        nuevos_datos):
    #armo la cantidad de placeholders necesarios para la cantidad de
    #campos
    sql = f"UPDATE {nombre_tabla} SET "

    nombres_columnas = obtener_columnas(
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

class ControladorDeTablas:
    def __init__(self,
            page,
            nombre_base_de_datos="federico_dos_santos.db",
            nombre_tabla="agenda_de_guardias",
            campos_de_tabla=[
                "id INTEGER PRIMARY KEY AUTOINCREMENT",
                "fecha DATE NOT NULL",
                "hora_inicio TIME NOT NULL",
                "ID_EMPLEADO INTEGER NOT NULL",
                "ID_SUPLENTE INTEGER NOT NULL"
            ]):
        self.vista = vista_tab.VistaABMCDeTablas(page,nombre_tabla)
        self.nombre_base_de_datos = nombre_base_de_datos
        self.nombre_tabla = nombre_tabla
        self.campos_de_tabla = campos_de_tabla
        self.vista.page.controls.clear()
        self.inicializar()

    def inicializar(self):
        def alta(e):
            datos = []
            #armo los datos a insertar en una lista
            for campo in self.vista.registro_modificable.controls:
                datos.append(campo.value)
            #valido la clave
            if lib_regex_clave.validar_clave(datos[0]) == False:
                self.vista.alerta_evento.title = 'Clave inválida'
                alerta(e)
                return

            #llamo a la funcion insertar datos en sqlite3
            try:
                lib_alta.insertar_datos(
                    self.nombre_base_de_datos, 
                    self.nombre_tabla, 
                    datos 
                )
                datos = lib_consulta.consultar_tabla(
                    self.nombre_base_de_datos, 
                    self.nombre_tabla
                )
                self.actualizar_vista()
                self.vista.alerta_evento.title = \
                    'Registro agregado a base de datos'
                alerta(e)
            except Exception as error:
                print(error)
                self.vista.alerta_evento.title = \
                    'No se pudo insertar el registro'
                alerta(e)
            
            
            
        def alerta(e):
            e.control.page.overlay.append(self.vista.alerta_evento)
            self.vista.alerta_evento.open = True
            e.control.page.update()
        
        def baja(e):
            #selecciono la primera celda del registro
            id = self.vista.registro_modificable.controls[0].value

            #verifico si existe, porque sino no lo puedo borrar\
            #  y debo informarlo
            registro = lib_consulta.consultar_tabla(
                self.nombre_base_de_datos,
                self.nombre_tabla,
                id
            )
            if registro == []:
                self.vista.alerta_evento.title=\
                    f'No existe el registro {id\
                    }, no se puede borrar'
                alerta(e)
                return
            
            try:
                lib_baja.borrar_registro(
                    self.nombre_base_de_datos, 
                    self.nombre_tabla, 
                    id
                )
                self.actualizar_vista()
                self.vista.alerta_evento.title = \
                    f'Registro con id={id} eliminado'
            except Exception as error:
                self.vista.alerta_evento.title = \
                    f'Error al borrar el registro con id={id}'
                print(error)
            alerta(e)

        def modificacion(e):
            id = self.vista.registro_modificable.controls[0].value

            #verifico si existe, porque sino no lo puedo modificar\
            #  y debo informarlo
            registro = lib_consulta.consultar_tabla(
                self.nombre_base_de_datos,
                self.nombre_tabla,
                id
            )
            if registro == []:
                self.vista.alerta_evento.title=\
                    f'No existe el registro {id\
                    }, no se puede modificar'
                alerta(e)
                return
            
            nuevos_datos_celdas = \
                self.vista.registro_modificable.controls[1:]
            nuevos_datos = []
            for celda in nuevos_datos_celdas:
                print(celda.value)
                nuevos_datos.append(celda.value)
                print(nuevos_datos)

            try:
                lib_modificacion.actualizar_registro(
                    self.nombre_base_de_datos,
                    self.nombre_tabla,
                    id,
                    tuple(nuevos_datos))
                self.actualizar_vista()
                self.vista.alerta_evento.title = \
                    f'Registro con id={id} actualizado'
            except Exception as error:
                self.vista.alerta_evento.title = \
                    f'No se pudo actualizar el registro con id={id}'
                print(error)
            alerta(e)
        
        #Creo la base si es que no existe
        cb.crear_base(self.nombre_base_de_datos)
        #Crear tabla de base de datos
        crear_tb.crear_tabla(
            self.nombre_base_de_datos, 
            self.nombre_tabla, 
            self.campos_de_tabla
        )
        #Cargo una lista de tuplas con los datos de la consulta sql
        self.vista.datos = lib_consulta.consultar_tabla(
            self.nombre_base_de_datos,
            self.nombre_tabla
        )
        # Cargo los titulos de las columnas
        self.vista.titulos_columnas = con_col.obtener_columnas(
            self.nombre_base_de_datos,
            self.nombre_tabla
        )
        # Inicializo la vista, requiere que previamente se haya
        # cargado datos y nombres de columnas en sus atributos
        # asi puede crear la tabla GUI. También necesita que le
        # pase por parámetros las funciones de los botones al
        # momento de inicializar los objetos GUI.
        self.vista.inicializar_vista(
            alta,
            baja,
            modificacion
        )
        
    def actualizar_vista(self):
        # Piso los datos viejos con los datos nuevos
        self.vista.datos = lib_consulta.consultar_tabla(
            self.nombre_base_de_datos,
            self.nombre_tabla
        )
        # De los objetos GUI actualizo solo la tabla
        self.vista.actualizar_tabla()

def main(page:flet.Page):
    ejecutar_controlador(page)
    print(page)

flet.app(target=main)
