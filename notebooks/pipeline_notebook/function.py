from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Paths are resolved relative to this file, so the project can be moved or cloned anywhere.
# This file lives in <project>/notebooks/pipeline_notebook/
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

CHROMA_PATH = str(PROJECT_ROOT / "notebooks" / "chroma_db_langchain")  # separate folder from notebook 01's chroma_db/
COLLECTION_NAME = "ml_book_langchain"

EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4.1-nano"

PROMPT_TEMPLATE = """
Your task is to explain the concept of {concept} to me in a way that is:

1. Clear and intuitive
2. Concise (in under 100 words)
3. Tailored specifically to me and what I already know

Base your explanation on the following excerpts from the reference book.
If the excerpts do not cover the concept, say so instead of making something up.

Excerpts:
{context}

Use the following information about me to personalize your explanations:

- Background: Aspiring Data Scientist in the Automotive Industry
- Professional Interests: Extracting structured information from engineering documents, data pipelines
- Personal Interests: Automotive technology, AI applications in engineering

The personalization should be subtle and natural. Avoid forced references to my background that don't genuinely enhance my understanding of the concept.
"""


def vcs(EMBEDDING_MODEL=EMBEDDING_MODEL, COLLECTION_NAME=COLLECTION_NAME, CHROMA_PATH=CHROMA_PATH):
    """Open the persisted Chroma vector store."""
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    vectorstore = Chroma(
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_PATH,
    )
    return vectorstore


def utils(k, vectorstore, CHAT_MODEL=CHAT_MODEL):
    """Build the retriever, prompt template and LLM used by the RAG chain."""
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    llm = ChatOpenAI(model=CHAT_MODEL, temperature=0)
    return retriever, prompt_template, llm


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def build_chain(retriever, prompt_template, llm):
    """Retrieved chunks fill {context}; the user's question fills {concept}."""
    return (
        {"context": retriever | format_docs, "concept": RunnablePassthrough()}
        | prompt_template
        | llm
        | StrOutputParser()
    )


def generate_explanation(concept, retriever, prompt_template, llm):
    chain = build_chain(retriever, prompt_template, llm)
    return chain.invoke(concept)
