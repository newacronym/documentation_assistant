from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI, OpenAIEmbeddings

import os
from typing import Any, Dict, List
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores.pinecone import Pinecone as PineconeLangChain
from pinecone import Pinecone
from consts import INDEX_NAME

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])


def run_llm(query: str, chat_history: List[Dict[str, Any]] = []) -> Any:
    embeddings = OpenAIEmbeddings()
    docsearch = PineconeLangChain.from_existing_index(
        index_name=INDEX_NAME, embedding=embeddings
    )
    chat = ChatOpenAI(verbose=True, temperature=0)

    qa = ConversationalRetrievalChain.from_llm(
        llm=chat, retriever=docsearch.as_retriever(), return_source_documents=True
    )
    return qa({"question": query, "chat_history": chat_history})


if __name__ == "__main__":
    print(run_llm(query="What is Langchain?"))
