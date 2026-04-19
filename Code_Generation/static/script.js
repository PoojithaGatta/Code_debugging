// Function to insert the copy button dynamically
function insertCopyButton() {
    const codeOutput = document.getElementById('generated-code');
    const copyButton = document.createElement('button');
    copyButton.id = 'copy-button';
    copyButton.innerHTML = '<i class="fas fa-copy"></i> Copy';
    codeOutput.parentElement.classList.add('code-output-container');
    codeOutput.parentElement.appendChild(copyButton);
}

// Function to handle copy to clipboard
function handleCopy() {
    const generatedCode = document.getElementById('generated-code');
    navigator.clipboard.writeText(generatedCode.textContent)
        .then(() => {
            alert('Code copied to clipboard!');
        })
        .catch((err) => {
            console.error('Failed to copy code: ', err);
        });
}

// Insert the copy button when the page loads
insertCopyButton();

// Add event listener to the copy button
document.getElementById('copy-button').addEventListener('click', handleCopy);

// Handle form submission
document.getElementById('prompt-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const prompt = document.getElementById('prompt').value;
    const selectedModel = document.getElementById('model').value;  // <-- Get selected model
    const generateButton = document.getElementById('generate-button');
    const buttonText = document.getElementById('button-text');
    const spinner = document.getElementById('spinner');
    const errorMessage = document.getElementById('error-message');
    const generatedCode = document.getElementById('generated-code');
    const copyButton = document.getElementById('copy-button');

    // Disable the button and show spinner
    generateButton.disabled = true;
    buttonText.textContent = 'Generating...';
    spinner.classList.add('spinner-visible');
    errorMessage.textContent = '';
    generatedCode.textContent = '';
    copyButton.style.display = 'none'; // Hide the copy button initially

    try {
        // Send the prompt and model to the backend
        const response = await fetch('/generate-code', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt: prompt, model: selectedModel }),  // <-- Send both
        });

        const data = await response.json();

        if (response.ok) {
            generatedCode.textContent = data.generated_code;
            copyButton.style.display = 'block'; // Show the copy button
        } else {
            errorMessage.textContent = data.error || 'Error generating code. Please try again.';
        }
    } catch (err) {
        errorMessage.textContent = 'Network error. Please try again.';
        console.error(err);
    } finally {
        generateButton.disabled = false;
        buttonText.textContent = 'Generate Code';
        spinner.classList.remove('spinner-visible');
    }
});
