# # Project main file
import os
from icecream import ic
from dotenv import load_dotenv, dotenv_values
import logging
from document_importer.vector_search import VectorSearch
from document_importer.markdown_parser import MarkdownParser
from document_importer.document_manager import DocumentManager
from document_importer.importer import Importer

def main() -> None:
    """
    Main function that imports documents, loads them into the vector search, and performs a similarity search.
    """
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    logging.info("Starting the document importer...")
    logging.info("-----------------Starting Script-----------------")
    # Load the environment variables
    load_dotenv(override=True)
    config = {
        **dotenv_values(),
    }
    logging.info(f"Imported configuration of length: {len(config.keys())}")
    Importer(config, repository="defra/example", directory="docs").run()

    logging.info("-----------------Script Completed-----------------")

    # # Check the environment variables
    # check_environment_variable("AZURE_OPENAI_ENDPOINT")
    # check_environment_variable("AZURE_OPENAI_API_KEY")
    # check_environment_variable("AZURE_OPENAI_API_VERSION")
    # check_environment_variable("AZURE_DEPLOYMENT")
    # check_environment_variable("VECTOR_STORE_ADDRESS")
    # check_environment_variable("VECTOR_STORE_PASSWORD")
    # check_environment_variable("INDEX_NAME")

    # # Set the parameters
    # directory = "docs"
    # repository = "defra/example"
    # chunk_size = 1000
    # chunk_overlap = 0

    # # Get all the markdown files
    # file_paths = list(get_all_files(directory))
    # logging.info(f"Found {len(file_paths)} markdown files in directory {directory}...")
    # logging.info(f"Files: {file_paths}")
    
    # vector_search:VectorSearch = VectorSearch(config)
    # document_manager:DocumentManager = DocumentManager(config)
    # markdown_parser:MarkdownParser = MarkdownParser()
    # failed_files:list[str] = []
    # succeed_files:list[str] = []
    # total_chunks:int = 0
    # succeed_cleaning:int = 0
    # #Load the documents
    # pre_import_index_stats = document_manager.get_document_store_statistics()
    # for file_path in file_paths:
    #     try:
    #         logging.info(f"Loading document {repository}:{file_path}...")
    #         docs = markdown_parser.parse(file_path, repository=repository, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    #         page_contents = docs.get("page_contents")
    #         page_metadatas = docs.get("page_metadatas")
    #         if document_manager.clean_document(repository, file_path): succeed_cleaning += 1
    #         vector_search.load_chunks(page_contents, page_metadatas)       
    #         succeed_files.append(file_path)
    #         total_chunks += len(page_contents)
    #     except Exception as e:
    #         logging.error(f"Failed to load document {file_path}: {str(e)}")
    #         failed_files.append(file_path)

    # if len(failed_files) > 0:
    #     logging.warning(f"Failed to load {len(failed_files)}/{len(file_paths)}")
    #     logging.debug(f"Failed files: {failed_files}")
    # if len(succeed_files) > 0:
    #     logging.info(f"Succeed to load {len(succeed_files)}/{len(file_paths)} with {total_chunks} chunks and successful cleaning {succeed_cleaning}.")
    #     logging.debug(f"Succeed files: {succeed_files}")
    # document_manager.get_document_store_statistics(pre_import_index_stats)
    # logging.info("Documents loaded")
    # # Perform a similarity search
    #logging.info("Performing similarity search...")
    # docs = vector_search.search(
    #     query="", search_type="hybrid", k=40, filters="repository eq 'defra/example' and source eq 'docs\index.md'"
    # )
    
    # logging.info(f"Found {len(docs)} similar documents")


def check_environment_variable(environment_variable: str) -> None:
    """
    Checks if the specified environment variable is set. Raises a ValueError if it is not set.
    Args:
        environment_variable: The name of the environment variable to check.
    """
    if not os.getenv(environment_variable):
        raise ValueError(f"Required environment variable {environment_variable} is not set")
    

def get_all_files(directory):
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
    

if __name__ == "__main__":
    main()


