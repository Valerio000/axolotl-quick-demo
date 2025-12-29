Design: Decouple corpus loader from CLI/processing

Problem

The current implementation directly calls `elotl.corpus.load('axolotl')` inside `demo.py`. This couples the processing logic to an external, I/O heavy dependency and makes unit testing and substitution (e.g., loading from different sources) harder.

Proposal

Introduce a small loader abstraction and a default implementation:

- Interface:

  ```py
  from typing import Protocol, Iterable
  from axolotl.model import CorpusEntry

  class CorpusLoader(Protocol):
      def load(self) -> Iterable[CorpusEntry]:
          ...
  ```

- Default implementation:

  ```py
  class DefaultCorpusLoader:
      def load(self):
          import elotl.corpus
          raw = elotl.corpus.load('axolotl')
          return [CorpusEntry(*entry[:5]) for entry in raw]
  ```

- Tests will use a `FakeLoader` that returns deterministic `CorpusEntry` objects so processing functions can be validated without external I/O.

Trade-offs

- Backwards compatibility: `demo.py` will accept an optional loader parameter; when omitted it uses `DefaultCorpusLoader()` for the original behavior.
- This adds a small amount of indirection but drastically improves testability and opens the door to alternative data sources (files, HTTP, fixtures).

Test plan

- Add `tests/test_loader.py` that provides a `FakeLoader` and verifies the pipeline (`categorize_by_document` → `select_documents` → `extract_word_pairs`) behaves deterministically.

Migration steps

1. Add `axolotl/model.py` with `CorpusEntry` dataclass.
2. Add `axolotl/loader.py` with `CorpusLoader` Protocol and `DefaultCorpusLoader`.
3. Update `demo.py` to use injected loader or default loader.
4. Add tests and PR with design doc link.
