import flet as ft
import vista.vista_abmc_tabla as vista_tab
import vista.generar_separadores as gen_sep
import vista.generar_tabla as gen_tab
import modelo.db_08_consultar_columnas as con_col
import vista.generar_boton as lib_botones
import vista.generar_filas as lib_filas
import vista.generar_columnas as lib_columnas
import vista.alerta_evento as lib_alerta
import vista.generar_filas_para_tablas as lib_filas_tabla


class VistaABMCDeTablas:
    def __init__(self, page, nombre_tabla):
        #configuración
        self.page = page
        self.page.title = f"ABMC de tabla {nombre_tabla}"
        self.page.scroll = "always"
        self.page.update()

        #para funcionamiento
        self.titulos_columnas = []
        self.datos = []

        #Objetos visibles
        self.botones = None
        self.registro_modificable = None
        self.tabla = None
        self.separador = None
        self.alerta_evento = ft.AlertDialog(
            title=ft.Text('')
        )

    def inicializar_tabla(self):
        #genero una tabla de forma dinamica con la tabla que estoy
        # consultando y con la vista que tengo para tablas
        self.tabla = gen_tab.generar_tabla(
            columnas_txt = self.titulos_columnas, 
            filas_lista_txt = self.datos
        )

    def actualizar_tabla(self):
        self.tabla.rows.clear()
        self.tabla.rows = lib_filas_tabla.generar_filas(self.datos)
        self.page.update()


    def inicializar_botones(self,
                            funcion_alta,
                            funcion_baja,
                            funcion_modificacion):
        boton_alta = lib_botones.generar_boton("Alta",
                                                funcion_alta
                                        )                       
        boton_baja = lib_botones.generar_boton("Baja",
                                                funcion_baja
                                           )
        boton_modificacion = lib_botones.generar_boton(
            "Modificacion",
            funcion_modificacion)
        
        self.botones = lib_filas.generar_filas([boton_alta,
                                                boton_baja,
                                                boton_modificacion
                                                ])
        
    def inicializar_registro_modificable(self):
        registro_modificable = []
        for campo in self.titulos_columnas:
            registro_modificable.append(ft.TextField(value='',
                                                label=campo,
                                                width=150
                                                )
                                        )
        self.registro_modificable = \
            lib_filas.generar_filas(registro_modificable)
    
    def inicializar_vista(
            self,
            alta,
            baja,
            modificacion):
        self.inicializar_botones(alta,baja,modificacion)
        self.inicializar_registro_modificable()
        self.inicializar_tabla()
        """----------------------------------------------------------
        Formulario: 
        es una columnas donde 1era fila va la fila de botones
        en segunda fila va una fila de celdas modificables
        """
        formulario = lib_columnas.generar_columnas([
            self.botones,
            self.registro_modificable
        ])
       
        """----------------------------------------------------------
        Genero un separador que separa con una línea móvil al
        formulario de la tabla.
        Finalmente el formulario que contiene todos los objetos
        a la página.
        """
        self.separador = gen_sep.generar_separador(
            self.page, 
            formulario, 
            self.tabla
            )
        self.page.add(self.separador)