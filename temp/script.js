document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('upload-form');
    const resultDisplay = document.getElementById('result');
    const fileInput = document.getElementById('upload-box');
    const fileNameDisplay = document.getElementById('file-name-display');

    // Display file name when a file is selected
    fileInput.addEventListener('change', () => {
        const file = fileInput.files[0];
        fileNameDisplay.textContent = file ? file.name : 'No file chosen';
    });

    // Handle form submission with fetch
    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const file = fileInput.files[0];
        if (!file) {
            resultDisplay.innerHTML = `<p style="color: red;">⚠️ Please select an image file.</p>`;
            return;
        }

        const formData = new FormData();
        formData.append('image', file);

        resultDisplay.innerHTML = `<p>⏳ Predicting... please wait.</p>`;
        

        try {
            const response = await fetch('http://localhost:5000/predict', {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();

            if (response.ok) {
                resultDisplay.innerHTML = `
                    <p>✅ <strong>Predicted Class:</strong> ${data.predicted_class.toUpperCase()}</p>
                `;
            } else {
                resultDisplay.innerHTML = `<p style="color: red;">❌ ${data.error || 'Unexpected error occurred.'}</p>`;
            }
        } catch (error) {
            resultDisplay.innerHTML = `<p style="color: red;">❌ Network error: ${error.message}</p>`;
            console.error('Fetch error:', error);
        }
    });
});
