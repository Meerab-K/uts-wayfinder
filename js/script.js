document.getElementById('find_path_form').addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent the form submission from reloading the page

    const startPoint = document.getElementById('start_point_select').value;
    const destination = document.getElementById('destination_select').value;

    const container = document.getElementById('path_result');

    container.innerHTML = '<p>Finding path from ' + startPoint + ' to ' + destination + '...</p>';

    // Call the python backend to find the path
    const response = await fetch('/find_path', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ start: startPoint, goal: destination })
    });

    const result = await response.json();
    if (result.path) {
        container.innerHTML = '<p>Path found: ' + result.path.join(' -> ') + '</p>';
    } else {
        container.innerHTML = '<p>No path found.</p>';
    }

    // Display generated map image
    if (result.map_image) {
        const img = document.createElement('img');
        img.src = 'data:image/png;base64,' + result.map_image;
        container.appendChild(img);
    }
})