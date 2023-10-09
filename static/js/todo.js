function deleteTodo(todoId) {
    if (confirm("Are you sure you want to delete this to-do item?")) {
        // Make an AJAX request to delete the to-do item
        fetch(`/delete_todo/${todoId}`, {
            method: 'GET'
        })
            .then(response => {
                if (response.ok) {
                    // Reload the page to update the to-do list
                    window.location.reload();
                } else {
                    alert("Failed to delete the to-do item.");
                }
            })
            .catch(error => {
                console.error("Error:", error);
            });
    }
}