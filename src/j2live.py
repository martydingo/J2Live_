from multiprocessing import freeze_support

freeze_support()

from nicegui import ui, app, native

from components.AppHeader import AppHeader
from components.Jinja2Editor import Jinja2Editor
from components.TemplatePreview import TemplatePreview
from components.YAMLEditor import YAMLEditor

from config import storageSecret, siteLogo, globalCss, tailwindCss
from themes.nord import NordTheme


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
        "flex w-full h-[90v] justify-evenly items-stretch antialiased lg:w-screen"
    )

    with rootLayout:
        with ui.element().classes(
            "basis-5/12 h-[40.45vh] flex items-stretch justify-around"
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


ui.run(
    show=False,
    storage_secret=storageSecret,
    port=native.find_open_port(),
)
