
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator


class UserProfile(AbstractUser):
    ROLE = (
        ('bayer', 'bayer'),
        ('seller', 'seller')
    )
    status_user = models.CharField(max_length=10, choices=ROLE, default='bayer')
    phone_number = PhoneNumberField(region='KG', null=True, blank=True)

    def __str__(self):
        return f"{self.username} - {self.status_user}"

class BrandCar(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Model(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'

class YearCar(models.Model):
    year = models.DateField()

    def __str__(self):
        return f'{self.year}'

class  Car(models.Model):
    brand = models.ForeignKey(BrandCar, related_name='cars', on_delete=models.CASCADE)
    model = models.ForeignKey(Model, related_name='car_model', on_delete=models.CASCADE)
    fuel_type = models.DecimalField(max_digits=6, decimal_places=1)
    transmission = (
        ('automat', 'automat'),
        ('mexanika','mexanika'),

    )
    year = models.ForeignKey(YearCar, related_name='car_year', on_delete=models.CASCADE)
    mileage = models.PositiveSmallIntegerField()
    price = models.PositiveSmallIntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='car_img')

    seller = models.ForeignKey(UserProfile, related_name='seller_car', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.brand} - {self.price} - {self.seller}'


class Action(models.Model):
    car = models.ForeignKey(Car, related_name='actions', on_delete=models.CASCADE)
    start_price = models.IntegerField()
    min_price = models.PositiveSmallIntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    STATUS_A = (
        ('активен', 'активен'),
        ('завершен', 'завершен'),
        ('отменен', 'отменен'),
    )

    def __str__(self):
        return f"{self.car} - {self.start_time}"

class Bid(models.Model):
    action = models.ForeignKey(Action, related_name='bides', on_delete=models.CASCADE)
    buyer = models.ForeignKey(UserProfile, related_name='bir_bayer', on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.action}- {self.buyer}'


class Feedback(models.Model):
    seller = models.ForeignKey(UserProfile, related_name='feedback_seller', on_delete=models.CASCADE)
    buyer = models.ForeignKey(UserProfile, related_name='buyer_feedback', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField([MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.seller} - {self.buyer} - {self.rating}'