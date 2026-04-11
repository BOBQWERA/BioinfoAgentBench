# PARE Visualizer

`tools/pare_visualizer/` is a static viewer for committed example PARE outputs.

## Rebuild the index

```bash
python tools/pare_visualizer/scripts/build_scores_index.py
```

## Serve locally

From `tools/pare_visualizer/`:

```bash
python -m http.server 8090
```

Then open `http://127.0.0.1:8090`.

## Data source

The index builder scans `examples/pare_outputs/` and writes
`tools/pare_visualizer/data/scores_index.json`.
