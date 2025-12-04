// searchLibrary.js

//recupera i dati delle funzioni da un URL e li restituisce come array

export async function loadData(url) {
    const res = await fetch(url);
    const data = await res.json();
    return Object.values(data.functions); 
}

// Filtra le funzioni in base al testo cercato nel nome o nella descrizione
export function filterByText(functions, text) {
    const t = text.toLowerCase();
    return functions.filter(fn =>
        fn.metadata.name.toLowerCase().includes(t) ||
        fn.metadata.description.toLowerCase().includes(t)
    );
}

// Raggruppa le etichette delle funzioni per chiave
export function getAllGroupedLabels(functions) {
    const groups = {}; 

    functions.forEach(fn => {
        fn.metadata.labels.forEach(label => {
            const [key, value] = label.split(":");
            if (!groups[key]) groups[key] = new Set();
            groups[key].add(value);
        });
    });

    Object.keys(groups).forEach(k => groups[k] = [...groups[k]]);
    return groups;
}
// Filtra le funzioni in base alle etichette selezionate
export function filterByLabel(functions, selected) {
    return functions.filter(fn => {
        return Object.entries(selected).every(([key, value]) =>
            fn.metadata.labels.includes(`${key}:${value}`)
        );
    });
}
