import flet as ft
import sqlite3
import re

#Anotaciones
# Dado que me quitó la posibilidad de usar POO parametricé todas las funciones para usar funciones en lugar de métodos, donde previamente se me hacía muy fácil compartir entre métodos variables como atributos de una clase.
# Como anteriormente utilicé el objeto vista como atributo del objeto controlador, ahora creo una variable vista que pertenece al stack de la función controlador.
# El único atributo que no logré parametrizar es alerta_evento, porque se agrega a la página solo cuando se necesita mostrar, luego se quita
# como usted enseñó variables globales me tomé el atrevimiento de usar una para este caso particular
global alerta_evento

# Adicionalmente, dejo un breve resumen de cómo acceder a los objetos de flet de la vista, que previamente eran super fáciles de acceder con un self.atributo en la vista
# tuve que debuguear para poder llegar a ellos ya que no están más como atributos

# mi vista la hice componiendo funciones con objetos de flet
# mi vista contiene parte alta, parte baja y un separador en el medio
# la parte alta tiene un formulario: 1 columna de 2 filas (fila de botones y fila de registro modificable)
# la parte baja tiene una tabla)

#si quiero acceder al registro_modificable
# antes era self.registro_modificable
# ahora tengo que conocer como cada objeto flet guarda internamente otros objetos de flet
# conceptualmente, ahora es: vista.formulario.columna.fila_registro.campos_de_texto
# en la práctica, ahora es: vista.controls[0].content.controls[1].controls

#si quiero acceder a la tabla
# antes era: self.tabla
# ahora es:vista.controls[2].content.controls

#modelo SQLITE3
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
    # aparte de downgradear el código a pedido del profe al paradigma imperativo, agregué este manejo de errores porque me dio problemas probando para el recuperatorio si trato de insertar 2 veces el mismo id
    try:
        sql = f"INSERT INTO {nombre_tabla} VALUES ({placeholders})"
        cursor.execute(sql, datos)
        con.commit()
        con.close()
    except Exception as error:
        print (error)
        con.close()
        return error

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
        print(f"Error al obtener las columnas de la tabla '{nombre_tabla}': {e}")
        con.commit()
        con.close()
        return []
#Modelo REGEX
def validar_clave(clave):
    patron = re.compile('[0-9]{1,10}')
    if patron.match(clave):
        return True
    else:
        return False

#VISTA - funciones para abstraer objetos de flet
def generar_alerta(texto):
    dlg = ft.AlertDialog(
        title=ft.Text(texto), on_dismiss=lambda e: print("Dialog dismissed!")
    )
    def open_dlg(e):
        e.control.page.overlay.append(dlg)
        dlg.open = True
        e.control.page.update()
    return ft.Column(
        [
            ft.ElevatedButton(texto, on_click=open_dlg)
        ]
    )

def generar_boton(texto, funcion):
    return ft.OutlinedButton(text=texto, on_click=funcion)

# basado en documentación oficial de flet tal cual como el profe nos mandó a buscar si es que queríamos implementar flet. 
#simplificado de ejemplo en https://flet.dev/docs/controls/column
def generar_columnas(objetos):
    return ft.Column(spacing=50, controls=objetos)

def generar_filas_para_tabla(datos):
    filas =[]
    for dato in datos:
        celdas = []
        for campo in dato:
            celdas.append(ft.DataCell(ft.Text(campo)))
        filas.append(ft.DataRow(celdas))
        
    return filas

# basado en documentación oficial de flet tal cual como el profe nos mandó a buscar si es que queríamos implementar flet. 
# encontré como generar una fila de contenedores acá
# https://flet.dev/docs/controls/container/
def generar_filas(objetos):
    return ft.Row(objetos)

#funcion copiada de documentación oficial de flet tal cual como el profe nos mandó a buscar si es que queríamos implementar flet. https://github.com/flet-dev/examples/blob/main/python/apps/controls-gallery/examples/layout/divider/02_draggable_divider.py
def generar_separador(
    page,
    botones,
    tabla):
        
        def move_divider(e: ft.DragUpdateEvent):
            if (e.delta_y > 0 and c.height < 300) or (e.delta_y < 0 and c.height > 100):
                c.height += e.delta_y
            c.update()

        def show_draggable_cursor(e: ft.HoverEvent):
            e.control.mouse_cursor = ft.MouseCursor.RESIZE_UP_DOWN
            e.control.update()

        c = ft.Container(
            #bgcolor=ft.Colors.AMBER,
            alignment=ft.alignment.center,
            height=150,
            # expand=1,
            content=botones #+ formulario
        )

        return ft.Column(
            [
                c,
                ft.GestureDetector(
                    content=ft.Divider(),
                    on_pan_update=move_divider,
                    on_hover=show_draggable_cursor,
                ),
                ft.Container(
                    #bgcolor=ft.Colors.PINK, 
                    alignment=ft.alignment.center_left, 
                    expand=1,
                    content = tabla
                ),
            ],
            spacing=0,
            scroll= True
        )

#  copiado de documentación oficial tal cual como el profe nos mandó a buscar si es que queríamos implementar flet.
# copiado de https://github.com/flet-dev/examples/blob/main/python/apps/controls-gallery/examples/layout/datatable/01_basic_datatable.py
# lo hice dinamico para que reciba una lista de titulos de columnas
# y una lista de filas, donde cada fila es una lista de celdas
def generar_tabla(columnas_txt, filas_lista_txt):
    columnas =[]
    filas = []
    for columna in columnas_txt:
        columnas.append(ft.DataColumn(ft.Text(columna)))
    for fila in filas_lista_txt:
        celdas = []
        for celda in fila:
            celdas.append(ft.DataCell(ft.Text(celda)))#,disabled=False))
        filas.append(ft.DataRow(cells=celdas))
    return ft.DataTable(
            columns=columnas,
            rows=filas
        )
# vista - generación de objetos de flet a partir de las funciones previamente realizadas
def generar_vista( page, nombre_tabla,titulos_columnas,datos,alta,baja,modificacion):
    #configuración
    global alerta_evento
    page = page
    page.title = f"ABMC de tabla {nombre_tabla}"
    page.scroll = "always"
    page.update()

    #Objetos visibles
    botones = None
    registro_modificable = None
    tabla = None
    separador = None
    alerta_evento = ft.AlertDialog(
        title=ft.Text('')
    )
    
    #Incializar
    botones = inicializar_botones(alta,baja,modificacion)
    registro_modificable = inicializar_registro_modificable(titulos_columnas)
    tabla = inicializar_tabla(titulos_columnas, datos)
    formulario = generar_columnas([
        botones,
        registro_modificable
    ])
    separador = generar_separador(
        page, 
        formulario, 
        tabla
        )
    page.add(separador)
    page.add(alerta_evento)
    return separador

def inicializar_tabla(titulos_columnas, datos):
    #genero una tabla de forma dinamica con la tabla que estoy
    # consultando y con la vista que tengo para tablas
    tabla = generar_tabla(
        columnas_txt = titulos_columnas, 
        filas_lista_txt = datos
    )
    return tabla

def actualizar_tabla(page,tabla,datos):
    tabla.rows.clear()
    tabla.rows = generar_filas_para_tabla(datos)
    page.update()

def inicializar_botones(funcion_alta,funcion_baja,funcion_modificacion):
    boton_alta = generar_boton("Alta", funcion_alta)                       
    boton_baja = generar_boton("Baja", funcion_baja)
    boton_modificacion = generar_boton("Modificacion", funcion_modificacion)
    botones = generar_filas([boton_alta, boton_baja, boton_modificacion])
    return botones

def inicializar_registro_modificable(titulos_columnas):
    registro_modificable = []
    for campo in titulos_columnas:
        registro_modificable.append(ft.TextField( value='', label=campo, width=150) )
    registro_modificable = generar_filas(registro_modificable)
    return registro_modificable

#Controlador
def ejecutar_controlador(
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

    def alta(e):
        global alerta_evento
        datos = []
        #armo los datos a insertar en una lista
        for campo in vista.controls[0].content.controls[1].controls:
            datos.append(campo.value)
        #valido la clave
        if validar_clave(datos[0]) == False:
            alerta_evento.title = 'Clave inválida'
            alerta(e)
            return

        #llamo a la funcion insertar datos en sqlite3
        try:
            error_base = insertar_datos(
                nombre_base_de_datos, 
                nombre_tabla, 
                datos 
            )
            datos = consultar_tabla(
                nombre_base_de_datos, 
                nombre_tabla
            )
            # aparte de downgradear el código a pedido del profe al paradigma imperativo, agregué este manejo de errores porque me dio problemas probando para el recuperatorio si trato de insertar 2 veces el mismo id
            if error_base is not None:
                alerta_evento.title = 'No se pudo insertar el registro'
                alerta(e)
                return
            actualizar_vista(page,vista,nombre_base_de_datos,nombre_tabla)
            alerta_evento.title = 'Registro agregado a base de datos'
            alerta(e)
        except Exception as error:
            print(error)
            alerta_evento.title = 'No se pudo insertar el registro'
            alerta(e)
        
    def alerta(e):
        global alerta_evento
        e.control.page.overlay.append(alerta_evento)
        alerta_evento.open = True
        e.control.page.update()
    
    def baja(e):
        global alerta_evento
        #selecciono la primera celda del registro
        id = vista.controls[0].content.controls[1].controls[0].value

        #verifico si existe, porque sino no lo puedo borrar
        #  y debo informarlo
        registro = consultar_tabla(
            nombre_base_de_datos,
            nombre_tabla,
            id
        )
        if registro == []:
            alerta_evento.title= f'No existe el registro {id}, no se puede borrar'
            alerta(e)
            return
        
        try:
            borrar_registro(
                nombre_base_de_datos, 
                nombre_tabla, 
                id
            )
            actualizar_vista(page,vista,nombre_base_de_datos,nombre_tabla)
            alerta_evento.title = f'Registro con id={id} eliminado'
        except Exception as error:
            alerta_evento.title = f'Error al borrar el registro con id={id}'
            print(error)
        alerta(e)

    def modificacion(e):
        global alerta_evento
        id = vista.controls[0].content.controls[1].controls[0].value

        #verifico si existe, porque sino no lo puedo modificar
        #  y debo informarlo
        registro = consultar_tabla(
            nombre_base_de_datos,
            nombre_tabla,
            id
        )
        if registro == []:
            alerta_evento.title= f'No existe el registro {id}, no se puede modificar'
            alerta(e)
            return
        
        nuevos_datos_celdas = vista.controls[0].content.controls[1].controls[1:]
        nuevos_datos = []
        for celda in nuevos_datos_celdas:
            print(celda.value)
            nuevos_datos.append(celda.value)
            print(nuevos_datos)

        try:
            actualizar_registro(
                nombre_base_de_datos,
                nombre_tabla,
                id,
                tuple(nuevos_datos))
            actualizar_vista(page,vista,nombre_base_de_datos,nombre_tabla)
            alerta_evento.title = f'Registro con id={id} actualizado'
        except Exception as error:
            vista.alerta_evento.title = f'No se pudo actualizar el registro con id={id}'
            print(error)
        alerta(e)

    #Creo la base si es que no existe
    crear_base(nombre_base_de_datos)
    #Crear tabla de base de datos
    crear_tabla(
        nombre_base_de_datos, 
        nombre_tabla, 
        campos_de_tabla
    )
    #Cargo una lista de tuplas con los datos de la consulta sql
    datos = consultar_tabla(
        nombre_base_de_datos,
        nombre_tabla
    )
    # Cargo los titulos de las columnas
    titulos_columnas = obtener_columnas(
        nombre_base_de_datos,
        nombre_tabla
    )
    # Inicializo la vista, requiere que previamente se haya
    # cargado datos y nombres de columnas en sus atributos
    # asi puede crear la tabla GUI. También necesita que le
    # pase por parámetros las funciones de los botones al
    # momento de inicializar los objetos GUI.
    vista = generar_vista( page, nombre_tabla,titulos_columnas,datos,alta,baja,modificacion)
    
def actualizar_vista(page,vista,nombre_base_de_datos,nombre_tabla):
    # Piso los datos viejos con los datos nuevos
    datos = consultar_tabla(
        nombre_base_de_datos,
        nombre_tabla
    )
    # De los objetos GUI actualizo solo la tabla
    actualizar_tabla(page,vista.controls[2].content,datos)

# MAIN
def main(page:ft.Page):
    ejecutar_controlador(page)
    print(page)

ft.app(target=main)
