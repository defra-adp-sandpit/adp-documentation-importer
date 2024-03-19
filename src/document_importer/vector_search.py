
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import AzureOpenAIEmbeddings, OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from icecream import ic
from azure.search.documents.indexes.models import (
    FreshnessScoringFunction,
    FreshnessScoringParameters,
    ScoringProfile,
    SearchableField,
    SearchField,
    SearchFieldDataType,
    SimpleField,
    TextWeights,
)
import logging


class VectorSearch:
    """
    A class for performing vector-based search using Azure OpenAI and Azure Search.
    """

    def __init__(self, config: dict = {}):
        """
        Initializes the VectorSearch object.

        Args:
            config (dict): A dictionary containing configuration parameters for Azure OpenAI and Azure Search.
        """
        # Azure OpenAI
        azure_endpoint: str = config.get("AZURE_OPENAI_ENDPOINT")
        azure_openai_api_key: str = config.get("AZURE_OPENAI_API_KEY")
        azure_openai_api_version: str = config.get("AZURE_OPENAI_API_VERSION")
        azure_deployment: str = config.get("AZURE_DEPLOYMENT")

        # Azure Search
        vector_store_address: str = config.get("VECTOR_STORE_ADDRESS")
        vector_store_password: str = config.get("VECTOR_STORE_PASSWORD")
        index_name: str = config.get("INDEX_NAME")

        # Initialize the Azure OpenAI Embeddings
        self.embeddings: AzureOpenAIEmbeddings = AzureOpenAIEmbeddings(
            azure_deployment=azure_deployment,
            openai_api_version=azure_openai_api_version,
            azure_endpoint=azure_endpoint,
            api_key=azure_openai_api_key,
        )
        logging.info(f"Embeddings initialized : {azure_deployment} (endpoint), {azure_deployment} (deployment)")      

        # Initialize the Azure Search Vector Store
        self.vector_store: AzureSearch = AzureSearch(
            azure_search_endpoint=vector_store_address,
            azure_search_key=vector_store_password,
            index_name=index_name,
            embedding_function=self.embeddings.embed_query,
            fields=self.__index_fields()
        )
        logging.info(f"Vector store initialized: {vector_store_address} (endpoint), {index_name} (index)")

    def search(self, query: str, k: int = 3, search_type: str = "similarity", filters: str = None):
        """
        Performs a vector-based search.

        Args:
            query (str): The search query.
            k (int): The number of results to retrieve (default: 3).
            search_type (str): The type of search to perform (default: "similarity").
            filters (str): The filters to apply to the search (default: None).

        Returns:
            list: A list of search results.
        """
        return self.vector_store.similarity_search(query=query, k=k, search_type=search_type, filters=filters)
    
    
    def load_documents(self, path: str, encoding: str = "utf-8", chunk_size: int = 1000, chunk_overlap: int = 0):
        """
        Loads documents from a file and adds them to the vector store.

        Args:
            path (str): The path to the file containing the documents.
            encoding (str): The encoding of the file (default: "utf-8").
            chunk_size (int): The size of each document chunk (default: 1000).
            chunk_overlap (int): The overlap between document chunks (default: 0).
        """
        print("Loading documents: {path}")
        loader = TextLoader(path, encoding=encoding)

        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        docs = text_splitter.split_documents(documents)

        self.vector_store.add_documents(documents=docs)

    def load_chunks(self, page_contents: list, page_metadatas: list):
        """
        Loads chunks of text and their corresponding metadata to the vector store.

        Args:
            page_contents (list): A list of text chunks.
            page_metadatas (list): A list of metadata corresponding to the text chunks.
        """
        self.vector_store.add_texts(page_contents, page_metadatas)

    
    def __index_fields(self):
        """
        Indexes the fields of the documents.

        Returns:
            list: A list of fields to index.
        """
        fields = [
            SimpleField(
                name="id",
                type=SearchFieldDataType.String,
                key=True,
                filterable=True,
            ),
            SearchableField(
                name="content",
                type=SearchFieldDataType.String,
                searchable=True,
            ),
            SearchField(
                name="content_vector",
                type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                searchable=True,
                vector_search_dimensions=len(self.embeddings.embed_query("Text")),
                vector_search_profile_name="myHnswProfile",
            ),
            SearchableField(
                name="metadata",
                type=SearchFieldDataType.String,
                searchable=True,
            ),
            # Additional field to store the title
            SearchableField(
                name="title",
                type=SearchFieldDataType.String,
                searchable=True,
            ),
            # Additional field for filtering on document source
            SimpleField(
                name="source",
                type=SearchFieldDataType.String,
                filterable=True,
            ),
            # Additional data field for last doc update
            SimpleField(
                name="last_update",
                type=SearchFieldDataType.DateTimeOffset,
                searchable=True,
                filterable=True,
            ),
            # Additional data field for last doc update
            SimpleField(
                name="uri",
                type=SearchFieldDataType.String,
                searchable=True,
                filterable=True,
            ),
            SimpleField(
                name="repository",
                type=SearchFieldDataType.String,
                searchable=True,
                filterable=True,
            ),
            SimpleField(
                name="summary",
                type=SearchFieldDataType.String,
                searchable=True,
            ),
        ]
        return fields