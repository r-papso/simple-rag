import logging

import uvicorn
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

from config import Config
from model import Document
from rag import index_document, rag
from utils import get_content

app = FastAPI()
app.add_middleware(HTTPSRedirectMiddleware)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/documents/")
async def add_document(document: Document):
    try:
        content = get_content(document)
    except Exception as e:
        logging.error(e, exc_info=True)
        raise HTTPException(status_code=400, detail=repr(e))

    try:
        await index_document(content)
        return Response()
    except Exception as e:
        logging.error(e, exc_info=True)
        raise HTTPException(status_code=400, detail=repr(e))


@app.get("/documents/")
async def get_answer(question: str):
    try:
        answer = await rag(question)
        return {"answer": answer}
    except Exception as e:
        logging.error(e, exc_info=True)
        raise HTTPException(status_code=400, detail=repr(e))


if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        port=8432,
        reload=True,
        ssl_certfile=Config.config()["certfile"],
        ssl_keyfile=Config.config()["keyfile"],
    )
