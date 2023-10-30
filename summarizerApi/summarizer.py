from pprint import pprint
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Pinecone,SingleStoreDB,ElasticKnnSearch,ElasticsearchStore
from langchain.schema import BaseOutputParser

from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)



import pinecone
import os

from langchain.embeddings.openai import OpenAIEmbeddings

def get_similarity_search_singlestore(openai_api_key=None,host=None,password=None,user="admin",db=None):
    os.environ["SINGLESTOREDB_URL"] = f"{user}:{password}@{host}:3306/{db}"
    docsearch = SingleStoreDB(OpenAIEmbeddings(openai_api_key=openai_api_key),table_name='scrap_doc')

    return docsearch


def get_similarity_search_pinecone(openai_api_key=None,temperature=0.0):
    
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

    pinecone.init(api_key='788fc40b-a4bd-40b6-b4c5-6d02ae274428', environment='us-west4-gcp-free')
    # Creating a Vector Store and Querying
    text_key = "text"
    index = pinecone.Index('scrap-data')
    vectorstore_search = Pinecone(index,embeddings.embed_query, text_key)
    return vectorstore_search





def get_elasticsearch_similarity_search(openai_api_key=None,temperature=0.0,index_name=None,es_cloud_id=None,es_user="elastic",es_password=None,es_api_key=None):
    elastic_vector_search = ElasticsearchStore(
            index_name=index_name,
            embedding=OpenAIEmbeddings(openai_api_key=openai_api_key),
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

def get_summarizer_question_query(query,document_question_query,openai_api_key):
    query_response = document_question_query.similarity_search(query,k=3)
    chat_model = ChatOpenAI(openai_api_key=openai_api_key)

    #print(query_response)
    metadata_source = [query_responses.metadata['source'] for query_responses in query_response]
    messages = [
    SystemMessage(content="You are a helpful assistant."),
    AIMessage(content="I'm great thank you. How can I help you?"), 
    ]
    source_knowledge = "\n".join([query_responses.page_content for query_responses in query_response])
    augmented_prompt = f"""Use the following pieces of context to answer the question at the end. 
    If you don't know the answer, just say that you don't know, don't try to make up an answer. 
    Use three sentences maximum and keep the answer as concise as possible. 
    Always say "thanks for asking!" at the end of the answer. .
    Contexts:
    {source_knowledge}
    Query: {query}"""

    prompt = HumanMessage(content=augmented_prompt)

    messages.append(prompt)

    response_query = chat_model(messages)

    
    return (response_query.content,metadata_source)

#question_answer  = get_elasticsearch_similarity_search(openai_api_key='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',
                                                      #index_name="owolabidevelop84@gmail.com_index_name",
                                                      # es_cloud_id="tracc:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyRmN2E5NjFiYTUzZDU0NzAyYjBkNmRiZDE3MWJiYTYwZSQyZjIxNDI0Nzg1ZjI0YWViYWE4M2QxMWU4MzhkZGZhYg==",
                                                       #es_password='6VXYyRVExbNPq15x9RdEXFQP',
                                                      # es_api_key="RGVJaWdJc0JGazl3TXAtR05TWUk6cE1yMlRWN1JTZ2FrdFk2aWtfbEpKQQ=="
                                                      #)

#answer = get_summarizer_question_query('who admonishes africa leader',question_answer,openai_api_key='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')















    
