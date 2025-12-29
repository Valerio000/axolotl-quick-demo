import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from demo import load_corpus, categorize_by_document, select_documents, extract_word_pairs
from axolotl.model import CorpusEntry


class FakeLoader:
    def __init__(self, items):
        self._items = items

    def load(self):
        return self._items


def make_corpus(n, doc='X'):
    return [CorpusEntry(f"S {i}", f"N {i}", "Modern", doc) for i in range(n)]


def test_pipeline_with_fake_loader():
    entries = make_corpus(12, doc='A') + make_corpus(8, doc='B')
    loader = FakeLoader(entries)

    loaded = list(load_corpus(loader))
    assert len(loaded) == 20

    docs = categorize_by_document(loaded)
    selected = select_documents(docs, n=2, min_entries=10)
    assert selected == ['A', 'B'] or selected == ['A'] or 'A' in selected

    pairs = extract_word_pairs(selected, docs, per_doc=5)
    assert all(p['source'] in ('A', 'B') for p in pairs)
    assert len(pairs) == 10 or len(pairs) == 5
