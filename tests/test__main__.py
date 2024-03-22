import pytest
from src.document_importer.__main__ import main

@pytest.mark.parametrize("args", [
    (["-r","adp/example1", "-d","example_docs/example"]),
    (["--repository","adp/example1", "--directory","example_docs/example"]),    
])
def test_main_with_correct_args(args: list):
    main(["-r","adp/example1", "-d","example_docs/example"])

@pytest.mark.parametrize("args", [
    (["-d","example"]),
    (["-r","example"]),
    ([])    
])
def test_main_with_incorrect_args(args: list):
    with pytest.raises(SystemExit) as exc_info:
        main(args)
    assert str(exc_info.value) == "2"
