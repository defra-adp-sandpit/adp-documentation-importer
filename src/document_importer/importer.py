import os
import logging
from document_importer.vector_search import VectorSearch
from document_importer.markdown_parser import MarkdownParser
from document_importer.document_manager import DocumentManager


class Importer:
    def __init__(self, config: dict, repository: str, directory: str) -> None:
        """
        Initializes an instance of the Importer class.
        Args:
            config (dict): The configuration dictionary.
            repository (str): The repository name.
            directory (str): The directory path.
        """
        # Load the environment variables
        self.config: dict = config
        # Verify the environment variables
        self.__check_environment_variable("AZURE_OPENAI_ENDPOINT")
        self.__check_environment_variable("AZURE_OPENAI_API_KEY")
        self.__check_environment_variable("AZURE_OPENAI_API_VERSION")
        self.__check_environment_variable("AZURE_DEPLOYMENT")
        self.__check_environment_variable("VECTOR_STORE_ADDRESS")
        self.__check_environment_variable("VECTOR_STORE_PASSWORD")
        self.__check_environment_variable("INDEX_NAME")
        # Set the parameters
        self.vector_search = VectorSearch(config)
        self.document_manager = DocumentManager(config)
        self.markdown_parser = MarkdownParser()
        self.directory: str = directory
        self.repository: str = repository
        self.chunk_size: int = 1000
        self.chunk_overlap: int = 0
        self.failed_files: list[str] = []
        self.succeed_files: list[str] = []
        self.total_chunks: int = 0
        self.succeed_cleaning: int = 0
        self.file_paths: list[str] = []

    def run(self) -> None:
        """
        Runs the import process.
        """
        # Get all the markdown files
        logging.info("-----------------Getting Markdown Files-----------------")
        self.file_paths = list(self.__get_all_files(self.directory))
        logging.info(f"Found {len(self.file_paths)} markdown files in directory {self.directory}...")
        logging.info(f"Files: {self.file_paths}")
        logging.info("-----------------Getting Pre-import Statistics-----------------")
        self.pre_import_index_stats = self.document_manager.get_document_store_statistics()
        logging.info("-----------------Starting Importing Files-----------------")
        for file_path in self.file_paths:
            try:
                logging.info(f"Loading document {self.repository}:{file_path}...")
                docs = self.markdown_parser.parse(file_path, repository=self.repository,
                                                  chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
                page_contents = docs.get("page_contents")
                page_metadatas = docs.get("page_metadatas")
                if self.document_manager.clean_document(self.repository, file_path):
                    self.succeed_cleaning += 1
                self.vector_search.load_chunks(page_contents, page_metadatas)
                self.succeed_files.append(file_path)
                self.total_chunks += len(page_contents)
            except Exception as e:
                logging.error(f"Failed to load document {file_path}: {str(e)}")
                self.failed_files.append(file_path)
        logging.info("-----------------Importing files completed-----------------")
        logging.info("-----------------Getting Post-import Statistics-----------------")
        self.post_import_index_stats = self.__report_result(self.pre_import_index_stats)

    def __report_result(self, pre_import_index_stats):
        """
        Reports the import result.
        Args:
            pre_import_index_stats: The pre-import index statistics.
        """
        if len(self.failed_files) > 0:
            print(f"Failed to load {len(self.failed_files)}/{len(self.file_paths)}")
            logging.debug(f"Failed files load a total of {self.failed_files} markdown files.")
        if len(self.succeed_files) > 0:
            print(f"Succeed to load {len(self.succeed_files)}/{len(self.file_paths)} markdown files "
                  + f"with a total of {self.total_chunks} chunks "
                  + f"and successful cleaned up {self.succeed_cleaning} older markdown files (if present).")
            logging.debug(f"Succeed files: {self.succeed_files}")
        self.document_manager.get_document_store_statistics(pre_import_index_stats)

    def __check_environment_variable(self, environment_variable: str) -> None:
        """
        Checks if the specified environment variable is set. Raises a ValueError if it is not set.
        Args:
            environment_variable (str): The name of the environment variable to check.
        Raises:
            ValueError: If the environment variable is not set.
        """
        if not self.config.get(environment_variable):
            raise ValueError(f"Required environment variable {environment_variable} is not set")

    def __get_all_files(self, directory):
        """
        Generator function that yields all the markdown files in the specified directory and its subdirectories.
        Args:
            directory: The directory to search for markdown files.
        Yields:
            The file paths of the markdown files.
        """
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                if os.path.splitext(filename)[1] == '.md':
                    yield os.path.join(dirpath, filename)
