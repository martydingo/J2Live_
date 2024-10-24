from multiprocessing import freeze_support

freeze_support()

from nicegui import ui, app, native
from nicegui.events import ValueChangeEventArguments

import config

from components.YAMLEditor import YAMLEditor
from components.Jinja2Editor import Jinja2Editor

from _ansible import renderTemplate
from themes.nord import NordTheme


monoFontFamily = '"Maple Mono", ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace'

logo = """
<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 512 512">
	<path fill="currentColor" d="m298.8 497.74l-46.302-1.213l2.389-28.06l1.5-25.658h-6.184v-21.028h-3.752l-.306-9.048l11.161-2.273l.927-77.105l-8.378-.456l.428-20.876l-4.003-.458l.323-10.778h11.252l.1-18.265l-11.17-.14v-8.571h-5.233v-1.92l-2.982.218l-5.509-9.597l42.366-9.093l42.915 10.044l-6.2 8.306l-3.24.18l.216 1.227l-5.727.864l-.58 7.97l-12.261.446l.127 21.716l28.162.499l1.316-36.066l3.263-41.834l-.717-14.176l-88.652 5.106l-74.338 3.802l-1.04 24.642l.002 25.724l-2.37 38.534l32.552.748l-.116-14.378l-8.717.417l-.726-9.377l-6.237.466l-6.085-9.991l36.454-8.08l38.965 8.011l-10.904 8.278l-3.672.541l-.433 7.523l-9.194.907l-.867 17.195l7.774-.585v25.219h-6.317l-1.029 29.301l2.82 27.423l1.246 7.15h5.126l-1.41 29.7l-3.749-.591l1.137 49.089h-34.816l2.84-48.675l-28.192 2.505l-.563 48.625l-55.657-.676l5.374-22.195l2.919-23.015l-42.273 1.04l6.828 49.119l-38.446-.712l1.13-49.969l-7.106-1.186l-2.085-26.587l12.102-1.854v-70.316h-7.368V317.86l-2.215-1.426l-4.078-8.646l13.073-3.324v-16.3l-10.56-.588l-.549-7.125h-3.508l-9.94-8.279l36.386-10.778l45.042 10.847l-4.772 6.679l-9.895 2.229l-1.214 8.962h-11.45l.416 16.27l47.842 2.715l4.772-85.971l-62.598 2.408l-1.26-23.699h-3.131l.979-9.5l2.61-2.792l1.233.005c.253 0 2.83.061 15.136 1.854c8.756 1.269 27.175.353 36.604-.243l-3.611-.631l17.037-15.153v-6.684l-6.108-1.17l-.521-8.41c-5.225.338-16.367 1.009-22.852 1.009c-8.516 0-36.427-2.334-37.614-2.433l-1.922-.16l-6.811-22.98l-13.556-1.219l-3.44-10.951l-22.546-2.797l-9.296-.698L0 109.529l19.647-17.25l-7.374-24.98l5.38 2.112c.212.083 21.74 8.491 51.207 15.614c29.627 7.156 180.51-3.117 259.573-13.363C406.4 61.558 503.35 15.531 504.317 15.067l1.694-.808l5.349 4.759l-6.325 19.318l-7.316 3.834l-.982 5.043L512 80.564l-7.125 5.54l-37.382 10.35l-1.407 3.914l-17.153 4.988l-8.728 23.627l-1.619.267c-.182.03-18.325 3.04-30.973 6.006c-11.057 2.593-37.139 4.598-45.473 5.191l-.433 14.293l-5.793.17l-.121 5.88l16.753 8.771l.314 3.796l4.066-.436c13.357-1.426 54.118-7.44 58.722-8.12h.764l1.162.341l4.422 2.582l.513 8.052l-4.279 1.098l-.267 28.091l-82.082 6.229l-1.608 16.217l3.098 31.192l3.796 17.37l4.493 31.189l35.658.27l-.734-16.52l-11.655.143l-.268-9.095h-4.339l-.26-1.617l-4.763.395l-4.946-9.2l40.115-8.135l43.878 8.827l-12.367 6.19l.486 2.489l-5.54.482l.695 7.716l-12.14 1.079l-.124 17.795l7.081.624v9.817l-2.003-.311v19.246l-4.78.141l.538 57.552l1.029 11.109h6.452l.601 9.175l-1.718.35l-.138 19.117l-5.352.58l1.095 18.485l3.973 30.272l-9.266 2.809l-12.894.286l-15.928-1.445l.143-32.226l1.19-15.939l-26.293.969l1.705 12.32l1.123 21.489l5.338 16.17l-11.708 3.36l-26.19 1.054l-22.23-1.718l.176-28.331l.869-21.442l-28.273.496l.48 12.85l2.93 17.77zm-6.303-88.011l28.568.99l-3.856-32.692l1.034-41.539l-26.81-1.735zm76.79-72.223l3.383 33.87l1.073 36.855l27.57-2.017V336.74zm-296.01-.97l.272 69.03l44.57-2.116l-2.902-11.534V366.5l4.113-27.572zm82.84 1.825l.87 22.441l.136 22.464l1.617 19.682l30.523-.53l-.37-63.935zm3.042-161.774l13.917 7.559l-.42 3.222l39.418-1.55l-.522-.753l.994-7.004l-3.725-5.752l.26-8.26l-4.251-5.009l.918-5.636l-40.247 2.748l-.563 12.758l-6.229.301zm107.124-.05l-.177 3.943l39.652-1.931l1.815-5.523l16.847-11.037l.344-6.836l-8.695-.367l.204-11.213l-43.568 5.404l-1.714 6.841v1.705l-.783 3.97l-1.28 3.05l-.26 8.144z" />
</svg>
"""

globalCss = f"""
@import url('https://fonts.googleapis.com/css2?family=Bai+Jamjuree:ital,wght@0,200;0,300;0,400;0,500;0,600;0,700;1,200;1,300;1,400;1,500;1,600;1,700&family=Titillium+Web:ital,wght@0,200;0,300;0,400;0,600;0,700;0,900;1,200;1,300;1,400;1,600;1,700&display=swap');

:root {{
    --monaco-monospace-font: {monoFontFamily} !important;
}}
"""


tailwindCss = """
    <style type="text/tailwindcss">
        @layer base {
            @font-face {
                font-family: 'Maple Mono';
                font-style: normal;
                src: url(/assets/MapleMono.ttf);
            }

            @font-face {
                font-family: 'Maple Mono';
                font-style: italic;
                src: url(/assets/MapleMono-Italic.ttf);
            }

            .font-mono {
                font-family: var(--monaco-monospace-font) !important;
            }

            .font-sans {
                font-family: "Titillium Web", ui-sans-serif, system-ui, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji" !important;
            }

            .font-serif {
                font-family: "Bai Jamjuree", ui-serif, Georgia, Cambria, "Times New Roman", Times, serif !important;
            }
            
            .monaco-editor {
                font-family: var(--monaco-monospace-font) !important;
            }
        }
    </style>
"""


def AppBar():
    with ui.row().classes("h-5 mb-2 -mt-1"):
        ui.html(logo)
        ui.markdown("J2Live").classes(
            "text-xl -ml-3 font-serif -mt-1 tracking-widest font-medium"
        )


def TemplatePreview():
    try:
        templatePreviewContent = app.storage.user["templatePreviewContent"]
    except KeyError:
        templatePreviewContent = ""
    try:
        templatePreviewLanguage = app.storage.user["templatePreviewLanguage"]
    except KeyError:
        templatePreviewLanguage = ""

    async def getMonacoEditor(divId):
        await ui.run_javascript(
            f"""
            function loadScript(url, callback) {{
                var script = document.createElement("script");
                script.type = "text/javascript";
                script.src = url;
                script.onload = callback;
                document.body.appendChild(script);
            }}

            loadScript("https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.52.0/min/vs/loader.min.js", function() {{
                require.config({{ paths: {{ 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.52.0/min/vs' }}}});
                require(['vs/editor/editor.main'], function() {{
                
                    async function TemplatePreview() {{
                      const {{ createHighlighter }} = await import('https://esm.sh/shiki@1.22.0')
                      const {{ shikiToMonaco }} = await import('https://esm.sh/@shikijs/monaco@1.22.0')

                      const highlighter = await createHighlighter({{
                        themes: ['nord'],
                        langs: [
                          "c",
                          "dockerfile",
                          "javascript",
                          "pascal",
                          "sql",
                          "c++",
                          "elixir",
                          "julia",
                          "php",
                          "yaml",
                          "c#",
                          "go",
                          "kotlin",
                          "python",
                          "typescript",
                          "clojure",
                          "html",
                          "lua",
                          "ruby",
                          "css",
                          "java",
                          "markdown",
                          "rust",
                        ]  
                      }})                    

                        monaco.languages.register({{ id: "c" }});
                        monaco.languages.register({{ id: "dockerfile" }});
                        monaco.languages.register({{ id: "javascript" }});
                        monaco.languages.register({{ id: "pascal" }});
                        monaco.languages.register({{ id: "sql" }});
                        monaco.languages.register({{ id: "c++" }});
                        monaco.languages.register({{ id: "elixir" }});
                        monaco.languages.register({{ id: "julia" }});
                        monaco.languages.register({{ id: "php" }});
                        monaco.languages.register({{ id: "yaml" }});
                        monaco.languages.register({{ id: "c#" }});
                        monaco.languages.register({{ id: "go" }});
                        monaco.languages.register({{ id: "kotlin" }});
                        monaco.languages.register({{ id: "python" }});
                        monaco.languages.register({{ id: "typescript" }});
                        monaco.languages.register({{ id: "clojure" }});
                        monaco.languages.register({{ id: "html" }});
                        monaco.languages.register({{ id: "lua" }});
                        monaco.languages.register({{ id: "ruby" }});
                        monaco.languages.register({{ id: "css" }});
                        monaco.languages.register({{ id: "java" }});
                        monaco.languages.register({{ id: "markdown" }});
                        monaco.languages.register({{ id: "rust" }});


                        shikiToMonaco(highlighter, monaco)

                        var parentDiv = getElement("{divId}");
                        window.templatePreview = monaco.editor.create(parentDiv, {{
                            value: `{templatePreviewContent}`, 
                            theme: "nord",
                            fontFamily: '{monoFontFamily}',
                            fontSize: 14,
                            readOnly: true,
                            lineNumbers: 'on',        
                            minimap: {{ enabled: true }},
                            glyphMargin: false,    
                            scrollbar: {{                    
                                vertical: 'hidden',
                                horizontal: 'hidden',
                                useShadows: false
                            }},
                            scrollBeyondLastLine: false,
                            renderLineHighlight: 'none',
                            hover: {{enabled: false}},
                            renderLineNumbers: 'off',
                            hideCursorInOverviewRuler: true, 
                            overviewRulerLanes: 0,
                            renderIndentGuides: false,
                            wordWrap: "on" 
                        }});

                        monaco.editor.setModelLanguage(window.templatePreview.getModel(), "{templatePreviewLanguage}");
    
                        var resizeObserver = new ResizeObserver(function(entries) {{
                            window.templatePreview.layout();
                        }});
                        resizeObserver.observe(parentDiv);
    
                        }}
    
                        TemplatePreview()
                }});
            }});
        """
        )

    with ui.row().classes("w-full flex flex-col justify-end"):
        ui.label("Generated Template").classes(
            "text-lg w-full text-end leading-none font-serif"
        )
        with ui.element("span").classes(
            "text-[#d8dee9] -mt-1 mb-1 text-end w-80 self-end"
        ):
            with ui.element("sup").classes("flex text-xs"):
                ui.label(
                    "The generated output below will automatically update when tweaking values on the left-hand side"
                ).classes("italic")

    container = ui.row().classes(f"w-full h-full max-h-[85.5vh] template-preview")

    ui.timer(0, lambda: getMonacoEditor(container.id), once=True)

    return container


async def handleYamlEditorChange(eventArgs: ValueChangeEventArguments):
    app.storage.user["yamlEditorContent"] = await ui.run_javascript(
        "window.yamlEditor.getValue()"
    )
    jinjaContent = app.storage.user["jinja2EditorContent"]
    try:
        renderedOutput, hasErrored = renderTemplate(
            app.storage.user["yamlEditorContent"] or "", jinjaContent
        )
    except Exception as errorMsg:
        renderedOutput = errorMsg

    detectCodeLangResponse = await ui.run_javascript(
        f"""
        const flourite = window.flourite;
        flourite(`{renderedOutput}`);
        """,
    )

    app.storage.user["templatePreviewLanguage"] = detectCodeLangResponse[
        "language"
    ].lower()

    ui.run_javascript(
        f"""
        window.templatePreview.setValue(`{renderedOutput}`)
        monaco.editor.setModelLanguage(window.templatePreview.getModel(), "{app.storage.user["templatePreviewLanguage"]}");
        """
    )

    app.storage.user["templatePreviewContent"] = renderedOutput


def YamlEditor():
    try:
        yamlEditorContent = app.storage.user["yamlEditorContent"]
    except KeyError:
        yamlEditorContent = ""

    async def getMonacoEditor(divId):
        await ui.run_javascript(
            f"""
            function loadScript(url, callback) {{
                var script = document.createElement("script");
                script.type = "text/javascript";
                script.src = url;
                script.onload = callback;
                document.body.appendChild(script);
            }}

            loadScript("https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.52.0/min/vs/loader.min.js", function() {{
                require.config({{ paths: {{ 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.52.0/min/vs' }}}});
                require(['vs/editor/editor.main'], function() {{
                
                    async function yamlEditor() {{
                      const {{ createHighlighter }} = await import('https://esm.sh/shiki@1.22.0')
                      const {{ shikiToMonaco }} = await import('https://esm.sh/@shikijs/monaco@1.22.0')

                      const highlighter = await createHighlighter({{
                        themes: ['nord'],
                        langs: [
                          "yaml",
                        ]  
                      }})                    

                      monaco.languages.register({{ id: "yaml" }});
                      shikiToMonaco(highlighter, monaco)
                      var parentDiv = getElement("{divId}");
                      window.yamlEditor = monaco.editor.create(parentDiv, {{
                          value: `{yamlEditorContent}`,
                          language: "yaml",
                          theme: "nord",
                          fontFamily: '{monoFontFamily}',
                          fontSize: 14,
                          readOnly: false,
                          lineNumbers: 'on',
                          minimap: {{ enabled: true }},
                          glyphMargin: false,    
                          scrollbar: {{                    
                              vertical: 'hidden',
                              horizontal: 'hidden',
                              useShadows: false
                          }},
                          scrollBeyondLastLine: false,
                          renderLineHighlight: 'none',
                          hover: {{enabled: false}},
                          renderLineNumbers: 'off',
                          hideCursorInOverviewRuler: true, 
                          overviewRulerLanes: 0,
                          renderIndentGuides: false,
                          wordWrap: "on" 
                      }});
  
                      var resizeObserver = new ResizeObserver(function(entries) {{
                          window.yamlEditor.layout();
                      }});
                      resizeObserver.observe(parentDiv);
  
                        window.yamlEditor.getModel().onDidChangeContent((event) => {{
                        emitEvent("yamlEditorChange", event)
                      }})
                    }}
  
                    yamlEditor()
                }});
            }});
        """
        )

        ui.on("yamlEditorChange", lambda e: handleYamlEditorChange(e))

    with ui.row().classes("w-full flex flex-col"):
        ui.label("YAML Variables").classes(
            "text-lg leading-none font-serif tracking-wide"
        )
        with ui.element("span").classes("text-[#d8dee9]"):
            with ui.element("sup").classes("flex text-xs"):
                ui.label("e.g.").classes("indent-4 italic")
                ui.space().classes("w-1")
                ui.label("some_var: abc").classes("font-mono bg-[#2e3440] px-1 italic")

    container = ui.row().classes(f"w-full h-full max-h-[88vh] yaml-editor")

    ui.timer(0, lambda: getMonacoEditor(container.id), once=True)


@ui.page(path="/", title="J2Live", favicon=logo.replace("currentColor", "white"))
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

    AppBar()
    rootLayout = ui.element().classes(
        "flex w-full h-[90v] justify-evenly items-stretch antialiased lg:w-screen"
    )

    with rootLayout:
        with ui.element().classes(
            "basis-5/12 h-[40.45vh] flex items-stretch justify-around"
        ):
            yamlEditor = YamlEditor()
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
    storage_secret=config.storageSecret,
    port=native.find_open_port(),
)
