import flet as ft

# copiado de https://github.com/flet-dev/examples/blob/main/python/apps/controls-gallery/examples/layout/datatable/01_basic_datatable.py
# lo hice dinamico para que reciba una lista de titulos de columnas
# y una lista de filas, donde cada fila es una lista de celdas
def generar_tabla(columnas_txt, filas_lista_txt):

    columnas =[]
    filas = []
    
    """Ejemplo de parametro columns
    columns=[
        ft.DataColumn(ft.Text("First name")),
        ft.DataColumn(ft.Text("Last name")),
        ft.DataColumn(ft.Text("Age"), numeric=True),
    ],
    """
    for columna in columnas_txt:
        columnas.append(ft.DataColumn(ft.Text(columna)))

    """
    ejemplo de parametro rows
    rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("John")),
                        ft.DataCell(ft.Text("Smith")),
                        ft.DataCell(ft.Text("43")),
                    ],
                ),...
            ],"""
    for fila in filas_lista_txt:
        celdas = []
        for celda in fila:
            celdas.append(ft.DataCell(ft.Text(celda)))#,disabled=False))
        filas.append(ft.DataRow(cells=celdas))



    return ft.DataTable(
            
            columns=columnas,
            
            rows=filas
        )