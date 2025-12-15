//
// Utility: raggruppa i valori delle labels
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

    // Converti Set -> array
    Object.keys(groups).forEach(k => groups[k] = [...groups[k]]);
    return groups;
}

//
// Ricerca full text
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
// Filtri AND/OR
// selected = {
//    domain: ["geo", "hydro"],
//    license: ["apache-2.0"],
//    ...
// }
// Logica SCELTA A:
//   OR dentro un gruppo
//   AND tra gruppi
//
export function filterByLabels(functions, selected) {

    return functions.filter(fn => {

        // Per ogni gruppo dei filtri (domain, license, ...)
        return Object.entries(selected).every(([key, values]) => {

            // Cerca  le chiavi nelle labels del tipo "labels":
            //  ["license:apache-2.0","domain:geo",...
            const fnValues = fn.metadata.labels
                .filter(l => l.startsWith(key + ":"))
                .map(l => l.split(":")[1]);

            // OR interno al gruppo:
            return values.some(v => fnValues.includes(v));
        });
    });
}

//
//  ricerca + filtri
//
export function applySearch(functions, text, selectedLabels) {
    let results = searchByText(functions, text);
    results = filterByLabels(results, selectedLabels);
    return results;
}
