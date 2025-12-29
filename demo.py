#!/usr/bin/env python3
"""Compact, readable Axolotl demo.
Keep functions testable and clear while removing ceremony.
"""

from collections import defaultdict
import logging, json, re
from pathlib import Path
from typing import Iterable, Optional

from axolotl.model import CorpusEntry
from axolotl.loader import CorpusLoader, DefaultCorpusLoader

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

SKIP_WORDS = {w.lower() for w in ('y', 'el', 'la', 'los', 'las', 'un', 'una', 'de', 'en')}
SAMPLE_PER_DOC = 10
OUT = Path("word_pairs_by_subject.json")
SNIP = 60
PUNCT = re.compile(r'^\W+|\W+$')


def load_corpus(loader: Optional[CorpusLoader] = None) -> Iterable[CorpusEntry]:
    """Load entries via the provided loader (or the DefaultCorpusLoader)."""
    if loader is None:
        loader = DefaultCorpusLoader()
    return list(loader.load())


def categorize_by_document(entries):
    docs = defaultdict(list)
    for e in entries:
        if e.spanish.strip() and e.nahuatl.strip():
            docs[e.document].append(e)
    return docs


def select_documents(doc_map, n: int = 3, min_entries: int = 10):
    chosen = [name for name, items in doc_map.items() if len(items) >= min_entries]
    return chosen[:n] if len(chosen) >= n else list(doc_map)[:n]


def first_content_word(text: str) -> str:
    last = ""
    for tok in (t.strip() for t in text.split()):
        tok = PUNCT.sub("", tok)
        if not tok:
            continue
        last = tok
        if tok.lower() not in SKIP_WORDS:
            return tok
    return last or "N/A"


def extract_word_pairs(selected_docs, docs, per_doc=SAMPLE_PER_DOC):
    pairs, cnt = [], 0
    for doc in selected_docs:
        for e in docs.get(doc, [])[:per_doc]:
            cnt += 1
            s = first_content_word(e.spanish)
            n = first_content_word(e.nahuatl)
            pairs.append({
                "id": cnt,
                "spanish": s,
                "nahuatl": n,
                "dialect": e.dialect,
                "source": doc,
                "full_spanish": (e.spanish[:SNIP] + "...") if len(e.spanish) > SNIP else e.spanish,
                "full_nahuatl": (e.nahuatl[:SNIP] + "...") if len(e.nahuatl) > SNIP else e.nahuatl,
            })
    return pairs


def write_output(pairs, entries, doc_map, selected_docs):
    classical = sum(1 for p in pairs if "Classical" in p["dialect"])
    stats = {
        "total_sentences": len(entries),
        "total_documents": len(doc_map),
        "selected_documents": selected_docs,
        "classical_count": classical,
        "modern_count": len(pairs) - classical,
    }
    OUT.write_text(json.dumps({"corpus_stats": stats, "word_pairs": pairs}, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.info("Exported %s", OUT)


def main():
    try:
        entries = load_corpus()
    except Exception as e:
        logger.error("Failed to load corpus: %s", e)
        return

    docs = categorize_by_document(entries)
    if not docs:
        logger.error("No documents found in corpus")
        return

    selected = select_documents(docs)
    pairs = extract_word_pairs(selected, docs)
    write_output(pairs, entries, docs, selected)
    logger.info("Done: %d word pairs from %d subjects", len(pairs), len(selected))


if __name__ == "__main__":
    main()
