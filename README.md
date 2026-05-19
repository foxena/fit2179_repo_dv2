# FIT2179 Data Visualisation 2 — Running Beyond Marathon Distance

This repository is a GitHub Pages-ready Vega-Lite data visualisation project.

## Story focus

The visualisation is not about a sports-watch brand. It uses one privacy-safe personal training log to make a broader running question concrete: what does the build-up to a 50 km run look like, and how does that effort compare with Australian ultra-marathon results?

## How to run locally

Because the page loads local JSON/CSV files, run it through a local web server rather than opening `index.html` directly:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000`.

## GitHub Pages upload structure

Upload the whole folder contents to a GitHub repository, then enable GitHub Pages from the repository settings.

Required files:

- `index.html`
- `css/style.css`
- `js/main.js`
- `data/*.json`, `data/*.csv` and `data/*.geojson`
- `specs/*.json`

The `specs` folder contains human-readable Vega-Lite JSON specifications.

## Privacy

The personal watch data has been reduced to activity summaries. Raw GPS route data is not included.

The Kaggle ultra-marathon files have also been aggregated before publication. They do not include athlete names, athlete IDs or individual-level race records.

## Personal training-log processing note

The watch export came from COROS FIT files. The parser skips developer-field bytes in data messages. Without this, FIT records become misaligned and many Running sessions are missed. The final personal dataset uses 99 Running sessions of at least 20 minutes, excluding short warm-up/test segments and all raw GPS traces. The longest run is 50.15 km on 2026-03-07.

## Public running comparison note

The Kaggle ultra-marathon dataset was processed outside the final webpage and reduced to small Australian aggregate files: finishers by year, distance summaries, 50 km speed bands, 50 km finish-time bands, age/gender summaries and distance/gender summaries. These files are lightweight enough for GitHub Pages and Vega-Lite.
