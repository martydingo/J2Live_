from nicegui import ui
from config import siteLogo


def AppHeader():
    with ui.row().classes("h-5 mb-2 -mt-1"):
        ui.html(siteLogo)
        ui.markdown("J2Live").classes(
            "text-xl -ml-3 font-serif -mt-1 tracking-widest font-medium"
        )
