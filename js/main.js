const charts = [
  {
    "id": "vis-distance-ladder",
    "spec": "specs/19_running_distance_benchmarks.json"
  },
  {
    "id": "vis-map",
    "spec": "specs/01_map_state_activity_frequency.json"
  },
  {
    "id": "vis-top",
    "spec": "specs/02_top_activities.json"
  },
  {
    "id": "vis-age",
    "spec": "specs/03_running_age_profile.json"
  },
  {
    "id": "vis-gender",
    "spec": "specs/04_running_gender_organised.json"
  },
  {
    "id": "vis-entities",
    "spec": "specs/05_running_organising_entities.json"
  },
  {
    "id": "vis-ultra-year",
    "spec": "specs/13_kaggle_ultra_finishers_by_year.json"
  },
  {
    "id": "vis-ultra-summary",
    "spec": "specs/14_kaggle_ultra_distance_summary.json"
  },
  {
    "id": "vis-50-speed",
    "spec": "specs/15_kaggle_50km_speed_distribution.json"
  },
  {
    "id": "vis-50-time",
    "spec": "specs/16_kaggle_50km_finish_time_distribution.json"
  },
  {
    "id": "vis-50-age",
    "spec": "specs/17_kaggle_50km_speed_by_age_gender.json"
  },
  {
    "id": "vis-monthly",
    "spec": "specs/07_coros_monthly_load.json"
  },
  {
    "id": "vis-weekly",
    "spec": "specs/08_coros_weekly_distance.json"
  },
  {
    "id": "vis-calendar",
    "spec": "specs/09_coros_calendar_heatmap.json"
  },
  {
    "id": "vis-scatter",
    "spec": "specs/10_coros_distance_pace_scatter.json"
  },
  {
    "id": "vis-hr-hills",
    "spec": "specs/11_coros_hr_hills.json"
  },
  {
    "id": "vis-effort",
    "spec": "specs/12_coros_effort_matrix.json"
  }
];

async function loadKpis() {
  const res = await fetch('data/project_kpis.json');
  const k = await res.json();
  const fmt = new Intl.NumberFormat('en-AU');
  const one = new Intl.NumberFormat('en-AU', { maximumFractionDigits: 1 });
  const fields = {
    kpiActivities: fmt.format(k.activity_count),
    kpiDistance: one.format(k.total_distance_km) + ' km',
    kpiHours: one.format(k.total_duration_hr) + ' hr',
    kpiElevation: fmt.format(k.total_elevation_gain_m) + ' m',
    kpiRange: k.first_activity + ' to ' + k.last_activity,
    kpiMedian: one.format(k.median_distance_km) + ' km median activity',
    kpiTypes: 'Running',
    kpiUltra: one.format(k.longest_run_km) + ' km on ' + k.longest_run_date
  };
  for (const [id, value] of Object.entries(fields)) {
    const el = document.getElementById(id);
    if (el) el.textContent = value;
  }
}

async function embedCharts() {
  for (const item of charts) {
    const el = document.getElementById(item.id);
    if (!el) continue;
    try {
      await vegaEmbed(el, item.spec, { actions: false, renderer: 'canvas' });
    } catch (error) {
      el.innerHTML = '<p class="error">Could not load this visualisation. Check the local file path or run through a local server.</p>';
      console.error(item.id, error);
    }
  }
}

loadKpis();
embedCharts();
