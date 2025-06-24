import flet as ft

#simplificado de ejemplo en https://flet.dev/docs/controls/column
def generar_columnas(objetos):
    return ft.Column(spacing=50, controls=objetos)