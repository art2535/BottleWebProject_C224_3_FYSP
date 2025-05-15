function buildGraph() {
    document.getElementById('treeMatrix').style.display = 'block';
}

function toggleTheory() {
    const container = document.querySelector(".theory-container");
    const content = document.getElementById("theoryContent");
    const isOpen = container.classList.toggle("open");
    content.style.display = isOpen ? "block" : "none";
}
