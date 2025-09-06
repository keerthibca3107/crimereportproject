// Add interactivity for flash messages and form UX
window.addEventListener('DOMContentLoaded', function() {
    // Animate flash messages
    const flashes = document.querySelectorAll('.flash');
    flashes.forEach(flash => {
        flash.style.opacity = 1;
        setTimeout(() => {
            flash.style.transition = 'opacity 0.7s';
            flash.style.opacity = 0;
        }, 3000);
    });

    // Add focus effect to inputs
    const inputs = document.querySelectorAll('input, textarea');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.style.borderColor = '#007bff';
            this.style.boxShadow = '0 0 5px #007bff44';
        });
        input.addEventListener('blur', function() {
            this.style.borderColor = '#ccc';
            this.style.boxShadow = 'none';
        });
    });
});
