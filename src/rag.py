import os
from typing import Iterable

from langchain import hub
from langchain.schema.document import Document
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import Config

os.environ["OPENAI_API_KEY"] = Config.config()["open_ai_key"]

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
prompt: ChatPromptTemplate = hub.pull("rlm/rag-prompt")
llm = ChatOpenAI(model=Config.config()["chat_model"])

vectorstore = Chroma(
    persist_directory=Config.config()["persist_directory"],
    embedding_function=OpenAIEmbeddings(model=Config.config()["embedding_model"]),
)


async def index_document(document: str) -> None:
    splits = [Document(page_content=x) for x in text_splitter.split_text(document)]
    _ = await vectorstore.aadd_documents(splits)


async def rag(question: str) -> str:
    retriever = vectorstore.as_retriever()

    rag_chain = (
        {"context": retriever | _format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return await rag_chain.ainvoke(question)


def _format_docs(docs: Iterable[Document]):
    return "\n\n".join(doc.page_content for doc in docs)
