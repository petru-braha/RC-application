import threading
import flet as ft

class LogBox(ft.Container):
    """
    A temporary notification box that appears at the top of the screen.
    It automatically fades away after a few seconds or can be closed manually.
    """

    def __init__(self, msg: str) -> None:
        super().__init__(ft.Row(
            controls=[
                ft.Text(msg, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                ft.Container(width=10), # Spacer
                ft.IconButton(
                    icon=ft.Icons.CLOSE, 
                    icon_color=ft.Colors.WHITE_70, 
                    icon_size=16,
                    on_click=self.close
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ))
        
        self.duration_seconds = 3.0
        
        # Visual configuration
        self.bgcolor = ft.Colors.BLACK_54
        self.border_radius = 5
        self.padding = ft.Padding.symmetric(horizontal=20, vertical=10)
        self.margin = ft.Margin.only(top=50)
        
        # Animation
        self.animate_opacity = 300 # ms
        self.opacity = 1.0 # Start visible
        
    def did_mount(self):
        """
        Called when the control is added to the page.
        """
        # Start the timer to fade out
        self.timer = threading.Timer(self.duration_seconds, self.fade_out)
        self.timer.start()

    def will_unmount(self):
        """
        Called when the control is removed.
        """
        if hasattr(self, 'timer') and self.timer:
            self.timer.cancel()

    def fade_out(self):
        self.opacity = 0
        self.update()
        
    def close(self, e=None):
        self.fade_out()
        # Optionally, we could strictly remove self from parent here if we had reference.
        # But setting opacity to 0 visually hides it as requested "fades away".
