"""Loading logic for loading documents from an s3 directory."""
from typing import List
from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseLoader
from langchain.document_loaders.unstructured import UnstructuredFileLoader
import tempfile
import os


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

