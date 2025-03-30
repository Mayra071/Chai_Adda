document.getElementById('orderForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Show loading state
    document.getElementById('submitBtn').style.display = 'none';
    document.getElementById('spinner').style.display = 'block';
    
    // Submit form data via AJAX
    fetch(this.action, {
        method: 'POST',
        body: new FormData(this),
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success && data.redirect_url) {
            window.location.href = data.redirect_url;
        } else {
            throw new Error(data.error || 'Payment failed');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Payment initiation failed: ' + error.message);
        document.getElementById('submitBtn').style.display = 'block';
        document.getElementById('spinner').style.display = 'none';
    });
});