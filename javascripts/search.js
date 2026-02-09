import { getLabelGroups, applySearch } from "../javascripts/searchLibrary.js";

const sidebar = document.getElementById("filterGroups");
const searchInput = document.getElementById("search");
const resultsEl = document.getElementById("results");
const activeFiltersEl = document.getElementById("activeFilters");

let allData = [];
let selectedLabels = {};
let indexPage = false;

init();

async function init() {
  const path = location.pathname;
  const secondLastIndex = path.lastIndexOf('/', path.lastIndexOf('/')-1);
  const key = path.substring(secondLastIndex+1, path.lastIndexOf("/"));
  
  if (path === "/" || path === "/hub/") {
    indexPage = true
  }
  
  let dataPath = "./data.json";
  if (!indexPage) {
	  dataPath = "." + dataPath;
  }
  
  const res = await fetch("../data.json");
  const json = await res.json();
  
  allData = indexPage ? mergeAllCategories(json) : json[key] || [];
  buildFilters(allData);
  updateResults();
}

function mergeAllCategories(json) {
  let allData = [];

  for (const [category, templatesArray] of Object.entries(json)) {
    for (const template of templatesArray) {
      template["category"] = category;
      template.metadata.labels.push("category:" + category);
      allData.push(template);
    }
  }
  
  return allData;
}

function buildFilters(data) {
  const groups = getLabelGroups(data)
  
  const groupsArray = Object.keys(groups).map(key => ({
    group: key,
    values: groups[key]
  }));
  
  groupsArray.sort(function(x, y) {
    if (x["group"] == "category") {
      return -1;
    }
	if (y["group"] == "category") {
      return 1;
    }
    return x["group"].localeCompare(y["group"]);
  });

  groupsArray.forEach(f => {
	const group = f["group"];
	const values = f["values"];
	
    const details = document.createElement("details");
    details.className = "filter-group";
    if (!indexPage) {
      details.open = true;
    }

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
	  ${indexPage ? `<span class="category">${fn.category}</span>` : ""}
      ${fn.metadata.version ? `<span class="version-badge">v${fn.metadata.version}</span>` : ""}
      <div class="subtitle">${fn.name}</div>
      <p>${fn.metadata.description}</p>
      ${fn.metadata.labels.map(l => {
        const [k, v] = l.split(":");
        return k === "category" ? "" : `<span class="chip ${selectedLabels[k]?.includes(v) ? "match" : ""}">${v}</span>`;
      }).join("")}
    </div>
  `).join("");
}
