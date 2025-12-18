//
// Utility: Groups label values together
//
export function getLabelGroups(functions) {
    const groups = {};

    functions.forEach(fn => {
        fn.metadata.labels.forEach(label => {
            const [key, value] = label.split(":");
            if (!groups[key]) groups[key] = new Set();
            groups[key].add(value);
        });
    });

    // Convert Set -> array
    Object.keys(groups).forEach(k => groups[k] = [...groups[k]]);
    return groups;
}

//
// Full text search
//
export function searchByText(functions, text) {
    if (!text.trim()) return functions;
    const q = text.toLowerCase();

    return functions.filter(fn =>
        fn.metadata.name.toLowerCase().includes(q) ||
        fn.metadata.description.toLowerCase().includes(q)
    );
}

//
// AND/OR filters
// selected = {
//    domain: ["geo", "hydro"],
//    license: ["apache-2.0"],
//    ...
// }
// Logic:
//   OR within a group
//   AND between groups
//
export function filterByLabels(functions, selected) {

    return functions.filter(fn => {

        // For each group filter (domain, license, ...)
        return Object.entries(selected).every(([key, values]) => {

            // Search keys in labels:
            //  ["license:apache-2.0","domain:geo",...
            const fnValues = fn.metadata.labels
                .filter(l => l.startsWith(key + ":"))
                .map(l => l.split(":")[1]);

            // OR within a group:
            return values.some(v => fnValues.includes(v));
        });
    });
}

//
//  Search and filters
//
export function applySearch(functions, text, selectedLabels) {
    let results = searchByText(functions, text);
    results = filterByLabels(results, selectedLabels);
    return results;
}
