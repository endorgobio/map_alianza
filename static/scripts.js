// Event listener for DOMContentLoaded to render the initial Plotly graph
document.addEventListener('DOMContentLoaded', function () {
    // Render the Plotly graph with initial data
    Plotly.newPlot('graph', graph_json.data, graph_json.layout);
});



/**
 * Update the Plotly graph with new data from the server.
 */
async function updateGraph() {
    try {
        const response = await fetch('/update_graph', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const graph_json = await response.json();
        Plotly.newPlot('graph', graph_json.data, graph_json.layout);
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while updating the graph.');
    }
}

/**
 * Upload a file and update the graph and control values based on the uploaded data.
 */
async function uploadFile() {
    // Show loading indicator (optional)
    const button = document.getElementById('btn_load');
    const originalText = button.innerText;
    button.innerText = 'Loading...';
    button.disabled = true;

    try {
        let fileInput = document.getElementById('file-input');
        if (fileInput.files.length === 0) {
            alert("Please select a file first!");
            return;
        }

        let formData = new FormData();
        formData.append("file", fileInput.files[0]);

        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();      
        const graph_json = JSON.parse(data.graph_json);   

        Plotly.newPlot('graph', graph_json.data, graph_json.layout);

       
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while uploading the file.');
    } finally {
        // Reset button state
        button.innerText = originalText;
        button.disabled = false;
    }
}