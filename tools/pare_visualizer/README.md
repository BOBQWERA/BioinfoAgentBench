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

## Publish online with GitHub Pages

This repository includes `.github/workflows/deploy-visualizer.yml`, which publishes
`tools/pare_visualizer/` with GitHub Pages.

1. Push the repository to GitHub.
2. Open `Settings -> Pages` in the GitHub repository.
3. Set `Source` to `GitHub Actions`.
4. Push to `main`, or manually run `Deploy PARE Visualizer` from the `Actions` tab.

Each deployment rebuilds `data/scores_index.json` from `examples/pare_outputs/` before
publishing.

## Data source

The index builder scans `examples/pare_outputs/` and writes
`tools/pare_visualizer/data/scores_index.json`.
