document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('file-input');
    const providerIdInput = document.getElementById('provider-id-input');
    const validatorIdInput = document.getElementById('validator-id-input');
    const proceedButton = document.querySelector('.proceed-button');
    const uploadSuccess = document.getElementById('upload-success');
    const progressBarContainer = document.getElementById('progress-bar-container');
    const progressBarFill = document.getElementById('progress-bar-fill');
    const languageDisplay = document.getElementById('language-display');
    const tokensDisplay = document.getElementById('tokens-display');
    const sessionIdDisplay = document.getElementById('session-id-display');

    proceedButton.addEventListener('click', function() {
        const file = fileInput.files[0];
        const providerId = providerIdInput.value.trim();
        const validatorId = validatorIdInput.value.trim();

        // Add a UUID validation check here
        const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
        if (!file || !providerId || !uuidRegex.test(validatorId)) {
            alert('Please ensure all fields are filled with valid UUIDs and a file is selected.');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);
        
        const url = `http://127.0.0.1:8000/api/v1/store?provider_id=${encodeURIComponent(providerId)}&validator_id=${encodeURIComponent(validatorId)}`;
        
        uploadSuccess.style.display = 'none';
        progressBarContainer.style.display = 'block';
        progressBarFill.style.width = '0%';  // Reset progress bar width before starting upload
        
        proceedButton.disabled = true;

        fetch(url, {
            method: 'POST',
            body: formData
        }).then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok.');
            }
            return response.json();
        }).then(data => {
            console.log('Upload successful:', data);
            progressBarFill.style.width = '100%';  // Update progress bar to full width on success
            if (data.message) {
                uploadSuccess.textContent = data.message;
                uploadSuccess.style.display = 'block';
            }

            // Display the returned data
            languageDisplay.textContent = data.language || 'N/A';
            tokensDisplay.textContent = data.num_tokens || 'N/A';
            sessionIdDisplay.textContent = data.session_id || 'N/A';
        }).catch(error => {
            console.error('Upload error:', error);
            alert('Failed to upload the file. Please try again.');
        }).finally(() => {
            // Hide progress bar and reset input after operation
            setTimeout(() => {
                progressBarContainer.style.display = 'none';
                fileInput.value = '';  // Optionally reset file input
            }, 2000);  // Delay to show completed progress bar for a moment
        });
    });
});