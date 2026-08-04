from dotenv import load_dotenv
load_dotenv(r"E:\Imarticus_ Learning\Jobs - 2026\Models\.env")

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

CHROMA_PATH = r"E:\Imarticus_ Learning\Jobs - 2026\Models\notebooks\chroma_db_langchain"  # separate folder from notebook 01's chroma_db/
COLLECTION_NAME = "ml_book_langchain"

EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4.1-nano"

def vcs(EMBEDDING_MODEL, COLLECTION_NAME, CHROMA_PATH):
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    vectorstore = Chroma(
    embedding_function=embeddings,
    collection_name=COLLECTION_NAME,
    persist_directory=CHROMA_PATH,)
    return vectorstore
 
def utils(k,vectorstore, CHAT_MODEL ):
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    prompt_template_str = """
    Your task is to explain the concept of {concept} to me in a way that is:

    1. Clear and intuitive
    2. Concise (in under 100 words)
    3. Tailored specifically to me and what I already know

     Use the following information about me to personalize your explanations:

    - Background: Aspiring Data Scientist in the Automotive Industry
    - Professional Interests: Extracting structured information from engineering documents, data pipelines
    - Personal Interests: Automotive technology, AI applications in engineering

     The personalization should be subtle and natural. Avoid forced references to my background that don't genuinely enhance my understanding of the concept.
    """
  
  # Create a prompt template
    prompt_template = ChatPromptTemplate.from_template(prompt_template_str)

    # Create a model interface
    llm = ChatOpenAI(model=CHAT_MODEL, temperature=0)
    
    return retriever, prompt_template, llm

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def generate_explanation(concept, retriever, prompt_template, llm):
    chain = (
    {"context": retriever | format_docs, "concept": RunnablePassthrough()}
    | prompt_template
    | llm
    | StrOutputParser())
    answer = chain.invoke(concept)
    return answer