from ast import Dict
import pytest
import sys
from src.document_importer.document_manager import DocumentManager


def test_document_manager():
    config: Dict = {
        "VECTOR_STORE_ADDRESS": "https://vectorstore",
        "VECTOR_STORE_PASSWORD": "password",
        "INDEX_NAME": "indexname"
    }
    document_manager = DocumentManager(config=config)
    assert document_manager is not None

def test_empty_dm():
    assert 1 == 1