from ast import Dict
from dotenv import load_dotenv, dotenv_values
import pytest
import sys
from src.document_importer.importer import Importer


def test_importer():
    load_dotenv(override=True)
    config = {
        **dotenv_values(),
    }
    importer = Importer(config, repository="adp/example1", directory="example_docs/example_1")
    importer.run()
    assert len(importer.succeed_files) == 1
    assert len(importer.failed_files) == 2