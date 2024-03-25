import frontmatter
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from datetime import datetime
from frontmatter import Post


class MarkdownParser:
    """
    A class that parses markdown documents and splits them into chunks.

    Args:
        None

    Attributes:
        None

    Methods:
        parse: Parses a markdown document and splits it into chunks.
    """

    def __init__(self):
        pass

    def parse(self, path: str, encoding: str = "utf-8",
              chunk_size: int = 1000, chunk_overlap: int = 0, repository: str = "") -> dict:
        """
        Parses a markdown document and splits it into chunks.

        Args:
            path (str): The path to the markdown document.
            encoding (str, optional): The encoding of the markdown document. Defaults to "utf-8".
            chunk_size (int, optional): The size of each chunk. Defaults to 1000.
            chunk_overlap (int, optional): The overlap between chunks. Defaults to 0.
            repository (str, optional): The repository name. Defaults to None.

        Returns:
            dict: A dictionary containing the metadata and contents of the parsed chunks.
        """
        # Load the documents
        markdown_document = self.__load_markdown_document(path)

        # MD splits
        splits = self.__spilt_markdown_document(chunk_size, chunk_overlap, markdown_document)

        return self.__format_chunks(splits, metadata=markdown_document, repository=repository, path=path)

    def __spilt_markdown_document(self, chunk_size, chunk_overlap, markdown_document) -> list:
        """
        Splits a markdown document into chunks based on header levels.

        Args:
            chunk_size (int): The size of each chunk.
            chunk_overlap (int): The overlap between chunks.
            markdown_document (str): The content of the markdown document.

        Returns:
            list: A list of chunks.
        """
        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ]
        markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=headers_to_split_on, strip_headers=False
        )
        md_header_splits = markdown_splitter.split_text(markdown_document.content)

        # Recursive character text splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

        # Split
        splits = text_splitter.split_documents(md_header_splits)
        return splits

    def __load_markdown_document(self, path: str) -> Post:
        """
        Loads a markdown document and validates its frontmatter.

        Args:
            path (str): The path to the markdown document.

        Returns:
            dict: The loaded markdown document.
        """
        markdown_document = frontmatter.load(path)
        if len(markdown_document.keys()) == 0:
            raise ValueError(f"No frontmatter found in the markdown document at {path}...")
        if not markdown_document.get("title") or markdown_document.get("title").strip() == "":
            raise ValueError(f"No title found in the frontmatter of the markdown document at {path}...")
        if not markdown_document.get("summary") or markdown_document.get("summary").strip() == "":
            raise ValueError(f"No summary found in the frontmatter of the markdown document at {path}...")
        if not markdown_document.get("uri") or markdown_document.get("uri").strip() == "":
            raise ValueError(f"No uri found in the frontmatter of the markdown document at {path}...")
        if markdown_document.get("authors") is None or markdown_document.get("authors") == []:
            raise ValueError(f"No authors found in the frontmatter of the markdown document at {path}...")
        return markdown_document

    def __format_chunks(self, chunks, metadata, repository: str, path: str) -> dict:
        """
        Formats the chunks and returns a dictionary containing the metadata and contents.

        Args:
            chunks (list): The list of chunks.
            metadata (dict): The metadata of the markdown document.
            repository (str): The repository name.
            path (str): The path to the markdown document.

        Returns:
            dict: A dictionary containing the metadata and contents of the chunks.
        """
        page_metadatas = []
        page_contents = []
        today = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S-00:00")
        chunk_number: int = 0
        for chunk in chunks:
            chunk_number += 1
            page_metadatas.append({
                    "title": metadata.get("title"),
                    "source": path,
                    "uri": metadata.get("uri"),
                    "repository": repository,
                    "path": path,
                    "summary": metadata.get("summary"),
                    "authors": metadata.get("authors"),
                    "last_update": today,
                    "heading": chunk.metadata,
                    "chunk_number": chunk_number,
                }
            )
            page_contents.append(chunk.page_content)

        return {
            "page_metadatas": page_metadatas,
            "page_contents": page_contents,
        }
