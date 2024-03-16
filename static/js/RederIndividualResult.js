function getPrediction(event) {
    // Prevent the form from submitting normally
    event.preventDefault();

    // Get the form element
    var form = document.getElementById('predictionForm');

    // Check if the form is valid
    if (!form.checkValidity()) {
        // If the form is not valid, submit it to trigger the browser's default validation
        form.reportValidity();
        // Return false to prevent the form from being submitted
        return false;
    }

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
            document.getElementById('predictionResult').innerHTML = 'The predicted SGPA of next sem is ' + result.prediction;
        })
        .catch(error => {
            console.error('Error:', error);
        });

    return false;
}

function renderSemesterFields() {
    var semesterCount = document.getElementById('semesterCount').value;
    var semesterFieldsDiv = document.getElementById('semesterFields');
    semesterFieldsDiv.innerHTML = ''; // Clear previous fields

    for (var i = 1; i <= semesterCount; i++) {
        var label = document.createElement('label');
        label.setAttribute('for', 'sem' + i);
        label.innerText = 'Sem ' + i + ' Marks:';
        
        var input = document.createElement('input');
        input.setAttribute('type', 'number');
        input.setAttribute('step', '0.01');
        input.setAttribute('class', 'form-control');
        input.setAttribute('id', 'sem' + i);
        input.setAttribute('name', 'sem' + i);
        input.setAttribute('required', '');
        
        var div = document.createElement('div');
        div.setAttribute('class', 'col-md-12');
        div.appendChild(label);
        div.appendChild(input);

        semesterFieldsDiv.appendChild(div);
    }
}