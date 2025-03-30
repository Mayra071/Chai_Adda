document.addEventListener('DOMContentLoaded', function() {
    // Get price from HTML element (removes ₹ symbol and converts to number)
    const priceText = document.querySelector('.price-value').textContent;
    const pricePerCup = parseFloat(priceText.replace('₹', ''));
    
    const quantityInput = document.getElementById('quantity');
    const totalPriceDisplay = document.getElementById('totalPrice');

    function calculateTotal() {
        // Get quantity and ensure it's between 1-10
        let quantity = parseInt(quantityInput.value);
        
        if (isNaN(quantity) || quantity < 1) {
            quantity = 1;
        } else if (quantity > 10) {
            quantity = 10;
        }
        
        quantityInput.value = quantity; // Update input if corrected
        const total = quantity * pricePerCup;
        totalPriceDisplay.textContent = `₹${total.toFixed(2)}`;
    }

    // Set initial total (1 × price)
    calculateTotal();

    // Update when quantity changes
    quantityInput.addEventListener('input', calculateTotal);

    // Form submission
    document.getElementById('orderForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Show loading spinner
        document.getElementById('submitBtn').style.display = 'none';
        document.getElementById('spinner').style.display = 'block';
        
        // Get form values
        const name = document.getElementById('name').value;
        const quantity = parseInt(quantityInput.value);
        const sugarLevel = document.getElementById('sugar').value;
        const total = quantity * pricePerCup;
        
        // Redirect to payment
        window.location.href = `/payment?chai_id={{ chai.id }}&name=${encodeURIComponent(name)}&quantity=${quantity}&sugar=${sugarLevel}&total=${total.toFixed(2)}`;
    });
});