import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from demo import extract_word_pairs, CorpusEntry


def make_entries(n, doc='D'):
    return [CorpusEntry(f"spanish {i}", f"nahuatl {i}", "Modern", doc) for i in range(n)]


def test_extract_word_pairs_handles_fewer_than_sample():
    docs = {"A": make_entries(5, "A")}
    pairs = extract_word_pairs(["A"], docs, per_doc=10)
    assert len(pairs) == 5
    # ensure ids are sequential and source is correct
    assert pairs[0]["id"] == 1 and pairs[-1]["id"] == 5
    assert all(p["source"] == "A" for p in pairs)


def test_extract_word_pairs_handles_empty_doc():
    docs = {"B": []}
    pairs = extract_word_pairs(["B"], docs, per_doc=10)
    assert pairs == []
