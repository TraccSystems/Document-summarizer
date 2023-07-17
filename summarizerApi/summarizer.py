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
    return vectorstore_search

def get_summarizer_question_query(message,question_answer):
    response = question_answer.similarity_search(message)
    return response[0].page_content





question_answer  = get_similarity_search(openai_api_key='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')

answer = get_summarizer_question_query('what did Tribunal do ?',question_answer)

print(answer)