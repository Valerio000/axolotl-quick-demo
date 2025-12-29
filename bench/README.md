Benchmark & profiling instructions

- Run the simple benchmark:
  - python bench/benchmark_extract.py

- Run a profiler run (writes profile_extract.pstats and prints top lines):
  - python scripts/profile_extract.py 5000

Notes:
- The benchmark is synthetic and aims to highlight time spent in `extract_word_pairs` and `first_content_word`.
- Use cProfile output to identify hotspots and guide targeted optimizations.
