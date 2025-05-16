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

function updateAdjacencyMatrixTable() {
    const numVerticesInput = document.getElementById('num_vertices');
    const table = document.getElementById('adjacencyMatrixTable');
    if (!numVerticesInput || !table) {
        console.error("Required elements (num_vertices or adjacencyMatrixTable) not found.");
        return;
    }

    let numVertices = parseInt(numVerticesInput.value);

    if (isNaN(numVertices) || numVertices < 1) {
        numVertices = 0;
    }

    table.innerHTML = '';

    if (numVertices === 0) return;

    let header = table.createTHead();
    let headerRow = header.insertRow(-1);
    let th = document.createElement('th');
    th.textContent = "V"; // Label for the corner
    headerRow.appendChild(th);
    for (let i = 0; i < numVertices; i++) {
        th = document.createElement('th');
        th.textContent = i;
        headerRow.appendChild(th);
    }

    let tbody = table.createTBody();
    for (let i = 0; i < numVertices; i++) {
        let row = tbody.insertRow(-1);
        let cellLabel = row.insertCell(-1);
        cellLabel.textContent = i;
        cellLabel.style.fontWeight = "bold";

        for (let j = 0; j < numVertices; j++) {
            let cell = row.insertCell(-1);
            let input = document.createElement('input');
            input.type = 'number';
            input.name = `edge_${i}_${j}`;
            input.min = "0";
            input.max = "1";
            input.value = "0";
            input.classList.add('input-field'); // Class from depth_method
            input.style.width = "40px";
            input.style.padding = "2px";
            if (i === j) {
                 input.value = "0";
                 input.readOnly = true; // Make diagonal cells read-only and 0
                 input.style.backgroundColor = "#f0f0f0"; // Visually indicate read-only
            }
            cell.appendChild(input);
        }
    }
}

function makeSymmetric() {
    const numVertices = parseInt(document.getElementById('num_vertices').value);
    if (isNaN(numVertices) || numVertices < 1) return;

    for (let i = 0; i < numVertices; i++) {
        for (let j = i + 1; j < numVertices; j++) { // Iterate only through the upper triangle (j > i)
            const input_ij = document.querySelector(`input[name="edge_${i}_${j}"]`);
            const input_ji = document.querySelector(`input[name="edge_${j}_${i}"]`);

            if (input_ij && input_ji) {
                // If either one is '1', make both '1'. Otherwise, both are '0'.
                if (input_ij.value === "1" || input_ji.value === "1") {
                    input_ij.value = "1";
                    input_ji.value = "1";
                } else {
                    // If both were '0' or one was '0' and other non-'1' (e.g. empty, invalid), set both to '0'
                    input_ij.value = "0";
                    input_ji.value = "0";
                }
            }
        }
    }
    // Ensure diagonal is 0 (already handled by readOnly, but good for explicit reset)
    for (let i = 0; i < numVertices; i++) {
        const input_ii = document.querySelector(`input[name="edge_${i}_${i}"]`);
        if (input_ii) {
            input_ii.value = "0";
        }
    }
}

function generateRandomValues() {
    const numVerticesInput = document.getElementById('num_vertices');
    if (!numVerticesInput) return;
    const numVertices = parseInt(numVerticesInput.value);

    if (isNaN(numVertices) || numVertices < 1) {
         alert("Please enter a valid number of vertices.");
        return;
    }

    // Ensure table is generated if it's not already
    const table = document.getElementById('adjacencyMatrixTable');
    if ((!table.tHead || table.tHead.rows.length === 0) && numVertices > 0) {
        updateAdjacencyMatrixTable();
    }


    for (let i = 0; i < numVertices; i++) {
        for (let j = 0; j < numVertices; j++) {
            const input = document.querySelector(`input[name="edge_${i}_${j}"]`);
            if (input) {
                if (i === j) {
                    input.value = "0";
                } else {
                    // Generate for upper triangle, then symmetrize
                    if (j > i) {
                        input.value = Math.round(Math.random());
                    }
                }
            }
        }
    }
    makeSymmetric(); // Call to make the randomly generated upper triangle symmetric
}

function validateAndSubmit() {
    const numVerticesInput = document.getElementById('num_vertices');
    if (!numVerticesInput) {
        alert("Number of vertices input not found!");
        return false;
    }
    const numVertices = parseInt(numVerticesInput.value);
    if (isNaN(numVertices) || numVertices < 1) {
        alert("Please enter a valid number of vertices (at least 1).");
        numVerticesInput.focus();
        return false;
    }

    for (let i = 0; i < numVertices; i++) {
        for (let j = 0; j < numVertices; j++) {
            const input_ij = document.querySelector(`input[name="edge_${i}_${j}"]`);
            if (!input_ij) {
                alert(`Matrix input edge_${i}_${j} not found. Please ensure the matrix is generated correctly.`);
                return false;
            }
            if (input_ij.value !== "0" && input_ij.value !== "1") {
                 alert(`Invalid value in adjacency matrix at (${i},${j}). Must be 0 or 1.`);
                 input_ij.focus();
                 return false;
            }
             if (i === j && input_ij.value !== "0") { // Self-loops must be 0
                alert(`Diagonal elements (self-loops) like at (${i},${j}) must be 0 for simple graph coloring.`);
                input_ij.value = "0";
                input_ij.focus();
                return false;
            }
            // Check for symmetry if desired before submission, though backend should handle it
            if (j > i) {
                const input_ji = document.querySelector(`input[name="edge_${j}_${i}"]`);
                if (input_ji && input_ij.value !== input_ji.value) {
                    alert(`Matrix is not symmetric at (${i},${j}) and (${j},${i}). Please use 'Make Symmetric' or correct manually.`);
                    input_ij.focus();
                    return false;
                }
            }
        }
    }
    return true; // Allow form submission
}


document.addEventListener('DOMContentLoaded', function() {
    updateAdjacencyMatrixTable(); // Initial table generation

    // Attempt to repopulate matrix from form_data if it exists (e.g., on page reload after POST)
    // This assumes 'form_data_json' is a script tag with JSON content rendered by the template
    const formDataJsonElement = document.getElementById('form_data_json');
    if (formDataJsonElement) {
        try {
            const formData = JSON.parse(formDataJsonElement.textContent);
            if (formData && formData.num_vertices) {
                 const numVertices = parseInt(formData.num_vertices);
                 const numVerticesInput = document.getElementById('num_vertices');
                 if(numVerticesInput && numVerticesInput.value != numVertices){ // Avoid re-render if value already correct
                    numVerticesInput.value = numVertices;
                    updateAdjacencyMatrixTable(); // Re-generate table if vertex count changed
                 }
            }
            if (formData && formData.adjacency_matrix && formData.adjacency_matrix.length > 0) {
                const matrixData = formData.adjacency_matrix;
                const currentNumVertices = parseInt(document.getElementById('num_vertices').value);
                if (matrixData.length === currentNumVertices) {
                    for (let i = 0; i < currentNumVertices; i++) {
                        for (let j = 0; j < currentNumVertices; j++) {
                            const inputElement = document.querySelector(`input[name="edge_${i}_${j}"]`);
                            if (inputElement && matrixData[i] && matrixData[i][j] !== undefined) {
                                inputElement.value = matrixData[i][j];
                            }
                        }
                    }
                }
            }
        } catch (e) {
            console.error("Error parsing or applying form_data_json:", e);
        }
    }
});