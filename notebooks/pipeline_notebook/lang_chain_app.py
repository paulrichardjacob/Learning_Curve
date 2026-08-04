from flask import Flask, request
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from function import vcs, utils, generate_explanation


CHROMA_PATH = r"E:\Imarticus_ Learning\Jobs - 2026\Models\notebooks\chroma_db_langchain"  # separate folder from notebook 01's chroma_db/
COLLECTION_NAME = "ml_book_langchain"

EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4.1-nano"

vdb = vcs(EMBEDDING_MODEL=EMBEDDING_MODEL,COLLECTION_NAME=COLLECTION_NAME, CHROMA_PATH=CHROMA_PATH)

app = Flask(__name__)

@app.route('/chatbot')
def chatbot():
    concept = request.form['question']
    retriever , prompt_template, llm = utils(k = 5, vectorstore = vdb, CHAT_MODEL = CHAT_MODEL)
    ans = generate_explanation(concept= concept, retriever= retriever, prompt_template= prompt_template, llm = llm)
    
    return ans

app.run()
    