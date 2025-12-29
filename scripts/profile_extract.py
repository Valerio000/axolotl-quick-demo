"""Profile extract_word_pairs using cProfile and write a text report.
Usage: python scripts/profile_extract.py [size]
"""
import sys

import cProfile
import pstats


def make_entries(n: int, doc: str = "D"):
    # Local import to avoid requiring sys.path hacks at module import time
    from axolotl.model import CorpusEntry

    return [
        CorpusEntry(f"spanish {i}", f"nahuatl {i}", "Modern", doc)
        for i in range(n)
    ]


def run(size: int = 5000):
    # Ensure imports happen after potential sys.path adjustment when running as script
    from demo import categorize_by_document, extract_word_pairs

    entries = []
    for doc in ("A", "B", "C"):
        entries.extend(make_entries(size, doc=doc))
    docs = categorize_by_document(entries)
    selected = list(docs.keys())[:3]

    def target() -> None:
        extract_word_pairs(selected, docs, per_doc=10)

    profiler = cProfile.Profile()
    profiler.runcall(target)
    stats = pstats.Stats(profiler).sort_stats("cumulative")
    stats.dump_stats("profile_extract.pstats")
    stats.print_stats(40)


if __name__ == "__main__":
    size = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    run(size)
