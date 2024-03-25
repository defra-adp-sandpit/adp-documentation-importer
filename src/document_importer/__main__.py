# Project main file
import sys
import argparse
from dotenv import load_dotenv, dotenv_values
import logging
from document_importer.importer import Importer


def main(args: list = sys.argv) -> None:
    """
    Main function that imports documents, loads them into the vector search, and performs a similarity search.
    """
    logging.info("Starting the document importer...")
    logging.info("-----------------Starting Script-----------------")
    # Parse the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--repository', help='The github repository name', required=True)
    parser.add_argument('-d', '--directory', help='The directory of the markdown documents', required=True)
    parser.add_argument('-l', '--loglevel', default='warning',
                        help='Provide logging level. Example --loglevel debug, default=warning')
    args = parser.parse_known_args(args)

    logging.basicConfig(level=args[0].loglevel.upper(), format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # Load the environment variables
    load_dotenv(override=True)
    config = {
        **dotenv_values(),
    }
    print(f"Imported configuration of length: {len(config.keys())}")
    print(f"Args: {args}")
    Importer(config, repository=args[0].repository, directory=args[0].directory).run()

    logging.info("-----------------Script Completed-----------------")


if __name__ == "__main__":
    main()
