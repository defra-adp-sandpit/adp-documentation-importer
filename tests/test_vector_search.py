import pytest
# from  src.document_importer.vector_search import VectorSearch
# from dotenv import load_dotenv, dotenv_values

# def test_vector_search():
#     load_dotenv(override=True)
#     config = {
#         **dotenv_values(),
#     }
#     vector_search = VectorSearch(config=config)
#     assert vector_search is not None

def test_empty_slap():
    assert 1 == 1