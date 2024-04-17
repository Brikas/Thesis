# Prompt builder
def userMsg(*args) -> dict:
    return {"role": "user", "content": "\n".join(args)}
def assistantMsg(*args) -> dict:
    return {"role": "assistant", "content": "\n".join(args)}
def systemMsg(*args) -> dict:
    return {"role": "system", "content": "\n".join(args)}