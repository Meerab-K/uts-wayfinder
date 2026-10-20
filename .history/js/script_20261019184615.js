document.getElementById('find_path_form').addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent the form submission from reloading the page

    const startPoint = document.getElementById('start_point_select').value;
    const destination = document.getElementById('destination_select').value;

    const container = document.getElementById('path_result');

    container.innerHTML = '<p>Finding path from ' + startPoint + ' to ' + destination + '...</p>';

    // Call the backend api to run the A* algorithm
    try {
        const response = await fetch('http://127.0.0.1:8000/route', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                start: startPoint,
                goal: destination
            })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const result = await response.json();
        container.textcontent = `Path: ${result.path.join(" → ")} | Distance: ${result.distance}`;

        // Draw the route
        const points = result.coordinates
            .map(point => `${point.x},${100 - point.y}`)
            .join(" ");

        document.getElementById("route-line")
            .setAttribute("points", points);
    } catch (error) {
        container.textContent = 'Error: ' + error.message;
    }
})