Axolotl Web (Vite + React)

Quick start:

1. cd web
2. npm install
3. npm run dev

This minimal app loads `public/data/word_pairs_by_subject.json` and shows a grid of word pairs using a small `GlassCard` component (local shim used to avoid a missing package).

Notes:
- This is an MVP using a static JSON file. For larger datasets migrate to a small API with pagination.
- To build for production: `npm run build` and deploy the `dist/` directory.
