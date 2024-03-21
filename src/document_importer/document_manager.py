from ast import Dict, List
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient, SearchItemPaged
from azure.search.documents.indexes import SearchIndexClient
import logging

class DocumentManager:
    """
    A class that manages documents and provides methods for retrieving and cleaning them.
    """

    def __init__(self, config):
        """
        Initializes a new instance of the DocumentManager class.

        Args:
            config: A dictionary containing configuration settings.
        """
        self.service_endpoint = config.get("VECTOR_STORE_ADDRESS")
        self.index_name = config.get("INDEX_NAME")
        key = config.get("VECTOR_STORE_PASSWORD")
        credential = AzureKeyCredential(key)
        self.search_client = SearchClient(self.service_endpoint, self.index_name, credential)
        self.index_client = SearchIndexClient(self.service_endpoint, credential)

    def get_full_document(self, repository:str, source:str) -> SearchItemPaged[Dict]:    
        """
        Retrieves the full document based on the repository and source.

        Args:
            repository: A string representing the repository.
            source: A string representing the source.

        Returns:
            The full document matching the repository and source.
        """
        filter = f"repository eq '{repository}' and source eq '{source}'"
        return self.search_client.search(search_text="*", filter=filter, top=1000)
    
    def clean_document(self, repository:str, source:str) -> int:
        """
        Cleans the documents for the specified repository and source.

        Args:
            repository: A string representing the repository.
            source: A string representing the source.

        Returns:
            True if the documents were cleaned successfully, False otherwise.
        """
        logging.info(f"Cleaning documents for {repository}:{source}...")
        # Getting documents from index
        chunks = self.get_full_document(repository, source)   
        data_list:List[Dict]=[]
        [data_list.append(chunk) for chunk in chunks]        
        if len(data_list) == 0:
            logging.info(f"No documents found for {repository}: {source}")
            return True
        # Deleting documents from index
        results = self.search_client.delete_documents(data_list)
        return self.__report_clean(repository, source, data_list, results)

    def get_document_store_statistics(self, oldStats:Dict = None) -> Dict:
        """
        Retrieves the statistics for the document store.

        Returns:
            A dictionary containing the statistics for the document store.
        """
        logging.info(f"Getting statistics for index {self.index_name}...")
        result:Dict = self.index_client.get_index_statistics(self.index_name)
        log:str = f"Statistics for index {self.index_name} retrieved: {result}"
        if oldStats!=None:
            log += f" old stats: {oldStats}"
        logging.info(log)
        return result
    def __report_clean(self, repository, source, data_list, results):
        """
        Reports the cleaning results for the specified repository and source.

        Args:
            repository: A string representing the repository.
            source: A string representing the source.
            data_list: A list of dictionaries representing the data to be cleaned.
            results: A list of cleaning results.

        Returns:
            True if all documents were deleted successfully, False otherwise.
        """
        failed_to_delete:int = 0
        succeeded_to_delete:int = 0
        for result in results:
            if result.succeeded == False:
                failed_to_delete += 1
            else:
                succeeded_to_delete += 1   
        if failed_to_delete > 0:
            logging.warning(f"Failed to delete {failed_to_delete}/{len(data_list)} for {repository}:{source}")
        logging.info(f"Succeeded to delete {succeeded_to_delete}/{len(data_list)} in {repository}:{source}")
        return failed_to_delete == 0

    def delete_vector_index(self, index: str):
        self.index_client.delete_index(index)        
