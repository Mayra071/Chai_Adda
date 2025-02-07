from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

# create your models here
class Chai_varity(models.Model):
    Chai_type = [
        ('PT', 'Plane Tea'),
        ('MC', 'Masala chai'),
        ('GC', 'Ginger chai'),
        ('LC', 'Lemon chai'),
        ('EC', 'Elaichi chai'),
        ('GT', 'Green Tea'),
        ('BT', 'Black Tea'),
        ('KC', 'Kulhad Chai'),
    ]

    name = models.CharField(max_length=20)
    price = models.IntegerField()
    image = models.ImageField(upload_to='chais/')
    date_time = models.DateTimeField(default=timezone.now)
    Chai_type = models.CharField(max_length=2, choices=Chai_type, default="ML")
    description = models.TextField(default="")
    
    def __str__(self):
        return self.name
    
class ChaiReview(models.Model):
    chai = models.ForeignKey(Chai_varity, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} review for {self.chai.name}'
        

class Store(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    chai_varieties = models.ManyToManyField(Chai_varity, related_name='stores')

    def __str__(self):
        return self.name
