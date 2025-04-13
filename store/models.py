from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    class ProductObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(availability='in_stock')

    availability_choices = (
        ('in_stock', 'In Stock'),
        ('out_of_stock', 'Out of Stock')
    )

    car_type_choices = (
        ('classic', 'Classic'),
        ('electrical', 'Electrical'),
        ('luxury', 'Luxury')
    )

    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    sku = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    availability = models.CharField(
        max_length=20, choices=availability_choices, default='in_stock')
    car_type = models.CharField(
        max_length=20, choices=car_type_choices, default='classic'
    )  # New field
    images = models.URLField()
    objects = models.Manager()  # Default manager
    productobjects = ProductObjects()  # Custom manager

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.name} - {self.car_type}"
