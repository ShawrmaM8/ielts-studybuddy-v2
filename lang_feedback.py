from language_tool_python import LanguageTool

def get_language_feedback(text):
    try:
        tool = LanguageTool('en-US')  # Local
    except:
        tool = LanguageTool('en-US', remote=True)  # Fallback
    matches = tool.check(text)
    return [{'rule': m.ruleId, 'message': m.message, 'context': m.context} for m in matches]