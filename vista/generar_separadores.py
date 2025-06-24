import flet as ft

#funcion copiada de https://github.com/flet-dev/examples/blob/main/python/apps/controls-gallery/examples/layout/divider/02_draggable_divider.py
def generar_separador(
    page,
    botones,
    tabla):
        
        def move_divider(e: ft.DragUpdateEvent):
            if (e.delta_y > 0 and c.height < 300) or \
                (e.delta_y < 0 and c.height > 100):
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