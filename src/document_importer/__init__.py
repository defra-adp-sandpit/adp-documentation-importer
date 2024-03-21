# # Project main file
import os
from icecream import ic
from dotenv import load_dotenv, dotenv_values
import logging
from importer import Importer

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

if __name__ == "__main__":
    main()