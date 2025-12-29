#!/usr/bin/env python3
"""
Refactored Axolotl demo: clearer structure, types, and testability.
"""

from dataclasses import dataclass
from collections import defaultdict
from typing import List, Dict, Iterable
import logging
import json
import re
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure defaults
SKIP_WORDS = {w.lower() for w in ('y', 'el', 'la', 'los', 'las', 'un', 'una', 'de', 'en')}
SAMPLE_PER_DOC = 10
OUTPUT_FILE = Path("word_pairs_by_subject.json")
WORD_SNIPPET_LEN = 60
PUNCT_RE = re.compile(r'^\W+|\W+$')

@dataclass
class CorpusEntry:
    spanish: str
    nahuatl: str
    dialect: str
    document: str
    iso: str = ""

def load_corpus(name: str = "axolotl") -> List[CorpusEntry]:
    import elotl.corpus  # local import so module errors are localized
    logger.info("Loading corpus '%s'...", name)
    raw = elotl.corpus.load(name)
    if not raw:
        raise RuntimeError("Corpus not found or empty")
    # Support entries with up to 5 fields; fill missing with empty strings
    return [CorpusEntry(*entry[:5]) for entry in raw]

def categorize_by_document(entries: Iterable[CorpusEntry]) -> Dict[str, List[CorpusEntry]]:
    docs: Dict[str, List[CorpusEntry]] = defaultdict(list)
    for e in entries:
        if e.spanish.strip() and e.nahuatl.strip():
            docs[e.document].append(e)
    return docs

def select_documents(doc_map: Dict[str, List[CorpusEntry]], n: int = 3, min_entries: int = 10) -> List[str]:
    chosen = [name for name, items in doc_map.items() if len(items) >= min_entries]
    if len(chosen) >= n:
        return chosen[:n]
    return list(doc_map.keys())[:n]

def first_content_word(text: str) -> str:
    token = ""
    for t in (t.strip() for t in text.split()):
        t = PUNCT_RE.sub("", t)
        if not t:
            continue
        token = t
        if token.lower() in SKIP_WORDS:
            continue
        return token
    return token or "N/A"

def extract_word_pairs(selected_docs: List[str], docs: Dict[str, List[CorpusEntry]], per_doc: int = SAMPLE_PER_DOC):
    word_pairs = []
    counter = 0
    for doc in selected_docs:
        for entry in docs.get(doc, [])[:per_doc]:
            counter += 1
            spanish_word = first_content_word(entry.spanish)
            nahuatl_word = first_content_word(entry.nahuatl)
            word_pairs.append({
                "id": counter,
                "spanish": spanish_word,
                "nahuatl": nahuatl_word,
                "dialect": entry.dialect,
                "source": doc,
                "full_spanish": (entry.spanish[:WORD_SNIPPET_LEN] + "...") if len(entry.spanish) > WORD_SNIPPET_LEN else entry.spanish,
                "full_nahuatl": (entry.nahuatl[:WORD_SNIPPET_LEN] + "...") if len(entry.nahuatl) > WORD_SNIPPET_LEN else entry.nahuatl
            })
    return word_pairs

def summarize(all_pairs, entries, doc_map, selected_docs):
    classical = sum(1 for p in all_pairs if "Classical" in p["dialect"])
    return {
        "total_sentences": len(entries),
        "total_documents": len(doc_map),
        "selected_documents": selected_docs,
        "classical_count": classical,
        "modern_count": len(all_pairs) - classical
    }

def export_json(data: dict, out: Path):
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.info("Exported %s", out)


def main():
    try:
        entries = load_corpus()
    except Exception as exc:
        logger.error("Failed to load corpus: %s", exc)
        return

    doc_map = categorize_by_document(entries)
    if not doc_map:
        logger.error("No documents found in corpus")
        return

    logger.info("Found %d document sources", len(doc_map))

    selected_docs = select_documents(doc_map)
    logger.info("Selected %d documents: %s", len(selected_docs), selected_docs)

    pairs = extract_word_pairs(selected_docs, doc_map)
    stats = summarize(pairs, entries, doc_map, selected_docs)
    export_json({"corpus_stats": stats, "word_pairs": pairs}, OUTPUT_FILE)
    logger.info("Done: %d word pairs from %d subjects", len(pairs), len(selected_docs))

if __name__ == "__main__":
    main()
