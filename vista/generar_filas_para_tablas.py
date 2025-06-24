import flet as ft

def generar_filas(datos):
    filas =[]
    for dato in datos:
        celdas = []
        for campo in dato:
            celdas.append(ft.DataCell(ft.Text(campo)))
        filas.append(ft.DataRow(celdas))
        
    return filas