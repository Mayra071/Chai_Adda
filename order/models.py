from django.db import models
from django.utils import timezone
from django.conf import settings
from chai.models import ChaiVariety

class Order(models.Model):
    SUGAR_LEVELS = [
        ('no', 'No Sugar'),
        ('normal', 'Normal'),
        ('less', 'Less Sugar'),
        ('max', 'Max Sugar')
    ]
    
    PAYMENT_STATUS = [
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded')
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    chai = models.ForeignKey(ChaiVariety, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    sugar_level = models.CharField(max_length=10, choices=SUGAR_LEVELS, default='normal')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    ordered_at = models.DateTimeField(default=timezone.now)
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='unpaid'
    )
    payment = models.OneToOneField(
        'payment.Payment',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='order'
    )
    notes = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-ordered_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f"Order #{self.id} - {self.chai.name} ({self.quantity}x)"

    def calculate_total_price(self):
        return self.quantity * self.chai.price

    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)
