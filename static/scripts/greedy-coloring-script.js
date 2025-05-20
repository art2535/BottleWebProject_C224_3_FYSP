// static/scripts/greedy_coloring_script.js

// Toggles the display of the theory section and rotates the arrow icon accordingly
function toggleTheory() {
    const container = document.querySelector(".theory-container");
    const content = document.getElementById("theoryContent");
    if (container && content) {
        const isOpen = container.classList.toggle("open");
        content.style.display = isOpen ? "block" : "none";
        const arrow = container.nextElementSibling.querySelector(".arrow");
        if (arrow) {
            arrow.style.transform = isOpen ? "rotate(180deg)" : "rotate(0deg)";
        }
    }
}

// Rebuilds the adjacency matrix table based on the selected number of vertices
function updateAdjacencyMatrixTable() {
    const numVertices = parseInt(document.getElementById('num_vertices').value) || 0;
    const table = document.getElementById('adjacencyMatrixTable');
    table.innerHTML = '';
    if (numVertices < 1) return;

    // Create table header row
    const thead = table.createTHead();
    const headerRow = thead.insertRow(-1);
    let cell = document.createElement('td');
    cell.classList.add('matrix-header');
    cell.textContent = '';
    headerRow.appendChild(cell);
    for (let j = 0; j < numVertices; j++) {
        cell = document.createElement('td');
        cell.classList.add('matrix-header');
        cell.textContent = j + 1;
        headerRow.appendChild(cell);
    }

    // Create table body with input fields
    const tbody = table.createTBody();
    for (let i = 0; i < numVertices; i++) {
        const row = tbody.insertRow(-1);
        const rowHeader = document.createElement('td');
        rowHeader.classList.add('matrix-header');
        rowHeader.textContent = i + 1;
        row.appendChild(rowHeader);

        for (let j = 0; j < numVertices; j++) {
            const cell = row.insertCell(-1);
            const input = document.createElement('input');
            input.type = 'number';
            input.name = `edge_${i}_${j}`;
            input.min = "0";
            input.max = "1";
            input.value = "0";
            input.classList.add('matrix-input');
            if (i === j) {
                // Disable diagonal inputs (self-loops not allowed)
                input.readOnly = true;
                input.style.backgroundColor = "#f0f0f0";
            }
            cell.appendChild(input);
        }
    }
}

// Fills the adjacency matrix with random symmetric 0/1 values
function generateRandomValues() {
    const numVertices = parseInt(document.getElementById('num_vertices').value);
    if (isNaN(numVertices) || numVertices < 1) {
        alert("Please enter a valid number of vertices.");
        return;
    }
    const table = document.getElementById('adjacencyMatrixTable');
    if (!table.tHead || table.tHead.rows.length === 0) {
        updateAdjacencyMatrixTable();
    }
    for (let i = 0; i < numVertices; i++) {
        for (let j = i + 1; j < numVertices; j++) {
            const rand = Math.round(Math.random());
            const inp1 = document.querySelector(`input[name="edge_${i}_${j}"]`);
            const inp2 = document.querySelector(`input[name="edge_${j}_${i}"]`);
            if (inp1 && inp2) {
                inp1.value = rand;
                inp2.value = rand;
            }
        }
        // Ensure diagonal remains zero
        const dia = document.querySelector(`input[name="edge_${i}_${i}"]`);
        if (dia) dia.value = "0";
    }
}

// Resets the graph matrix to default values based on the current vertex count
function resetGraph() {
    updateAdjacencyMatrixTable();
}

// Validates form inputs before submission: number of vertices, matrix values, symmetry, and diagonal
function validateAndSubmit() {
    const numVertices = parseInt(document.getElementById('num_vertices').value);
    if (isNaN(numVertices) || numVertices < 1) {
        alert("Please enter a valid number of vertices (1–8).");
        return false;
    }
    for (let i = 0; i < numVertices; i++) {
        for (let j = 0; j < numVertices; j++) {
            const inp = document.querySelector(`input[name="edge_${i}_${j}"]`);
            if (!inp) {
                alert(`Missing input at (${i},${j}).`);
                return false;
            }
            if (inp.value !== "0" && inp.value !== "1") {
                alert(`Invalid value at (${i+1},${j+1}). Must be 0 or 1.`);
                inp.focus();
                return false;
            }
            if (i === j && inp.value !== "0") {
                alert(`Diagonal (${i+1},${j+1}) must be 0.`);
                inp.value = "0";
                inp.focus();
                return false;
            }
            if (j > i) {
                const inp2 = document.querySelector(`input[name="edge_${j}_${i}"]`);
                if (inp2 && inp.value !== inp2.value) {
                    alert(`Matrix not symmetric at (${i+1},${j+1}) and (${j+1},${i+1}).`);
                    return false;
                }
            }
        }
    }
    return true;
}

// Executes on page load: builds matrix table and restores previous form data if available
document.addEventListener('DOMContentLoaded', function() {
    updateAdjacencyMatrixTable();

    const dataElem = document.getElementById('form_data_json');
    if (dataElem) {
        try {
            const formData = JSON.parse(dataElem.textContent);
            if (formData.num_vertices) {
                const nv = parseInt(formData.num_vertices);
                const inp = document.getElementById('num_vertices');
                if (inp && parseInt(inp.value) !== nv) {
                    inp.value = nv;
                    updateAdjacencyMatrixTable();
                }
            }
            if (formData.adjacency_matrix) {
                const mat = formData.adjacency_matrix;
                for (let i = 0; i < mat.length; i++) {
                    for (let j = 0; j < mat.length; j++) {
                        const inp = document.querySelector(`input[name="edge_${i}_${j}"]`);
                        if (inp && mat[i][j] !== undefined) {
                            inp.value = mat[i][j];
                        }
                    }
                }
            }
        } catch (e) {
            console.error("Error parsing form_data_json:", e);
        }
    }
});
