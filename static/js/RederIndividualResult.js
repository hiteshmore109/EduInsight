function getPrediction(event) {
    // Prevent the form from submitting normally
    event.preventDefault();

    // Show a loading message
    document.getElementById('predictionResult').innerHTML = 'Predicting...';

    // Get the form data
    var formData = new FormData(document.getElementById('predictionForm'));

    // Send an AJAX request to the server
    var url = document.getElementById('predictionForm').getAttribute('data-url');
    fetch(url, {
        method: 'POST',
        body: formData
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(result => {
            // Update the page with the prediction result
            document.getElementById('predictionResult').innerHTML = 'The predicted sem 4 is ' + result.prediction;
        })
        .catch(error => {
            console.error('Error:', error);
        });

    return false;
}