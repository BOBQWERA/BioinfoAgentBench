const DIMENSIONS = ["P", "A", "R", "E"];
const DIMENSION_LABELS = ["Planning", "Action", "Reflection", "Evolution"];
const COLORS = [
  "#1667ff",
  "#19b987",
  "#ff7a59",
  "#9a56ff",
  "#00a3c4",
  "#f5a524",
  "#ef476f",
  "#2d8fdd",
];

const state = {
  records: [],
  benchStats: {},
  selectedBench: "all",
  search: "",
  selectedIds: new Set(),
  overlayChart: null,
  benchChart: null,
  detailCharts: new Map(),
};

const el = {
  benchSelect: document.getElementById("benchSelect"),
  searchInput: document.getElementById("searchInput"),
  questionList: document.getElementById("questionList"),
  detailCards: document.getElementById("detailCards"),
  recordCountTag: document.getElementById("recordCountTag"),
  selectedCountTag: document.getElementById("selectedCountTag"),
  benchStatsTag: document.getElementById("benchStatsTag"),
  clearSelectionBtn: document.getElementById("clearSelectionBtn"),
  overlayRadar: document.getElementById("overlayRadar"),
  benchRadar: document.getElementById("benchRadar"),
};

function getFilteredRecords() {
  const search = state.search.trim().toLowerCase();
  return state.records.filter((r) => {
    const benchMatch = state.selectedBench === "all" || r.bench === state.selectedBench;
    if (!benchMatch) return false;
    if (!search) return true;
    const blob = `${r.id} ${r.question}`.toLowerCase();
    return blob.includes(search);
  });
}

function getSelectedRecords() {
  return state.records.filter((r) => state.selectedIds.has(r.id));
}

function scoreArray(rec) {
  return DIMENSIONS.map((d) => Number(rec?.scores?.[d] ?? 0));
}

function shortText(text, n = 115) {
  if (!text) return "";
  return text.length > n ? `${text.slice(0, n)}...` : text;
}

function updateBenchSelector() {
  const benches = [...new Set(state.records.map((x) => x.bench))];
  el.benchSelect.innerHTML = [
    `<option value="all">All Benchmarks (${benches.length})</option>`,
    ...benches.map((b) => `<option value="${b}">${b}</option>`),
  ].join("");
}

function renderQuestionList() {
  const rows = getFilteredRecords();
  el.recordCountTag.textContent = `${rows.length} records`;
  if (!rows.length) {
    el.questionList.innerHTML = `<div class="empty">No records match the current filters.</div>`;
    return;
  }

  el.questionList.innerHTML = rows
    .map((r) => {
      const selectedCls = state.selectedIds.has(r.id) ? "selected" : "";
      return `
      <article class="question-item ${selectedCls}" data-id="${r.id}">
        <div class="qid">${r.id}</div>
        <div class="qtext">${shortText(r.question)}</div>
        <div class="score-strip">
          <span class="pill">P ${r.scores.P}</span>
          <span class="pill">A ${r.scores.A}</span>
          <span class="pill">R ${r.scores.R}</span>
          <span class="pill">E ${r.scores.E}</span>
        </div>
      </article>
      `;
    })
    .join("");
}

function makeRadarConfig(datasets, maxValue = 5) {
  return {
    type: "radar",
    data: {
      labels: DIMENSION_LABELS,
      datasets,
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          labels: {
            boxWidth: 14,
            color: "#2f3850",
            font: { family: "Plus Jakarta Sans", size: 12, weight: "600" },
          },
        },
      },
      scales: {
        r: {
          min: 0,
          max: maxValue,
          ticks: { stepSize: 1, backdropColor: "transparent", color: "#7a849f" },
          angleLines: { color: "rgba(89, 107, 151, 0.2)" },
          grid: { color: "rgba(89, 107, 151, 0.2)" },
          pointLabels: { color: "#4a577b", font: { weight: "700", size: 12 } },
        },
      },
    },
  };
}

function renderOverlayChart() {
  const selected = getSelectedRecords();
  el.selectedCountTag.textContent = `${selected.length} selected`;
  if (state.overlayChart) state.overlayChart.destroy();

  const datasets = selected.slice(0, 12).map((r, i) => {
    const c = COLORS[i % COLORS.length];
    return {
      label: r.id,
      data: scoreArray(r),
      borderColor: c,
      backgroundColor: `${c}22`,
      pointBackgroundColor: c,
      borderWidth: 2,
      tension: 0.2,
    };
  });
  state.overlayChart = new Chart(el.overlayRadar, makeRadarConfig(datasets));
}

function renderBenchChart() {
  const bench = state.selectedBench;
  if (state.benchChart) state.benchChart.destroy();

  if (bench === "all" || !state.benchStats[bench]) {
    el.benchStatsTag.textContent = "Select one benchmark";
    state.benchChart = new Chart(el.benchRadar, makeRadarConfig([]));
    return;
  }

  const stat = state.benchStats[bench];
  el.benchStatsTag.textContent = `n=${stat.count}`;
  const row = stat.avg_scores;
  state.benchChart = new Chart(
    el.benchRadar,
    makeRadarConfig([
      {
        label: `${bench} avg`,
        data: [row.P, row.A, row.R, row.E],
        borderColor: "#161d2f",
        backgroundColor: "rgba(22, 29, 47, 0.15)",
        pointBackgroundColor: "#161d2f",
        borderWidth: 2,
      },
    ])
  );
}

function tokenTotal(record) {
  const tu = record.token_usage || {};
  const total = tu.total || tu;
  return Number(total.total_tokens || 0);
}

function confidenceText(record) {
  const c = record.confidence;
  if (typeof c !== "number") return "-";
  return c.toFixed(2);
}

function renderDetails() {
  const selected = getSelectedRecords();
  if (!selected.length) {
    el.detailCards.innerHTML = `<div class="empty">Select at least one record to inspect the score breakdown.</div>`;
    return;
  }

  el.detailCards.innerHTML = selected
    .slice(0, 6)
    .map(
      (r) => `
      <article class="detail-card" id="card-${r.id}">
        <div class="detail-header">
          <div>
            <div class="qid">${r.id}</div>
            <div class="meta">${r.bench} · ${r.model || "-"} · ${r.scoring_mode || "-"}</div>
          </div>
          <span class="tag">Single-record radar</span>
        </div>
        <div class="detail-body">
          <div class="mini-chart"><canvas id="mini-${r.id}"></canvas></div>
          <div>
            <div class="metric-grid">
              <div class="metric"><div class="k">Planning (P)</div><div class="v">${r.scores.P}</div></div>
              <div class="metric"><div class="k">Action (A)</div><div class="v">${r.scores.A}</div></div>
              <div class="metric"><div class="k">Reflection (R)</div><div class="v">${r.scores.R}</div></div>
              <div class="metric"><div class="k">Evolution (E)</div><div class="v">${r.scores.E}</div></div>
              <div class="metric"><div class="k">Confidence</div><div class="v">${confidenceText(r)}</div></div>
              <div class="metric"><div class="k">Total Tokens</div><div class="v">${tokenTotal(r)}</div></div>
            </div>
            <p class="summary">${r.overall_summary || "No summary."}</p>
            <ul class="reason-list">
              ${DIMENSIONS.map(
                (d) =>
                  `<li><strong>${d}:</strong> ${shortText(r.reason?.[d] || "-", 300)}</li>`
              ).join("")}
            </ul>
          </div>
        </div>
      </article>
      `
    )
    .join("");

  selected.slice(0, 6).forEach((r, i) => {
    const canvas = document.getElementById(`mini-${r.id}`);
    if (!canvas) return;
    const old = state.detailCharts.get(r.id);
    if (old) old.destroy();
    const c = COLORS[i % COLORS.length];
    const chart = new Chart(
      canvas,
      makeRadarConfig([
        {
          label: r.id,
          data: scoreArray(r),
          borderColor: c,
          backgroundColor: `${c}24`,
          pointBackgroundColor: c,
          borderWidth: 2,
        },
      ])
    );
    state.detailCharts.set(r.id, chart);
  });
}

function bindEvents() {
  el.benchSelect.addEventListener("change", () => {
    state.selectedBench = el.benchSelect.value;
    renderQuestionList();
    renderBenchChart();
  });

  el.searchInput.addEventListener("input", () => {
    state.search = el.searchInput.value || "";
    renderQuestionList();
  });

  el.clearSelectionBtn.addEventListener("click", () => {
    state.selectedIds.clear();
    renderQuestionList();
    renderOverlayChart();
    renderDetails();
  });

  el.questionList.addEventListener("click", (e) => {
    const item = e.target.closest(".question-item");
    if (!item) return;
    const id = item.dataset.id;
    if (!id) return;
    if (state.selectedIds.has(id)) {
      state.selectedIds.delete(id);
    } else {
      state.selectedIds.add(id);
    }
    renderQuestionList();
    renderOverlayChart();
    renderDetails();
  });
}

async function init() {
  const res = await fetch("./data/scores_index.json");
  if (!res.ok) throw new Error(`Failed to load index json: ${res.status}`);
  const payload = await res.json();
  state.records = payload.records || [];
  state.benchStats = payload.bench_stats || {};

  updateBenchSelector();
  renderQuestionList();
  renderOverlayChart();
  renderBenchChart();
  renderDetails();
  bindEvents();
}

init().catch((err) => {
  console.error(err);
  document.body.innerHTML = `<main style="padding:30px;font-family:sans-serif"><h2>Failed to load visualizer data</h2><pre>${String(
    err
  )}</pre></main>`;
});

