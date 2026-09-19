from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator


class CarMake(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    CAR_TYPES = (
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('Wagon', 'Wagon'),
        ('Coupe', 'Coupe'),
        ('Truck', 'Truck'),
    )
    car_type = models.CharField(max_length=20, choices=CAR_TYPES)
    year = models.IntegerField(validators=[MinValueValidator(2015), MaxValueValidator(2023)])

    def __str__(self):
        return f"{self.car_make.name} {self.name}"


class Dealer(models.Model):
    full_name = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    zip = models.CharField(max_length=10)
    state = models.CharField(max_length=2)

    def __str__(self):
        return self.full_name


class Review(models.Model):
    user_profile = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    dealer_id = models.IntegerField(default=0)
    review = models.TextField()
    purchase = models.BooleanField(default=False)
    purchase_date = models.DateField(null=True, blank=True)
    car_make = models.CharField(max_length=50, blank=True)
    car_model = models.CharField(max_length=50, blank=True)
    car_year = models.IntegerField(null=True, blank=True)
    sentiment = models.CharField(max_length=10, default="neutral")
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Review by {self.user_profile} on dealer {self.dealer_id}"
