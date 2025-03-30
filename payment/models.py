from django.db import models
from django.conf import settings

class Payment(models.Model):
    PAYMENT_MODES = [
        ('CASH', 'Cash'),
        ('UPI', 'UPI'),
        ('CARD', 'Card'),
        ('WALLET', 'Digital Wallet')
    ]

    PAYMENT_STATUS = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
        ('PENDING_DELIVERY', 'Pending Delivery')
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="User"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(
        max_length=10,
        choices=PAYMENT_MODES,
        default='UPI'
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='PENDING'
    )
    transaction_id = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True
    )
    upi_id = models.CharField(max_length=50, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def __str__(self):
        username = self.user.username if self.user else "Guest"
        order = self.order if hasattr(self, 'order') else None
        return f"{username} - ₹{self.amount} ({self.payment_mode}) - {self.payment_status}"

    def mark_as_paid(self):
        self.is_paid = True
        self.payment_status = 'COMPLETED'
        if hasattr(self, 'order'):
            self.order.payment_status = 'paid'
            self.order.save()
        self.save()

    def mark_as_failed(self):
        self.is_paid = False
        self.payment_status = 'FAILED'
        if hasattr(self, 'order'):
            self.order.payment_status = 'failed'
            self.order.save()
        self.save()

    def mark_as_refunded(self):
        self.payment_status = 'REFUNDED'
        if hasattr(self, 'order'):
            self.order.payment_status = 'refunded'
            self.order.save()
        self.save()

    @property
    def chai(self):
        return self.order.chai if self.order else None