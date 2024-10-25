from nicegui import app, ui
from config import monoFontFamily


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

    container = ui.row().classes(f"w-full h-full max-h-[84.5vh] template-preview")

    ui.timer(0, lambda: getMonacoEditor(container.id), once=True)

    return container
