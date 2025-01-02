 // Function to update the displayed value for sliders
 function updateValue(value, elementId) {
    document.getElementById(elementId).innerText = value;
}

// Function to show the loading overlay
function showLoading() {
    document.getElementById('loading-overlay').style.display = 'flex';
}

// Function to hide the loading overlay
function hideLoading() {
    document.getElementById('loading-overlay').style.display = 'none';
}

// Function to update the loading message
function updateLoadingMessage(message) {
    document.getElementById('loading-message').textContent = message;
}

document.getElementById('mainForm').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent default form submission

    showLoading();
    updateLoadingMessage('Processing your request. Please wait...');

    // Gather all form data
    const formData = new FormData(this);

    // Submit to the /data endpoint
    fetch('/data', {
        method: 'POST',
        body: formData
    }).then(response => {
        if (response.ok) {
            // Update the loading message
            updateLoadingMessage('Almost there! Thanks for your patience');

            // Submit the hidden form to /output (POST request)
            document.getElementById('redirectForm').submit();
        } else {
            console.error('Error submitting to /data:', response.status);
            updateLoadingMessage('Something went wrong. Please try again.');
            hideLoading(); // Hide the loading overlay on error
        }
    }).catch(error => {
        console.error('Error submitting to /data:', error);
        updateLoadingMessage('Something went wrong. Please try again.');
        hideLoading(); // Hide the loading overlay on error
    });
});