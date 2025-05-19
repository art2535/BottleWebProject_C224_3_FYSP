// Function to toggle the display of the theory block
function toggleTheory() {
    const content = document.getElementById('theoryContent');
    content.style.display = content.style.display === 'none' ? 'block' : 'none';
}

// Function to dynamically update adjacency and weight tables
function updateMatrixTables(n, preserveValues = false) {
    const adjacencyTable = document.getElementById('adjacency-table');
    const weightsTable = document.getElementById('weights-table');

    // Collect existing values if preserving
    let oldAdjacency = [];
    let oldWeights = [];
    if (preserveValues) {
        for (let i = 0; i < n; i++) {
            oldAdjacency[i] = [];
            oldWeights[i] = [];
            for (let j = 0; j < n; j++) {
                const adjInput = document.querySelector(`input[name="adjacency_${i}_${j}"]`);
                const weightInput = document.querySelector(`input[name="weights_${i}_${j}"]`);
                oldAdjacency[i][j] = adjInput ? parseInt(adjInput.value) || 0 : 0;
                oldWeights[i][j] = weightInput ? parseInt(weightInput.value) || 0 : 0;
            }
        }
    }

    // Clear existing tables
    adjacencyTable.innerHTML = '';
    weightsTable.innerHTML = '';

    // Check if n is within the valid range (3–7)
    if (n >= 3 && n <= 7) {
        // Create header rows (horizontal numbering)
        let headerRowAdj = document.createElement('tr');
        let headerRowWgt = document.createElement('tr');
        let emptyCornerAdj = document.createElement('td');
        let emptyCornerWgt = document.createElement('td');
        emptyCornerAdj.className = 'matrix-header';
        emptyCornerWgt.className = 'matrix-header';
        headerRowAdj.appendChild(emptyCornerAdj); // Empty corner cell
        headerRowWgt.appendChild(emptyCornerWgt);
        for (let j = 0; j < n; j++) {
            let tdAdj = document.createElement('td');
            let tdWgt = document.createElement('td');
            tdAdj.className = 'matrix-header';
            tdWgt.className = 'matrix-header';
            tdAdj.textContent = j + 1;
            tdWgt.textContent = j + 1;
            headerRowAdj.appendChild(tdAdj);
            headerRowWgt.appendChild(tdWgt);
        }
        adjacencyTable.appendChild(headerRowAdj);
        weightsTable.appendChild(headerRowWgt);

        // Create rows with vertical numbering
        for (let i = 0; i < n; i++) {
            let adjRow = document.createElement('tr');
            let weightRow = document.createElement('tr');
            let tdAdj = document.createElement('td');
            let tdWgt = document.createElement('td');
            tdAdj.className = 'matrix-header';
            tdWgt.className = 'matrix-header';
            tdAdj.textContent = i + 1;
            tdWgt.textContent = i + 1;
            adjRow.appendChild(tdAdj);
            weightRow.appendChild(tdWgt);

            for (let j = 0; j < n; j++) {
                // Adjacency matrix
                let adjCell = document.createElement('td');
                let adjInput = document.createElement('input');
                adjInput.type = 'number';
                adjInput.name = `adjacency_${i}_${j}`;
                adjInput.min = '0';
                adjInput.max = '1';
                adjInput.required = true;
                adjInput.value = preserveValues && oldAdjacency[i] ? oldAdjacency[i][j] : '0';
                adjCell.appendChild(adjInput);
                adjRow.appendChild(adjCell);

                // Weight matrix
                let weightCell = document.createElement('td');
                let weightInput = document.createElement('input');
                weightInput.type = 'number';
                weightInput.name = `weights_${i}_${j}`;
                weightInput.min = '0';
                weightInput.max = '100';
                weightInput.required = true;
                weightInput.value = preserveValues && oldWeights[i] ? oldWeights[i][j] : '0';
                weightCell.appendChild(weightInput);
                weightRow.appendChild(weightCell);
            }
            adjacencyTable.appendChild(adjRow);
            weightsTable.appendChild(weightRow);
        }
    }
}

// Generate random values for adjacency and weight matrices
function generateRandomMatrices() {
    const n = parseInt(document.getElementById('n-vertices').value);
    if (isNaN(n) || n < 3 || n > 7) {
        alert('Please enter a valid number of vertices (from 3 to 7).');
        return;
    }

    updateMatrixTables(n, true); // Preserve existing values before randomizing
    for (let i = 0; i < n; i++) {
        for (let j = 0; j < n; j++) {
            document.querySelector(`input[name="adjacency_${i}_${j}"]`).value = Math.floor(Math.random() * 2);
            document.querySelector(`input[name="weights_${i}_${j}"]`).value = Math.floor(Math.random() * 10);
        }
    }
}

// Clear the form fields and reset the result card
function clearFields() {
    const n = parseInt(document.getElementById('n-vertices').value) || 3;
    // Clear matrix input fields
    for (let i = 0; i < n; i++) {
        for (let j = 0; j < n; j++) {
            const adjInput = document.querySelector(`input[name="adjacency_${i}_${j}"]`);
            const weightInput = document.querySelector(`input[name="weights_${i}_${j}"]`);
            if (adjInput) adjInput.value = '0';
            if (weightInput) weightInput.value = '0';
        }
    }
    // Clear the graph and result card
    const graphCard = document.querySelector('.graph-card');
    graphCard.innerHTML = `
        <h3>Graph and Result</h3>
        <p class="placeholder">Enter parameters and click "Build Spanning Tree" to see results.</p>
    `;
}

// Listener to update tables when the number of vertices changes
document.getElementById('n-vertices').addEventListener('input', function () {
    const n = parseInt(this.value);
    if (!isNaN(n) && n >= 3 && n <= 7) {
        updateMatrixTables(n, true); // Preserve values when updating
    } else {
        this.value = 3;
        updateMatrixTables(3, true);
    }
});

// Initialization on page load
document.addEventListener('DOMContentLoaded', function () {
    const n = parseInt(document.getElementById('n-vertices').value) || 3;
    // Only update tables if no server-side data exists
    const hasServerData = document.querySelectorAll('input[name^="adjacency_"]').length > 0;
    if (!hasServerData) {
        updateMatrixTables(n);
    }
});