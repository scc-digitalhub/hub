function openTab(tabName) {
    // Hide all tabs and show the selected one
    let tabs = document.getElementsByClassName("template-info-tab");
    for (let tab of tabs) {
        tab.style.display = "none";
    }
    document.getElementById("template-" + tabName).style.display = "block";

    // Mark all tab buttons as deselected and highlight the selected one
    let tabButtons = document.getElementsByClassName("tab-button");
    for (let button of tabButtons) {
        button.classList.remove("tab-button-selected");
        button.classList.add("tab-button-not-selected");
    }
    let selectedTabButton = document.getElementById("tab-button-" + tabName)
    selectedTabButton.classList.remove("tab-button-not-selected");
    selectedTabButton.classList.add("tab-button-selected");
}

function toggleRef() {
    const clickedClass = "hub-ref-button-clicked";
    const iconExpand = "&#x25BC;";
    const iconCollapse = "&#x25B2;";

    let button = document.getElementById('hub-ref-text');
    let buttonIcon = document.getElementById('hub-ref-icon');
    let ref = document.getElementById("hub-ref-link");
    
    if (button.classList.contains(clickedClass)) {
        // Collapse
        button.classList.remove(clickedClass);
        buttonIcon.innerHTML = iconExpand;
        ref.style.display = "none";
    } else {
        // Expand
        button.classList.add(clickedClass);
        buttonIcon.innerHTML = iconCollapse;
        ref.style.display = "block";
    }
}

function copyRef() {
    let ref = document.getElementById('hub-ref-link-text');
    navigator.clipboard.writeText(ref.innerHTML);
}