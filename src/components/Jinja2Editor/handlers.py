from nicegui import app, ui
from _ansible import renderTemplate
from nicegui.events import ValueChangeEventArguments


async def handleJinja2EditorChange(eventArgs: ValueChangeEventArguments):
    app.storage.user["jinja2EditorContent"] = await ui.run_javascript(
        "window.jinja2Editor.getValue()"
    )
    yamlContent = app.storage.user["yamlEditorContent"]
    try:
        renderedOutput, hasErrored = renderTemplate(
            yamlContent, app.storage.user["jinja2EditorContent"]
        )
    except Exception as errorMsg:
        renderedOutput = errorMsg

    app.storage.user["templatePreviewContent"] = renderedOutput

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
