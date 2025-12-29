import sys
import os
import pytest
# Make project root importable when running tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from demo import first_content_word, select_documents, CorpusEntry


def test_first_content_word_skips_articles_and_punctuation():
    assert first_content_word("La casa, bonita.") == "casa"
    assert first_content_word("  Y   perro") == "perro"
    assert first_content_word("(El) barco") == "barco"


def test_first_content_word_empty_returns_na():
    assert first_content_word("") == "N/A"
    assert first_content_word("   ") == "N/A"


def test_select_documents_prefers_docs_with_enough_entries():
    # Create fake doc_map with lengths
    a = [CorpusEntry("s", "n", "d", "A")] * 12
    b = [CorpusEntry("s", "n", "d", "B")] * 8
    c = [CorpusEntry("s", "n", "d", "C")] * 15
    doc_map = {"A": a, "B": b, "C": c}

    selected = select_documents(doc_map, n=2, min_entries=10)
    assert selected == ["A", "C"]


def test_select_documents_fallback_to_first_keys():
    # No doc has min_entries
    a = [CorpusEntry("s", "n", "d", "A")] * 3
    b = [CorpusEntry("s", "n", "d", "B")] * 2
    doc_map = {"A": a, "B": b}

    selected = select_documents(doc_map, n=3, min_entries=10)
    assert selected == ["A", "B"]
