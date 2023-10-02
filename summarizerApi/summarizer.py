from pprint import pprint
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.vectorstores import Pinecone,SingleStoreDB,ElasticKnnSearch,ElasticsearchStore

import pinecone
import os

from langchain.embeddings.openai import OpenAIEmbeddings

def get_similarity_search_singlestore(openai_api_key=None,host=None,password=None,user="admin",db=None):
    os.environ["SINGLESTOREDB_URL"] = f"{user}:{password}@{host}:3306/{db}"
    docsearch = SingleStoreDB(OpenAIEmbeddings(openai_api_key=openai_api_key),table_name='scrap_doc')

    return docsearch

def get_summarizer_question_query_singlestore(message,question_answer):
    response = question_answer.similarity_search(message)
    return response[0].page_content

def get_similarity_search(openai_api_key=None,temperature=0.0):
    
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

    pinecone.init(api_key='788fc40b-a4bd-40b6-b4c5-6d02ae274428', environment='us-west4-gcp-free')
    # Creating a Vector Store and Querying
    text_key = "text"
    index = pinecone.Index('scrap-data')
    vectorstore_search = Pinecone(index,embeddings.embed_query, text_key)
    return vectorstore_search


def get_summarizer_question_query(message,question_answer):
    response = question_answer.similarity_search(message,k=1)
    return response


def get_elasticsearch_summary_query(openai_api_key=None,temperature=0.0,index_name=None,es_cloud_id=None,es_user="elastic",es_password=None,es_api_key=None):
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    elastic_vector_search = ElasticsearchStore(
            index_name=index_name,
            embedding=embeddings,
            es_cloud_id=es_cloud_id,
            es_user=es_user,
            es_password=es_password,
            es_api_key=es_api_key,
            strategy=ElasticsearchStore.ExactRetrievalStrategy()
           
        )
    #elastic_vector_search.client.indices.refresh(index=index_name)

    return elastic_vector_search






#qa = get_similarity_search_singlestore(openai_api_key='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',
                           #host='svc-39f86d53-e0bf-4708-9e17-18faf0dfe22c-dml.aws-virginia-6.svc.singlestore.com',
                           #password='84563320Owo',db='scrap_db'
                           #)
#answer = get_summarizer_question_query_singlestore('tell me who celebrate 50 years',qa)
#print(answer)


#question_answer  = get_similarity_search(openai_api_key='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')

#answer = get_summarizer_question_query('tell me about  President Urges Action',question_answer)
