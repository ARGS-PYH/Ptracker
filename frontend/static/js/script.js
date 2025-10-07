document.addEventListener('DOMContentLoaded', () => {
    // Select all forms in the document
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', function (e) {
            let valid = true;
            const inputs = form.querySelectorAll('input, textarea, select');
            // Remove previous error messages
            form.querySelectorAll('.form-error').forEach(el => el.remove());

            inputs.forEach(input => {
                // Skip disabled or readonly fields
                if (input.disabled || input.readOnly) return;

                // Required field validation
                if (input.hasAttribute('required') && !input.value.trim()) {
                    showError(input, 'This field is required.');
                    valid = false;
                }

                // Email validation
                if (input.type === 'email' && input.value) {
                    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                    if (!emailPattern.test(input.value)) {
                        showError(input, 'Please enter a valid email address.');
                        valid = false;
                    }
                }

                // Number validation
                if (input.type === 'number' && input.value) {
                    if (isNaN(input.value)) {
                        showError(input, 'Please enter a valid number.');
                        valid = false;
                    }
                }

                // Minlength validation
                if (input.hasAttribute('minlength')) {
                    const min = parseInt(input.getAttribute('minlength'), 10);
                    if (input.value.length < min) {
                        showError(input, `Please enter at least ${min} characters.`);
                        valid = false;
                    }
                }

                // Maxlength validation
                if (input.hasAttribute('maxlength')) {
                    const max = parseInt(input.getAttribute('maxlength'), 10);
                    if (input.value.length > max) {
                        showError(input, `Please enter no more than ${max} characters.`);
                        valid = false;
                    }
                }

                // Pattern validation
                if (input.hasAttribute('pattern') && input.value) {
                    const pattern = new RegExp(input.getAttribute('pattern'));
                    if (!pattern.test(input.value)) {
                        showError(input, 'Invalid format.');
                        valid = false;
                    }
                }
            });

            if (!valid) {
                e.preventDefault();
            }
        });
    });

    function showError(input, message) {
        let error = document.createElement('div');
        error.className = 'form-error';
        error.style.color = 'red';
        error.style.fontSize = '0.9em';
        error.textContent = message;
        input.parentNode.insertBefore(error, input.nextSibling);
    }
});