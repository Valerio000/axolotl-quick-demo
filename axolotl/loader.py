from typing import Protocol, Iterable, List
from .model import CorpusEntry

class CorpusLoader(Protocol):
    def load(self) -> Iterable[CorpusEntry]:
        ...

class DefaultCorpusLoader:
    def load(self) -> List[CorpusEntry]:
        import elotl.corpus
        raw = elotl.corpus.load('axolotl')
        if not raw:
            return []
        return [CorpusEntry(*entry[:5]) for entry in raw]
