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
        numVertices = 0; // Clear table if input is invalid
    }

    table.innerHTML = ''; // Clear existing table

    if (numVertices === 0) return;

    // Create table header (optional, but good for clarity)
    let header = table.createTHead();
    let headerRow = header.insertRow(-1);
    let th = document.createElement('th');
    headerRow.appendChild(th); // Empty top-left cell
    for (let i = 0; i < numVertices; i++) {
        th = document.createElement('th');
        th.textContent = i;
        headerRow.appendChild(th);
    }

    // Create table body
    let tbody = table.createTBody();
    for (let i = 0; i < numVertices; i++) {
        let row = tbody.insertRow(-1);
        let cellLabel = row.insertCell(-1);
        cellLabel.textContent = i; // Row label

        for (let j = 0; j < numVertices; j++) {
            let cell = row.insertCell(-1);
            let input = document.createElement('input');
            input.type = 'number';
            input.name = `edge_${i}_${j}`;
            input.min = "0";
            input.max = "1";
            input.value = "0"; // Default value
            input.classList.add('input-field'); // From depth_method for style
            input.style.width = "40px"; // Compact size
            input.style.padding = "2px";
            if (i === j) { // Optional: disable self-loops or set to 0
                 input.value = "0";
                 // input.disabled = true;
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
                if (input_ij.value !== input_ji.value) {
                    // Prefer 1 if there's a mismatch, or make them both 0 or 1 based on one of them
                    // Here, we set ji to ij's value.
                    input_ji.value = input_ij.value;
                }
            }
        }
    }
     // Ensure diagonal is 0
    for (let i = 0; i < numVertices; i++) {
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

    // Call update to ensure table exists if it was cleared or not initialized
    if (document.getElementById('adjacencyMatrixTable').rows.length === 0 && numVertices > 0) {
        updateAdjacencyMatrixTable();
    }


    for (let i = 0; i < numVertices; i++) {
        for (let j = 0; j < numVertices; j++) {
            const input = document.querySelector(`input[name="edge_${i}_${j}"]`);
            if (input) {
                if (i === j) {
                    input.value = "0"; // No self-loops
                } else {
                    input.value = Math.round(Math.random()); // Random 0 or 1
                }
            }
        }
    }
    makeSymmetric(); // Ensure the random matrix is symmetric
}

function colorGraph() {
    // This function is now primarily for validation or AJAX submission if you choose that route.
    // For simple form submission, the "Color Graph" button can be type="submit".
    // If client-side validation is needed before submit:
    const numVertices = parseInt(document.getElementById('num_vertices').value);
    if (isNaN(numVertices) || numVertices < 1) {
        alert("Please enter a valid number of vertices (at least 1).");
        return false; // Prevent form submission
    }
    for (let i = 0; i < numVertices; i++) {
        for (let j = 0; j < numVertices; j++) {
            const input_ij = document.querySelector(`input[name="edge_${i}_${j}"]`);
            if (input_ij && (input_ij.value !== "0" && input_ij.value !== "1")) {
                 alert(`Invalid value in adjacency matrix at (${i},${j}). Must be 0 or 1.`);
                 return false;
            }
        }
    }
    // If validation passes, the form will be submitted by the actual submit button
    document.getElementById('graphForm').submit();
}

function internalSubmit() {
    // This is called by the "Submit Adjacency Matrix" button
    // It can perform final client-side checks before actual form submission if needed
    const numVertices = parseInt(document.getElementById('num_vertices').value);
    if (isNaN(numVertices) || numVertices < 1) {
        alert("Please enter a valid number of vertices (at least 1).");
        return false; // Prevent form submission
    }
     for (let i = 0; i < numVertices; i++) {
        for (let j = 0; j < numVertices; j++) {
            const input_ij = document.querySelector(`input[name="edge_${i}_${j}"]`);
            if (input_ij && (input_ij.value !== "0" && input_ij.value !== "1")) {
                 alert(`Invalid value in adjacency matrix at (${i},${j}). Must be 0 or 1.`);
                 return false;
            }
             if (i === j && input_ij.value !== "0") {
                alert(`Diagonal elements (self-loops) like at (${i},${j}) must be 0 for simple graph coloring.`);
                input_ij.value = "0"; // Correct it
                // return false; // Or prevent submission
            }
        }
    }
    // Optional: If "Make Symmetric" wasn't pressed, you could enforce it here
    // makeSymmetric();
    return true; // Allow form submission
}


// Initialize table on page load
document.addEventListener('DOMContentLoaded', function() {
    updateAdjacencyMatrixTable();

    // If form_data is available (e.g., after a POST request with errors or results),
    // try to repopulate the matrix. The form_data needs to be exposed to JS.
    // This part is a bit tricky without knowing exactly how your Bottle template passes complex data to JS.
    // For now, we assume the Bottle template directly renders values if form_data.adjacency_matrix exists.
    // Or, you'd embed it as a JSON string and parse it here.

    // Example of how you might repopulate if form_data was a global JS object:
    /*
    if (typeof window.form_data_js !== 'undefined' && window.form_data_js.adjacency_matrix) {
        const matrix = window.form_data_js.adjacency_matrix;
        const numVertices = parseInt(document.getElementById('num_vertices').value);
        if (matrix.length === numVertices) {
            for (let i = 0; i < numVertices; i++) {
                for (let j = 0; j < numVertices; j++) {
                    const inputElement = document.querySelector(`input[name="edge_${i}_${j}"]`);
                    if (inputElement && matrix[i] && matrix[i][j] !== undefined) {
                        inputElement.value = matrix[i][j];
                    }
                }
            }
        }
    }
    */
});