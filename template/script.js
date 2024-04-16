document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('file-input');
    const providerIdInput = document.getElementById('provider-id-input');
    const validatorIdInput = document.getElementById('validator-id-input');
    const proceedButton = document.querySelector('.proceed-button');
    const uploadSuccess = document.querySelector('#upload-success');
    const languageDisplay = document.getElementById('language-display');
    const tokensDisplay = document.getElementById('tokens-display');
    const sessionIdDisplay = document.getElementById('session-id-display');

    proceedButton.addEventListener('click', function() {
        const file = fileInput.files[0];
        const providerId = providerIdInput.value.trim();
        const validatorId = validatorIdInput.value.trim();

        if (file && providerId && validatorId) {
            const formData = new FormData();
            formData.append('file', file);
            
            // Include provider_id and validator_id as query parameters
            const url = `http://127.0.0.1:8000/api/v1/store?provider_id=${encodeURIComponent(providerId)}&validator_id=${encodeURIComponent(validatorId)}`;
            
            fetch(url, {
                method: 'POST',
                body: formData,
            }).then(response => response.json())
            .then(data => {
                console.log('Upload successful:', data);
                if(data.message) {
                    uploadSuccess.textContent = data.message; // Display success message
                    uploadSuccess.style.display = 'block';
                }

                // Display the returned data
                languageDisplay.textContent = 'Language: ' + data.language;
                tokensDisplay.textContent = 'Number of Tokens: ' + data.num_tokens;
                sessionIdDisplay.textContent = 'Session ID: ' + data.session_id;

                // Optionally reset file input
                fileInput.value = '';
            }).catch(error => {
                console.error('Upload error:', error);
                alert('Failed to upload the file. Please try again.');
            });
        } else {
            alert('Please ensure all fields are filled and a file is selected.');
        }
    });
});
