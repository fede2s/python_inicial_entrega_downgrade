import modelo.db_01_crear_base as cb
import modelo.db_02_crear_tabla as crear_tb
import modelo.db_03_insertar_datos as lib_alta
import modelo.db_04_borrar_registro as lib_baja
import modelo.db_05_actualizar_registro as lib_modificacion
import modelo.db_06_consultar_tabla as lib_consulta
import modelo.db_08_consultar_columnas as con_col
import vista.vista_abmc_tabla as vista_tab
import modelo.regex_validar_clave as lib_regex_clave

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