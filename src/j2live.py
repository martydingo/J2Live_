from multiprocessing import freeze_support

freeze_support()

from nicegui import ui, app, native

from components.AppHeader import AppHeader
from components.Jinja2Editor import Jinja2Editor
from components.TemplatePreview import TemplatePreview
from components.YAMLEditor import YAMLEditor

from config import siteLogo, globalCss, tailwindCss
from themes.nord import NordTheme
from random import SystemRandom
from string import ascii_uppercase, digits
from os import getenv


@ui.page(path="/", title="J2Live", favicon=siteLogo.replace("currentColor", "white"))
async def App():
    ui.dark_mode().enable()
    NordTheme()
    ui.add_css(globalCss)
    ui.add_head_html(tailwindCss)
    ui.add_body_html(
        f"""
            <script src="https://unpkg.com/flourite@1.3.0"></script>
        """
    )

    app.add_static_file(
        local_file="src/assets/MapleMono.ttf", url_path="/assets/MapleMono.ttf"
    )
    app.add_static_file(
        local_file="src/assets/MapleMono.ttf", url_path="/assets/MapleMono-Italic.ttf"
    )

    AppHeader()
    rootLayout = ui.element().classes(
        "flex w-full justify-evenly items-stretch antialiased max-h-sm"
    )

    with rootLayout:
        with ui.element().classes(
            "basis-5/12 h-[39.45vh] flex items-stretch justify-around"
        ):
            yamlEditor = YAMLEditor()
            jinja2Editor = Jinja2Editor()
        with ui.element().classes("basis-5/12 justify-center items-center"):
            templatePreview = TemplatePreview()

            # .bind_content_from(
            #     app.storage.user,
            #     "templatePreviewContent",
            #     lambda template: f"{template}",
            # )


customPort = getenv("PORT")
if customPort != None:
    customPort = int(customPort)
customStorageSecret = getenv("STORAGE_SECRET")
nativeMode = getenv("NATIVE")

if nativeMode == "false":
    ui.run(
        show=False,
        storage_secret=customStorageSecret
        or "".join(SystemRandom().choice(ascii_uppercase + digits) for _ in range(64)),
        port=customPort or native.find_open_port(),
    )

else:
    ui.run(
        show=False,
        storage_secret=customStorageSecret
        or "".join(SystemRandom().choice(ascii_uppercase + digits) for _ in range(64)),
        port=customPort or native.find_open_port(),
        native=True,
        window_size=(1920, 1080),
        frameless=True,
    )
