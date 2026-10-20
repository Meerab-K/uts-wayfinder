document.getElementById('find_path_form').addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent the form submission from reloading the page

    const startPoint = document.getElementById('start_point_select').value;
    const destination = document.getElementById('destination_select').value;

    const container = document.getElementById('path_result');

    container.innerHTML = '<p>Finding path from ' + startPoint + ' to ' + destination + '...</p>';

    // Call the backend api to run the A* algorithm

    
})