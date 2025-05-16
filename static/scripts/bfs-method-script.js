// static/scripts/bfs-method-script.js
function toggleTheory() {
    const content = document.getElementById('theoryContent');
    const arrow = document.querySelector('.arrow');
    content.style.display = content.style.display === 'none' ? 'block' : 'none';
    arrow.textContent = content.style.display === 'none' ? '▼' : '▲';
}

function updateMatrixTable(n) {
    const adjacencyTable = document.getElementById('adjacency-table');
    adjacencyTable.innerHTML = '';

    if (n >= 1) {
        // Create header row
        let headerRow = document.createElement('tr');
        headerRow.innerHTML = '<td></td>';
        for (let j = 0; j < n; j++) {
            headerRow.innerHTML += `<td>${j}</td>`;
        }
        adjacencyTable.appendChild(headerRow);

        // Create matrix rows
        for (let i = 0; i < n; i++) {
            let row = document.createElement('tr');
            row.innerHTML = `<td>${i}</td>`;
            for (let j = 0; j < n; j++) {
                let cell = document.createElement('td');
                let input = document.createElement('input');
                input.type = 'number';
                input.name = `edge_${i}_${j}`;
                input.min = '0';
                input.max = '1';
                input.value = '0';
                input.required = true;
                cell.appendChild(input);
                row.appendChild(cell);
            }
            adjacencyTable.appendChild(row);
        }
    }
}

function generateRandomMatrix() {
    const n = parseInt(document.getElementById('num_vertices').value);
    if (isNaN(n) || n < 1) {
        alert('Please enter a valid number of vertices (at least 1).');
        return;
    }
    updateMatrixTable(n);

    // Use setTimeout to ensure DOM is updated before filling values
    setTimeout(() => {
        for (let i = 0; i < n; i++) {
            for (let j = i; j < n; j++) {
                const value = i === j ? 0 : Math.floor(Math.random() * 2);
                document.querySelector(`input[name="edge_${i}_${j}"]`).value = value;
                document.querySelector(`input[name="edge_${j}_${i}"]`).value = value;
            }
        }
    }, 0);
}


function clearFields() {
    document.getElementById('matrix-form').reset();
    document.getElementById('num_vertices').value = '3';
    document.getElementById('start_vertex').value = '0';
    updateMatrixTable(3);
}

document.getElementById('num_vertices').addEventListener('input', function () {
    const n = parseInt(this.value);
    if (!isNaN(n) && n >= 1) {
        updateMatrixTable(n);
    } else {
        updateMatrixTable(0);
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const n = parseInt(document.getElementById('num_vertices').value) || 3;
    updateMatrixTable(n);
});