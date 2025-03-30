from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# create your models here
class ChaiVariety(models.Model):
    CHAI_TYPE_CHOICES = [
        ('PT', 'Plain Tea'),
        ('MC', 'Masala Chai'),
        ('GC', 'Ginger Chai'),
        ('LC', 'Lemon Chai'),
        ('EC', 'Elaichi Chai'),
        ('GT', 'Green Tea'),
        ('BT', 'Black Tea'),
        ('KC', 'Kulhad Chai'),
    ]

    name = models.CharField(max_length=20)
    price = models.IntegerField()
    image = models.ImageField(upload_to='chais/')
    date_time = models.DateTimeField(default=timezone.now)
    chai_type = models.CharField(max_length=2, choices=CHAI_TYPE_CHOICES, default="PT")
    description = models.TextField(default="", blank=True)
    
    class Meta:
        verbose_name = 'Chai Variety'
        verbose_name_plural = 'Chai Varieties'
    
    def __str__(self):
        return self.name
    
class ChaiReview(models.Model):
    chai = models.ForeignKey(ChaiVariety, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        help_text="Rate between 1 and 5"
    )
    comment = models.TextField(blank=True)
    date_added = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Chai Review'
        verbose_name_plural = 'Chai Reviews'
        unique_together = ['chai', 'user']  # Prevent duplicate reviews
        ordering = ['-date_added']  # Show newest reviews first

    def __str__(self):
        return f'{self.user.username} review for {self.chai.name}'

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.rating < 1 or self.rating > 5:
            raise ValidationError({'rating': 'Rating must be between 1 and 5'})

class Store(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    address = models.TextField(help_text="Full address of the store", default="")
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    opening_time = models.TimeField(help_text="Store opening time", default='09:00')
    closing_time = models.TimeField(help_text="Store closing time", default='21:00')
    is_active = models.BooleanField(default=True)
    chai_varieties = models.ManyToManyField(ChaiVariety, related_name='stores')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Store'
        verbose_name_plural = 'Stores'
        ordering = ['name']

    def __str__(self):
        return self.name

    def is_open(self):
        current_time = timezone.localtime().time()
        return self.opening_time <= current_time <= self.closing_time
