function renderSemesterInputs() {
    const semesterCount = document.getElementById('semesterCount').value;
    const semesterInputsDiv = document.getElementById('semesterInputs');
    semesterInputsDiv.innerHTML = '';

    for (let i = 1; i <= semesterCount; i++) {
        const semesterInput = document.createElement('div');
        semesterInput.classList.add('col-md-12');

        const label = document.createElement('label');
        label.classList.add('form-label');
        label.textContent = `Sem ${i} Data:`;

        const input = document.createElement('input');
        input.type = 'file';
        input.classList.add('form-control');
        input.id = `sem${i}`;
        input.name = `sem${i}`;
        input.accept = '.csv';
        input.required = true;

        input.addEventListener('change', function (e) {
            const file = e.target.files[0];

            // Remove any existing error message before checking the new input
            const existingError = input.nextElementSibling;
            if (existingError && existingError.classList.contains('alert-danger')) {
                existingError.remove();
            }

            if (file.type !== 'text/csv') {
                const errorDiv = document.createElement('div');
                errorDiv.classList.add('alert', 'alert-danger');
                errorDiv.textContent = 'Only CSV files are allowed!';
                input.after(errorDiv);
                // Clear the input value
                e.target.value = '';
            } else {
                // Remove any existing error message if the file is valid
                const existingError = input.nextElementSibling;
                if (existingError) {
                    input.parentElement.removeChild(existingError);
                }
            }
        });

        semesterInput.appendChild(label);
        semesterInput.appendChild(input);
        semesterInputsDiv.appendChild(semesterInput);
    }
}

function getClassPrediction(event) {
    event.preventDefault();

    const formData = new FormData(document.getElementById('csvForm'));
    const url = document.getElementById('csvForm').dataset.url;

    fetch(url, {
        method: 'POST',
        body: formData
    })
        .then(response => response.blob())
        .then(blob => {
            const url = window.URL.createObjectURL(new Blob([blob]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'predicted_data.csv');
            document.body.appendChild(link);
            link.click();
            link.remove();
        })
        .catch(error => {
            console.error('Error:', error);
            const predictionResult = document.getElementById('predictionResult');
            predictionResult.innerHTML = '<div class="alert alert-danger">An error occurred while processing the prediction.</div>';
        });

    return false;
}