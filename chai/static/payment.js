 // Toggle UPI ID field visibility
 document.querySelectorAll('input[name="payment_mode"]').forEach(radio => {
    radio.addEventListener('change', function() {
        document.getElementById('upi-id-container').style.display = 
            this.value === 'UPI' ? 'block' : 'none';
    });
});

// Handle payment submission
document.getElementById("submitBtn").addEventListener("click", function () {
    const paymentMode = document.querySelector('input[name="payment_mode"]:checked').value;
    const upiId = paymentMode === 'UPI' ? document.getElementById('upi-id').value : null;
    
    // Validate UPI ID if UPI mode selected
    if (paymentMode === 'UPI' && (!upiId || !upiId.includes('@'))) {
        alert("Please enter a valid UPI ID!");
        return;
    }

    // Show spinner
    document.getElementById("spinner").style.display = "block";
    document.getElementById("btn-text").textContent = "Processing...";

    // Prepare form data
    const formData = new FormData();
    formData.append('amount', '{{ chai.price }}');  // From template context
    formData.append('payment_mode', paymentMode);
    if (upiId) formData.append('upi_id', upiId);
    formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');

    // Submit to server
    fetch('/payment/create/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            if (paymentMode === 'UPI') {
                window.location.href = `/payment/verify-upi/${data.payment_id}/`;
            } else {
                window.location.href = '/payment/success/';
            }
        } else {
            alert("Payment failed: " + data.error);
        }
    })
    .catch(error => {
        alert("Network error. Please try again.");
    })
    .finally(() => {
        document.getElementById("spinner").style.display = "none";
        document.getElementById("btn-text").textContent = "Confirm Payment";
    });
});