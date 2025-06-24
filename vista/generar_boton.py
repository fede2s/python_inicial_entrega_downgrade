import flet

def generar_boton(texto, funcion):
    """
    Genera un botón de Flet con el texto especificado y una 
    función opcional para el evento on_click.

    :param texto: Texto que se mostrará en el botón.
    :param on_click: Función que se ejecutará al hacer clic 
    en el botón (opcional).
    :return: Un objeto Button de Flet.
    """
    return flet.OutlinedButton(text=texto, on_click=funcion)