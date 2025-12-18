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