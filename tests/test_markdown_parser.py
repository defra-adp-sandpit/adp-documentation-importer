from ast import Dict
from dotenv import load_dotenv, dotenv_values
import pytest

from src.document_importer.markdown_parser import MarkdownParser

def test_markdown_parser_convert_markdown_file_into_chucks_correctly() -> None:
    """
    Test case for the MarkdownParser class.

    This test case verifies the behavior of the `parse` method of the MarkdownParser class.
    It checks if the method correctly parses a Markdown file and returns the expected chunks.

    The test performs the following steps:
    1. Arrange the necessary objects and variables.
    2. Act by calling the `parse` method with the specified path and repository.
    3. Assert the correctness of the returned chunks.

    The test asserts the following conditions:
    - The returned chunks should not be None.
    - The number of chunks should be 2.
    - The "page_contents" key should be present in the chunks.
    - The contents of each chunk should not be blank or empty.
    - The number of contents should be 9.
    - The "page_metadatas" key should be present in the chunks.
    - The number of metadatas should be 9.
    - Each metadata should have the expected keys and values.

    """
    # Arrange
    mdp: MarkdownParser = MarkdownParser()
    repository: str = "adp/example1"
    path: str = "example_docs/example_1/index.md"

    # Act
    chunks: dict = mdp.parse(path=path, repository=repository)

    # Assert
    assert chunks is not None
    assert len(chunks) == 2
    assert "page_contents" in chunks
    contents = chunks.get("page_contents")
    for content in contents:
        assert content.strip(), "Content should not be blank or empty"
    assert len(contents) == 9
    assert "page_metadatas" in chunks
    metadatas = chunks.get("page_metadatas")
    assert len(metadatas) == 9
    # Check the metadata
    chuck_number = 0
    for metadata in metadatas:
        chuck_number += 1
        assert "title" in metadata
        assert metadata.get("title") == "Why ADP"
        assert "summary" in metadata
        assert metadata.get("summary") == "Explainations of what ADP is and the pros and cons of using it."
        assert "authors" in metadata
        assert "uri" in metadata
        assert metadata.get("uri") == "https://defra.github.io/adp-documentation/"
        assert "repository" in metadata
        assert metadata.get("repository") == repository
        assert "path" in metadata
        assert metadata.get("path") == path
        assert "heading" in metadata
        assert "chunk_number" in metadata
        assert metadata.get("chunk_number") == chuck_number

@pytest.mark.parametrize("key", [
    ("title"),
    ("summary"),
    ("authors"),
    ("uri"),
])
def test_throw_exception_when_frontmatter_keys_are_not_present(key: str) -> None:
    """
    Test case to verify that an exception is thrown when frontmatter keys are not present.
    
    Args:
        key (str): The key to be removed from the frontmatter.
    
    Raises:
        ValueError: If no uri is found in the frontmatter of the markdown document.
    """
    
    # Arrange
    mdp: MarkdownParser = MarkdownParser()
    path: str = f"example_docs/bad_example_1/index_no_{key}.md"
    
    # Act and Assert
    with pytest.raises(ValueError) as exc_info:
        mdp.parse(path=path, repository="adp/example1", chunk_size=0, chunk_overlap=0)
        assert str(exc_info.value) == f"No uri found in the frontmatter of the markdown document at {path}"

@pytest.mark.parametrize("key", [
    ("title"),
    ("summary"),
    ("authors"),
    ("uri"),
])
def test_throw_exception_when_frontmatter_keys_are_not_blank_present(key: str) -> None:
    """
    Test case to verify that an exception is thrown when frontmatter keys are not present.
    
    Args:
        key (str): The key to be removed from the frontmatter.
    
    Raises:
        ValueError: If no uri is found in the frontmatter of the markdown document.
    """
    
    # Arrange
    mdp: MarkdownParser = MarkdownParser()
    path: str = f"example_docs/bad_example_1/index_blank_{key}.md"
    
    # Act and Assert
    with pytest.raises(ValueError) as exc_info:
        mdp.parse(path=path, repository="adp/example1", chunk_size=0, chunk_overlap=0)
        assert str(exc_info.value) == f"No uri found in the frontmatter of the markdown document at {path}"
        
def test_throw_exception_when_frontmatter_are_not_present() -> None:
    """
    Test case to verify that an exception is thrown when frontmatter is not present in the markdown document.
    """
    # Arrange
    mdp: MarkdownParser = MarkdownParser()
    path: str = f"example_docs/bad_example_1/index_no_front_matter.md"
    
    # Act and Assert
    with pytest.raises(ValueError) as exc_info:
        mdp.parse(path=path, repository="adp/example1", chunk_size=0, chunk_overlap=0)
        assert str(exc_info.value) == f"No frontmatter found in the markdown document at {path}"



    
