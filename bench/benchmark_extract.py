"""Simple benchmark for extract_word_pairs using synthetic corpora.
Usage: python bench/benchmark_extract.py
"""
import time
from typing import Optional


def make_entries(n: int, doc: str = "D"):
    # Local import to avoid modifying sys.path at import time
    from axolotl.model import CorpusEntry

    return [
        CorpusEntry(f"spanish {i}", f"nahuatl {i}", "Modern", doc)
        for i in range(n)
    ]


def benchmark(size: int, per_doc: Optional[int] = None):
    # create 3 documents each with 'size' entries
    from demo import categorize_by_document, extract_word_pairs

    entries = []
    for doc in ("A", "B", "C"):
        entries.extend(make_entries(size, doc=doc))

    docs = categorize_by_document(entries)
    selected = list(docs.keys())[:3]

    if per_doc is None:
        per_doc = size

    start = time.perf_counter()
    pairs = extract_word_pairs(selected, docs, per_doc=per_doc)
    elapsed = time.perf_counter() - start
    return elapsed, len(pairs)


if __name__ == "__main__":
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(root))

    sizes = [1000, 5000, 10000]
    print("Benchmarking extract_word_pairs (per_doc=size)")
    for s in sizes:
        t, count = benchmark(s)
        print(f"size={s:6d}: time={t:.4f}s, produced={count}")
