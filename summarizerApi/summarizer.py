from langchain.vectorstores import SingleStoreDB
from langchain.chains import LLMChain

import os
from langchain.embeddings.openai import OpenAIEmbeddings

def get_similarity_search(openai_api_key=None,host=None,password=None,user="admin",db=None):
    os.environ["SINGLESTOREDB_URL"] = f"{user}:{password}@{host}:3306/{db}"
    docsearch = SingleStoreDB(OpenAIEmbeddings(openai_api_key=openai_api_key),table_name='scrap_doc')
    return docsearch

def get_summarizer_question_query(message,question_answer):
    response = question_answer.similarity_search(message)
    return response['answer']










