from pprint import pprint
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.vectorstores import Pinecone
import pinecone
import os

from langchain.embeddings.openai import OpenAIEmbeddings

def get_similarity_search(openai_api_key=None,temperature=0.0):
    
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

    pinecone.init(api_key='ce38df20-6e16-47cd-928a-9a8471b28edd', environment='us-west1-gcp-free')
    # Creating a Vector Store and Querying
    text_key = "text"
    index = pinecone.Index('articles-doc')
    vectorstore_search = Pinecone(index,embeddings.embed_query, text_key)

    llm = ChatOpenAI(
    openai_api_key=openai_api_key,
    temperature=temperature)

    qa_with_sources = RetrievalQAWithSourcesChain.from_chain_type( 
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore_search.as_retriever())

    return qa_with_sources

def get_summarizer_question_query(message,question_answer):
    response = question_answer(message)
    return response
