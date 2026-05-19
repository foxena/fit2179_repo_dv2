# Moodle 500-word response draft

## Domain, why and who

My domain is recreational running and ultra-distance running in Australia. The visualisation is designed for an average Australian audience who may understand running as a simple activity, but may not know how training volume, terrain and race distance change what a run means. The purpose is to tell a broader story about what it takes to move beyond marathon distance, using one runner’s training log as a concrete example and Australian public running-event data as the comparison point.

## What

The visualisation combines multiple real-world datasets. A personal running-watch export was processed into privacy-safe summaries including date, distance, duration, pace, heart rate and elevation gain. Raw GPS traces were excluded. Public running-event context comes from the Kaggle Big Dataset of Ultra-Marathon Running, filtered to Australian events from 2015–2022 and aggregated into small files covering 50 km, 100 km and 100 mile results. No athlete names, IDs or individual records are published. AusPlay By Sport Data Tables, released 30 April 2026, provide Australian running/jogging participation context by activity, age, gender and organising entity. AusPlay National Data Tables provide state/territory physical activity frequency data for the required map. ABS ASGS Edition 3 state/territory boundaries were simplified into GeoJSON for fast loading.

## How

The page uses a scrolling story layout rather than a dashboard. The first section establishes the central question and uses KPI cards plus a distance ladder to make 50 km meaningful for a broad audience. The Australian context section uses a map, ranked bars and grouped bars to show that running is popular but often self-directed. The public running-event section uses line charts, bar charts and a bubble plot to compare the 50.15 km training run with aggregated Australian ultra-marathon results. The training-log section uses layered charts, a weekly area chart, a calendar heatmap and scatterplots to reveal training rhythm, volume, terrain and effort. The final custom-built effort matrix combines derived data into a relative score using average heart rate, distance and elevation gain per kilometre. Interactivity is limited to tooltips because the assignment focuses on presentation and storytelling, not expert exploration.

## AI acknowledgement

ChatGPT was used to assist with data processing, Vega-Lite specification drafting, HTML/CSS structure and copy editing. The final visualisation, design decisions and submission should be reviewed by the student before submission.
