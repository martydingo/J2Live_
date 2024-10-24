from nicegui import app, ui
from _ansible import renderTemplate
from nicegui.events import ValueChangeEventArguments


async def handleYamlEditorChange(eventArgs: ValueChangeEventArguments):
    app.storage.user["yamlEditorContent"] = await ui.run_javascript(
        "window.yamlEditor.getValue()"
    )
    jinjaContent = app.storage.user["jinjaEditorContent"]
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
