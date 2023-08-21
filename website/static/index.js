function addDeleteButtons() {
    // Get all the rows in the table
    let rows = document.querySelectorAll('tbody tr');
    rows.forEach(row => {// Loop through each row
        let deleteButton = document.createElement('button');// Create a new delete button
        deleteButton.innerHTML = 'Delete';
        deleteButton.classList.add('btn', 'btn-danger', 'btn-sm');
        deleteButton.addEventListener('click', () => {// Add an event listener to the delete button     
            let transactionId = row.id.split('-')[1];// Get the transaction ID from the row ID
            fetch('/delete-transaction', {// Send a DELETE request to the server
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ transactionId: transactionId })
            }).then(response => {
                if (response.ok) {
                    
                    row.remove();// Remove the row from the table
                }
            });
        });
        
        row.lastElementChild.appendChild(deleteButton);// Append the delete button to the last cell in the row
    });
}