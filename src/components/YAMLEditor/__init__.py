from nicegui import ui, app
from config import monoFontFamily
from .handlers import handleYamlEditorChange


def YAMLEditor():
    async def getMonacoEditor(divId):
        try:
            yamlEditorContent = app.storage.user["yamlEditorContent"]
        except KeyError:
            yamlEditorContent = ""
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
