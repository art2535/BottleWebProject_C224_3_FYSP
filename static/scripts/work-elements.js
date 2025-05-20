// Function to display the tree matrix section.
function buildGraph() {
    document.getElementById('treeMatrix').style.display = 'block';
}

// Function to toggle the visibility of the theory section.
function toggleTheory() {
    const container = document.querySelector(".theory-container");
    const content = document.getElementById("theoryContent");
    // Toggle the "open" class on the container and adjust content visibility.
    const isOpen = container.classList.toggle("open");
    content.style.display = isOpen ? "block" : "none";
}

// Function to update the matrix based on the number of vertices.
function updateMatrix() {
    // Parse the number of vertices, default to 3 if invalid.
    const vertices = parseInt(document.getElementById('vertices').value) || 3;

    // Ensure the number of vertices is between 1 and 8.
    if (vertices < 1 || vertices > 8) return;

    const table = document.getElementById('matrixTable');
    table.innerHTML = ''; // Clear any previous table content.

    // Create the table header based on the number of vertices.
    let header = '<tr><td class="matrix-header"></td>';
    for (let i = 1; i <= vertices; i++) {
        header += `<td class="matrix-header">${i}</td>`;
    }
    header += '</tr>';
    table.innerHTML += header;

    // Create the matrix rows for the edges between vertices.
    for (let i = 0; i < vertices; i++) {
        let row = `<tr><td class="matrix-header">${i + 1}</td>`;
        for (let j = 0; j < vertices; j++) {
            row += `<td><input type="number" name="edge_${i + 1}_${j + 1}" min="0" max="1" value="0"></td>`;
        }
        row += '</tr>';
        table.innerHTML += row;
    }
}

// Function to reset the form and matrix to their initial state.
function resetForm() {
    // Reset the form inputs to their default values.
    document.getElementById('dfsForm').reset();

    // Update the matrix after form reset.
    updateMatrix();

    // Reset the graph plot area with a placeholder text.
    const graphPlot = document.querySelector('.graph-plot');
    if (graphPlot) {
        graphPlot.innerHTML = '<p>Graph will be displayed here after processing.</p>';
    }

    // Clear the tree matrix area.
    const treeMatrix = document.querySelector('.tree-matrix');
    if (treeMatrix) {
        treeMatrix.innerHTML = '';
    }
}