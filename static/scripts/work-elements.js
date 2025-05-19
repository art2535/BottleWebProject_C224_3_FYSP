function buildGraph() {
    document.getElementById('treeMatrix').style.display = 'block';
}

function toggleTheory() {
    const container = document.querySelector(".theory-container");
    const content = document.getElementById("theoryContent");
    const isOpen = container.classList.toggle("open");
    content.style.display = isOpen ? "block" : "none";
}

function updateMatrix() {
    const vertices = parseInt(document.getElementById('vertices').value) || 3;
    if (vertices < 1 || vertices > 8) return;

    const table = document.getElementById('matrixTable');
    table.innerHTML = '';


    let header = '<tr><td></td>';
    for (let i = 1; i <= vertices; i++) {
        header += `<td>${i}</td>`;
    }
    header += '</tr>';
    table.innerHTML += header;


    for (let i = 0; i < vertices; i++) {
        let row = `<tr><td>${i + 1}</td>`;
        for (let j = 0; j < vertices; j++) {
            row += `<td><input type="number" name="edge_${i + 1}_${j + 1}" min="0" max="1" value="0"></td>`;
        }
        row += '</tr>';
        table.innerHTML += row;
    }
}

function resetForm() {
    document.getElementById('dfsForm').reset();

    updateMatrix();

    const graphPlot = document.querySelector('.graph-plot');
    if (graphPlot) {
        graphPlot.innerHTML = '<p>Graph will be displayed here after processing.</p>';
    }

    const treeMatrix = document.querySelector('.tree-matrix');
    if (treeMatrix) {
        treeMatrix.innerHTML = '';
    }
}
