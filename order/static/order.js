document.addEventListener('DOMContentLoaded', function() {
    const pricePerCupElement = document.getElementById('price-per-cup');
    const quantityInput = document.getElementById('quantity');
    const totalPriceDisplay = document.getElementById('totalPrice');
    const finalPriceDisplay = document.getElementById('finalPrice');
    const orderForm = document.getElementById('orderForm');
    const submitBtn = document.getElementById('submitBtn');
    const spinner = document.getElementById('spinner');

    if (!pricePerCupElement || !quantityInput || !totalPriceDisplay) return;

    const pricePerCup = parseFloat(pricePerCupElement.dataset.price) || 0;

    function calculateTotal() {
        const quantity = Math.max(1, parseInt(quantityInput.value) || 0);
        const total = quantity * pricePerCup;
        totalPriceDisplay.textContent = `₹${total.toFixed(2)}`;
    }

    quantityInput.addEventListener('input', function () {
        this.value = this.value.replace(/[^0-9]/g, ''); // Allow only numbers
        calculateTotal();
    });

    calculateTotal(); // Initialize price

    if (orderForm) {
        orderForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            finalPriceDisplay.textContent = totalPriceDisplay.textContent;
            submitBtn.disabled = true;
            submitBtn.style.display = 'none';
            spinner.style.display = 'block';

            setTimeout(() => {
                this.submit();
            }, 500);
        });
    }
});
