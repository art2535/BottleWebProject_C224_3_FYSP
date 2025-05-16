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

        for (let j = 0; j < numVertices; j++) {
            let cell = row.insertCell(-1);
            let input = document.createElement('input');
            input.type = 'number';
            input.name = `edge_${i}_${j}`;
            input.min = "0";
            input.max = "1";
            input.value = "0";
            input.classList.add('input-field');
            input.style.width = "40px";
            input.style.padding = "2px";
            if (i === j) {
                 input.value = "0";
                 // input.readOnly = true; // Make diagonal cells read-only and 0
            }
            cell.appendChild(input);
        }
    }
}

function makeSymmetric() {
    const numVertices = parseInt(document.getElementById('num_vertices').value);
    if (isNaN(numVertices) || numVertices < 1) return;

    for (let i = 0; i < numVertices; i++) {
        for (let j = i + 1; j < numVertices; j++) {
            const input_ij = document.querySelector(`input[name="edge_${i}_${j}"]`);
            const input_ji = document.querySelector(`input[name="edge_${j}_${i}"]`);
            if (input_ij && input_ji) {
                // If one is changed, make the other the same.
                // Prioritize the one being changed if we could detect that,
                // otherwise, just pick one (e.g. input_ij.value)
                if (input_ij.value !== input_ji.value) {
                     input_ji.value = input_ij.value; // Or vice versa, or average, or set to 0/1 based on a rule
                }
            }
        }
    }
    for (let i = 0; i < numVertices; i++) { // Ensure diagonal is 0
        const input_ii = document.querySelector(`input[name="edge_${i}_${i}"]`);
        if (input_ii) {
            input_ii.value = "0";
        }
    }
}

function generateRandomValues() {
    const numVertices = parseInt(document.getElementById('num_vertices').value);
    if (isNaN(numVertices) || numVertices < 1) {
         alert("Please enter a valid number of vertices.");
        return;
    }

    if (document.getElementById('adjacencyMatrixTable').rows.length === 0 && numVertices > 0) {
        updateAdjacencyMatrixTable();
    }

    for (let i = 0; i < numVertices; i++) {
        for (let j = 0; j < numVertices; j++) {
            const input = document.querySelector(`input[name="edge_${i}_${j}"]`);
            if (input) {
                if (i === j) {
                    input.value = "0";
                } else {
                    input.value = Math.round(Math.random());
                }
            }
        }
    }
    makeSymmetric();
}

// Renamed from colorGraph to be more generic for form submission validation
function validateAndSubmit() {
    const numVerticesInput = document.getElementById('num_vertices');
    if (!numVerticesInput) {
        alert("Number of vertices input not found!");
        return false;
    }
    const numVertices = parseInt(numVerticesInput.value);
    if (isNaN(numVertices) || numVertices < 1) {
        alert("Please enter a valid number of vertices (at least 1).");
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
             if (i === j && input_ij.value !== "0") {
                alert(`Diagonal elements (self-loops) like at (${i},${j}) must be 0 for simple graph coloring.`);
                input_ij.value = "0";
                input_ij.focus();
                return false; // Or just correct and allow submission
            }
        }
    }
    // If all validations pass, the form will submit due to type="submit"
    return true;
}


document.addEventListener('DOMContentLoaded', function() {
    updateAdjacencyMatrixTable();

    // Repopulate matrix from form_data if it exists (e.g., on page reload after POST)
    // This requires form_data.adjacency_matrix to be available in a way JS can access.
    // For simplicity, we assume Bottle template might directly set values in input fields
    // if form_data was passed back. If not, this part can be enhanced.
    const adjMatrixDataElement = document.getElementById('adjacencyMatrixData');
    if (adjMatrixDataElement) {
        try {
            const matrixData = JSON.parse(adjMatrixDataElement.textContent);
            if (matrixData && matrixData.length > 0) {
                const numVertices = matrixData.length;
                document.getElementById('num_vertices').value = numVertices; // Set vertex count
                updateAdjacencyMatrixTable(); // Regenerate table based on count

                for (let i = 0; i < numVertices; i++) {
                    for (let j = 0; j < numVertices; j++) {
                        const inputElement = document.querySelector(`input[name="edge_${i}_${j}"]`);
                        if (inputElement && matrixData[i] && matrixData[i][j] !== undefined) {
                            inputElement.value = matrixData[i][j];
                        }
                    }
                }
            }
        } catch (e) {
            console.error("Error parsing adjacency matrix data for repopulation:", e);
        }
    }
});