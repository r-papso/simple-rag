from model import Document


def get_content(document: Document) -> str:
    if (document.path and document.content) or (not document.path and not document.content):
        raise ValueError("Exactly one field from (path, content) has to be provided.")

    if document.path:
        with open(document.path) as f:
            content = f.read()
    else:
        content = document.content

    return content
