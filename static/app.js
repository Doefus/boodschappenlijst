document.addEventListener('DOMContentLoaded', function() {
    loadItems();
});

document.getElementById('textForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const text = document.getElementById('textInput').value;

    fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ textInput: text })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
        loadItems();  // Update the list after submitting a new item
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});

function loadItems() {
    fetch('/items', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        const itemsList = document.getElementById('itemsList');
        itemsList.innerHTML = '';  // Clear the current list

        data.forEach(item => {
            const row = document.createElement('tr');

            const itemCell = document.createElement('td');
            itemCell.textContent = item[1];
            row.appendChild(itemCell);

            const dateCell = document.createElement('td');
            dateCell.textContent = new Date(item[2]).toLocaleString();
            row.appendChild(dateCell);

            const actionCell = document.createElement('td');
            const deleteButton = document.createElement('button');
            deleteButton.textContent = '🗑️';
            deleteButton.addEventListener('click', function() {
                deleteItem(item[0]);
            });
            actionCell.appendChild(deleteButton);
            row.appendChild(actionCell);

            itemsList.appendChild(row);
        });
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function deleteItem(itemId) {
    fetch('/delete_item', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ item_id: itemId })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
        loadItems();  // Update the list after deleting an item
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
