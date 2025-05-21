function toggleTheory() {
    // Toggle the visibility of the theory explanation block
    const container = document.querySelector(".theory-container");
    const content = document.getElementById("theoryContent");
    if (container && content) {
        const isOpen = container.classList.toggle("open");
        content.style.display = isOpen ? "block" : "none";

        // Rotate the arrow icon depending on open state
        const arrow = container.nextElementSibling.querySelector(".arrow");
        if (arrow) {
            arrow.style.transform = isOpen ? "rotate(180deg)" : "rotate(0deg)";
        }
    }
}

function updateAdjacencyMatrixTable() {
    // Dynamically rebuild the adjacency matrix table based on number of vertices
    const numVertices = parseInt(document.getElementById('num_vertices').value) || 0;
    const table = document.getElementById('adjacencyMatrixTable');
    table.innerHTML = '';
    if (numVertices < 1) return;

    // Create table header row
    const thead = table.createTHead();
    const headerRow = thead.insertRow(-1);
    let cell = document.createElement('td');
    cell.classList.add('matrix-header');
    headerRow.appendChild(cell); // Empty top-left corner

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

        // Row header with vertex number
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

            // Disable diagonal (no self-loops allowed)
            if (i === j) {
                input.readOnly = true;
                input.style.backgroundColor = "#f0f0f0";
            }

            cell.appendChild(input);
        }
    }
}

function generateRandomValues() {
    // Fill the adjacency matrix with a random connected undirected graph
    const numVertices = parseInt(document.getElementById('num_vertices').value);
    if (isNaN(numVertices) || numVertices < 2) {
        alert("Please enter a valid number of vertices.");
        return;
    }

    updateAdjacencyMatrixTable();

    // First, create a random spanning tree to ensure connectivity
    const edges = [];
    const nodes = Array.from({length: numVertices}, (_, i) => i);

    // Shuffle nodes
    for (let i = nodes.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [nodes[i], nodes[j]] = [nodes[j], nodes[i]];
    }

    // Add an edge from each node to a random previous node to form a tree
    for (let k = 1; k < nodes.length; k++) {
        const u = nodes[k];
        const v = nodes[Math.floor(Math.random() * k)];
        edges.push([u, v]);
    }

    // Mark the spanning tree edges in the matrix
    edges.forEach(([i, j]) => {
        const inp1 = document.querySelector(`input[name="edge_${i}_${j}"]`);
        const inp2 = document.querySelector(`input[name="edge_${j}_${i}"]`);
        if (inp1 && inp2) {
            inp1.value = "1";
            inp2.value = "1";
        }
    });

    // Add additional random edges to the rest of the matrix
    for (let i = 0; i < numVertices; i++) {
        for (let j = i + 1; j < numVertices; j++) {
            // Skip edges already added
            if (edges.some(e => (e[0] === i && e[1] === j) || (e[0] === j && e[1] === i))) continue;

            const rand = Math.round(Math.random());
            const inp1 = document.querySelector(`input[name="edge_${i}_${j}"]`);
            const inp2 = document.querySelector(`input[name="edge_${j}_${i}"]`);
            if (inp1 && inp2) {
                inp1.value = rand;
                inp2.value = rand;
            }
        }

        // Set diagonal to 0 (no self-loops)
        const dia = document.querySelector(`input[name="edge_${i}_${i}"]`);
        if (dia) dia.value = "0";
    }
}

function resetGraph() {
    // Reset matrix inputs to default (all zeros except diagonal)
    updateAdjacencyMatrixTable();
}

function validateAndSubmit() {
    // Validate matrix before form submission
    const numVertices = parseInt(document.getElementById('num_vertices').value);
    if (isNaN(numVertices) || numVertices < 2) {
        alert("Please enter a valid number of vertices (2–8).");
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
                // Ensure matrix is symmetric
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

document.addEventListener('DOMContentLoaded', function() {
    // Initialize matrix on page load
    updateAdjacencyMatrixTable();

    // If form_data_json is embedded, restore previous form state
    const dataElem = document.getElementById('form_data_json');
    if (dataElem) {
        try {
            const formData = JSON.parse(dataElem.textContent);
            const nv = parseInt(formData.num_vertices);
            if (!isNaN(nv)) {
                const inp = document.getElementById('num_vertices');
                inp.value = nv;
                updateAdjacencyMatrixTable();
            }

            if (Array.isArray(formData.adjacency_matrix)) {
                formData.adjacency_matrix.forEach((row, i) => {
                    row.forEach((val, j) => {
                        const inp = document.querySelector(`input[name="edge_${i}_${j}"]`);
                        if (inp) inp.value = val;
                    });
                });
            }
        } catch (e) {
            console.error("Error parsing form_data_json:", e);
        }
    }
});
