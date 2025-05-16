function toggleTheory() {
    const content = document.getElementById('theoryContent');
    content.style.display = content.style.display === 'none' ? 'block' : 'none';
}

function updateMatrixTables(n) {
    const adjacencyTable = document.getElementById('adjacency-table');
    const weightsTable = document.getElementById('weights-table');
    adjacencyTable.innerHTML = '';
    weightsTable.innerHTML = '';

    if (n >= 3) {
        for (let i = 0; i < n; i++) {
            let adjRow = document.createElement('tr');
            let weightRow = document.createElement('tr');

            for (let j = 0; j < n; j++) {
                let adjCell = document.createElement('td');
                let adjInput = document.createElement('input');
                adjInput.type = 'number';
                adjInput.name = `adjacency_${i}_${j}`;
                adjInput.min = '0';
                adjInput.max = '1';
                adjInput.required = true;
                adjCell.appendChild(adjInput);
                adjRow.appendChild(adjCell);

                let weightCell = document.createElement('td');
                let weightInput = document.createElement('input');
                weightInput.type = 'number';
                weightInput.name = `weights_${i}_${j}`;
                weightInput.min = '0';
                weightInput.required = true;
                weightCell.appendChild(weightInput);
                weightRow.appendChild(weightCell);
            }

            adjacencyTable.appendChild(adjRow);
            weightsTable.appendChild(weightRow);
        }
    }
}

function generateRandomMatrices() {
    const n = parseInt(document.getElementById('n-vertices').value);
    if (isNaN(n) || n < 3) {
        alert('Please enter a valid number of vertices (at least 3).');
        return;
    }
    updateMatrixTables(n);

    for (let i = 0; i < n; i++) {
        for (let j = 0; j < n; j++) {
            document.querySelector(`input[name="adjacency_${i}_${j}"]`).value = Math.floor(Math.random() * 2);
            document.querySelector(`input[name="weights_${i}_${j}"]`).value = Math.floor(Math.random() * 11);
        }
    }
}

function clearFields() {
    document.getElementById('matrix-form').reset();
    updateMatrixTables(0);
}

document.getElementById('n-vertices').addEventListener('input', function () {
    const n = parseInt(this.value);
    if (!isNaN(n) && n >= 3) {
        updateMatrixTables(n);
    } else {
        updateMatrixTables(0);
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const n = parseInt(document.getElementById('n-vertices').value);
    const adjInputs = document.querySelectorAll('input[name^="adjacency_"]');
    const weightInputs = document.querySelectorAll('input[name^="weights_"]');
    if ((adjInputs.length === 0 || weightInputs.length === 0) && !isNaN(n) && n >= 3) {
        updateMatrixTables(n);
    }
});