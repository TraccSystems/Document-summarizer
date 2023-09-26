import csv
from requests_html import HTMLSession
from datetime import datetime
import boto3
import os
import glob
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter,RecursiveCharacterTextSplitter
from typing import List
from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseLoader
from langchain.document_loaders.unstructured import UnstructuredFileLoader
import tempfile
from langchain.vectorstores import SingleStoreDB
from langchain.document_loaders import DirectoryLoader,CSVLoader,PyPDFLoader
from langchain.vectorstores import Pinecone
from unstructured.cleaners.core import clean_extra_whitespace
import pinecone



class S3FileLoader_space(BaseLoader):
    """Loading logic for loading documents from s3."""

    def __init__(self, bucket: str, key: str, space_key:str,space_secrete:str):
        """Initialize with bucket and key name."""
        self.bucket = bucket
        self.key = key
        self.space_key = space_key
        self.space_secrete = space_secrete

    def load(self) -> List[Document]:
        """Load documents."""
        try:
            import boto3
        except ImportError:
            raise ImportError(
                "Could not import `boto3` python package. "
                "Please install it with `pip install boto3`."
            )
        s3 = boto3.client("s3",
        region_name='nyc3',
        endpoint_url='https://nyc3.digitaloceanspaces.com',
        aws_access_key_id=self.space_key,
        aws_secret_access_key=self.space_secrete
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = f"{temp_dir}/{self.key}"
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            s3.download_file(self.bucket, self.key, file_path)
            loader = UnstructuredFileLoader(file_path)
            return loader.load()

class S3DirectoryLoader_space(BaseLoader):
    """Loading logic for loading documents from s3."""
    def __init__(self, bucket: str,space_key:str,space_secrete:str, prefix: str = "",):
        """Initialize with bucket and key name."""
        self.bucket = bucket
        self.prefix = prefix
        self.space_key = space_key
        self.space_secrete = space_secrete

    def load(self) -> List[Document]:
        """Load documents."""
        try:
            import boto3
        except ImportError:
            raise ImportError(
                "Could not import boto3 python package. "
                "Please install it with `pip install boto3`."
            )
        s3 = boto3.resource("s3",
         region_name='nyc3',
        endpoint_url='https://nyc3.digitaloceanspaces.com',
        aws_access_key_id=self.space_key,
        aws_secret_access_key=self.space_secrete
        )
        bucket = s3.Bucket(self.bucket)
        docs = []
        for obj in bucket.objects.filter(Prefix=self.prefix):
             loader = S3FileLoader_space(self.bucket, obj.key,self.space_key,self.space_secrete)
             docs.extend(loader.load())
        return docs
    


def load_external_document(space_key=None,space_secret=None,pinecone_api_key=None,pinecone_environment=None,openai_api_key=None,index_name='scrap-data'):

    current_date = datetime.today().strftime("%A-%d-%B-%Y")

    folder_name ='latestArticles' 
    prefix = f"{folder_name}_" + current_date  # to load latest article from s3 with current date
    loader = S3DirectoryLoader_space('scrap-data',space_key,space_secret, prefix=prefix)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    doc = text_splitter.split_documents(documents)
    
    os.environ["OPENAI_API_KEY"] = openai_api_key
    embeddings = OpenAIEmbeddings()
    pinecone.init(
    api_key=pinecone_api_key,  # find at app.pinecone.io
    environment=pinecone_environment,  # next to api key in console
    )
    Pinecone.from_documents(doc,embeddings, index_name=index_name)
    return 


def load_local_document(file_paths:str):
    loader =  CSVLoader(file_path=file_paths, source_column="links")
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)

    return texts




def load_uploaded_documments_to_pinecone(file_path=None,pinecone_api_key=None,pinecone_environment=None,openai_api_key=None,index_name='scrap-data'):
    """
    function to load any documment type to pinecone db
    file type.. text files, powerpoints, html, pdfs, images, and more.

    """

    file_extension = os.path.splitext(file_path)[1]
    
    ## check for file extension
    if file_extension.lower() == ".pdf":
        loader = PyPDFLoader(file_path)
    else:
      loader = UnstructuredFileLoader(file_path,
      mode="elements",
      post_processors=[clean_extra_whitespace],)

    data = loader.load()

    text_splitter = text_splitter = CharacterTextSplitter(
    chunk_size=1000, chunk_overlap=0)

    texts = text_splitter.split_documents(data)

    print(texts)

    os.environ["OPENAI_API_KEY"] = openai_api_key
    embeddings = OpenAIEmbeddings()
    pinecone.init(
    api_key=pinecone_api_key,  # find at app.pinecone.io
    environment=pinecone_environment,  # next to api key in console
    )
    Pinecone.from_documents(texts, embeddings, index_name=index_name)

    return






