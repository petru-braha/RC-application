import flet as ft

left_panel = ft.Container(
        width=250,
        bgcolor=ft.Colors.BLUE_GREY_900,
        padding=10,
        content=ft.Column([
            connection_list,
            ft.Divider(),
            ft.Row([static_connect_btn], alignment=ft.MainAxisAlignment.CENTER),
        ], expand=True)
    )