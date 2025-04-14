from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from cloudinary.models import CloudinaryField
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator

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

    # Existing fields
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    key_features = ArrayField(
        models.CharField(max_length=200),
        blank=True,
        default=list,
        help_text="A list of key features (e.g., 'Turbo engine', 'Leather seats')"
    )
    sku = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    availability = models.CharField(
        max_length=20, choices=availability_choices, default='in_stock')
    car_type = models.CharField(
        max_length=20, choices=car_type_choices, default='classic'
    )
    image_url = models.URLField(blank=True, null=True) 
    image_public_id = models.CharField(max_length=255, blank=True, null=True)

    engine = models.CharField(
        max_length=100,
        blank=True,
        help_text="Engine configuration (e.g., '4.0L Twin-Turbo V8')"
    )
    power = models.CharField(
        max_length=100,
        blank=True,
        help_text="Power output (e.g., '496 hp @ 5,500 rpm')"
    )
    torque = models.CharField(
        max_length=100,
        blank=True,
        help_text="Torque output (e.g., '700 Nm @ 2,000-4,500 rpm')"
    )
    transmission = models.CharField(
        max_length=100,
        blank=True,
        help_text="Transmission type (e.g., '9G-TRONIC 9-Speed Automatic')"
    )
    acceleration_0_100 = models.CharField(
        max_length=50,
        blank=True,
        help_text="0-100 km/h acceleration time (e.g., '4.3 seconds')"
    )
    top_speed = models.CharField(
        max_length=50,
        blank=True,
        help_text="Top speed (e.g., '250 km/h (electronically limited)')"
    )
    fuel_economy = models.CharField(
        max_length=50,
        blank=True,
        help_text="Fuel consumption (e.g., '10.2 L/100km (combined)')"
    )
    dimensions = models.CharField(
        max_length=100,
        blank=True,
        help_text="Dimensions L×W×H (e.g., '5,289 mm × 1,954 mm × 1,503 mm')"
    )
    weight_kg = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Curb weight in kilograms"
    )
    wheelbase_mm = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Wheelbase in millimeters"
    )
    fuel_tank_capacity = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Fuel tank capacity in liters"
    )
    trunk_capacity_liters = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Trunk capacity in liters"
    )

    objects = models.Manager()  # Default manager
    productobjects = ProductObjects()  # Custom manager

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.name} - {self.car_type}"