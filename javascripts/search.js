import { getLabelGroups, applySearch } from "../javascripts/searchLibrary.js";

const sidebar = document.getElementById("filterGroups");
const searchInput = document.getElementById("search");
const resultsEl = document.getElementById("results");
const activeFiltersEl = document.getElementById("activeFilters");

let allData = [];
let selectedLabels = {};

init();

async function init() {
  const res = await fetch("../data.json");
  const json = await res.json();

  const path = location.pathname;
  const key = path.substring('/hub/'.length, path.lastIndexOf('/'));

  allData = json[key] || [];
  buildFilters(allData);
  updateResults();
}

function buildFilters(data) {
  const groups = getLabelGroups(data);

  Object.entries(groups).forEach(([group, values]) => {
    const details = document.createElement("details");
    details.className = "filter-group";
    details.open = true;

    details.innerHTML = `<summary>${group}</summary>`;

    values.forEach(value => {
      details.insertAdjacentHTML("beforeend", `
        <label class="filter-label">
          <input class="filter-checkbox" type="checkbox"
                 data-group="${group}" value="${value}">
          ${value}
        </label>
      `);
    });

    sidebar.appendChild(details);
  });

  sidebar.addEventListener("change", onFilterChange);
  searchInput.addEventListener("input", updateResults);
}

function onFilterChange(e) {
  const cb = e.target;
  if (!cb.classList.contains("filter-checkbox")) return;

  const { group } = cb.dataset;
  const value = cb.value;

  selectedLabels[group] ??= [];

  cb.checked
    ? selectedLabels[group].push(value)
    : selectedLabels[group] = selectedLabels[group].filter(v => v !== value);

  if (selectedLabels[group].length === 0) delete selectedLabels[group];

  updateResults();
}

function updateResults() {
  const text = searchInput.value;
  const results = applySearch(allData, text, selectedLabels);

  renderActiveFilters();
  renderResults(results);
}

function renderActiveFilters() {
  const entries = Object.entries(selectedLabels);

  if (entries.length === 0) {
    activeFiltersEl.style.display = "none";
    activeFiltersEl.innerHTML = "";
    return;
  }

  activeFiltersEl.style.display = "block";
  activeFiltersEl.innerHTML = entries.map(([group, values]) => `
    <div>
      <div class="filter-group-title">${group}</div>
      ${values.map(v => `<span class="filter-chip">${v}</span>`).join("")}
    </div>
  `).join("");
}

function renderResults(results) {
  if (!results.length) {
    resultsEl.innerHTML = `<div class="no-results">No results found.</div>`;
    return;
  }

  resultsEl.innerHTML = results.map(fn => `
    <div class="result-card">
      <a href="${fn.path}">${fn.metadata.name}</a>
      ${fn.metadata.version ? `<span class="version-badge">v${fn.metadata.version}</span>` : ""}
      <div class="subtitle">${fn.name}</div>
      <p>${fn.metadata.description}</p>
      ${fn.metadata.labels.map(l => {
        const [k, v] = l.split(":");
        return `<span class="chip ${selectedLabels[k]?.includes(v) ? "match" : ""}">${v}</span>`;
      }).join("")}
    </div>
  `).join("");
}
