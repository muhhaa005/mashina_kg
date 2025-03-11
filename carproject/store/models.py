from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator
from multiselectfield import MultiSelectField


ROLE_CHOICES = (
    ('owner', 'owner'),
    ('client', 'client')
)

class UserProfile(AbstractUser):
    phone_number = PhoneNumberField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_images/', null=True, blank=True)


class Client(UserProfile):
    role = models.CharField(max_length=32, choices=ROLE_CHOICES, default='client')
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(15),
                                                       MaxValueValidator(80)], null=True, blank=True)

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'

    class Meta:
        verbose_name= 'client'
        verbose_name_plural = "client"


class Owner(UserProfile):
    owner_name = models.CharField(max_length=32)
    role = models.CharField(max_length=32, choices=ROLE_CHOICES, default='owner')
    location = models.CharField(max_length=64)

    def __str__(self):
        return self.owner_name

    class Meta:
        verbose_name= 'owner'
        verbose_name_plural = "owner"


class Category(models.Model):
    category_name = models.CharField(max_length=32)

    def __str__(self):
        return f'{self.category_name}'


class CarMake(models.Model):
    car_name = models.CharField(max_length=32, unique=True)
    car_image = models.FileField(upload_to='car_images/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='category_make')

    def __str__(self):
        return self.car_name


class CarModel(models.Model):
    car_model = models.CharField(max_length=32, unique=True)
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name='car_makes')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='category_model')

    def __str__(self):
        return f'{self.car_model}'



class Car(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name='makes')
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name='model')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    year = models.PositiveSmallIntegerField()
    BODY_CHOICES = (
        ('любое', 'любое'),
        ('седан', 'седан'),
        ('внедорожник', 'внедорожник'),
        ('пикап', 'пикап'),
        ('универсал', 'универсал'),
        ('внедорожник', 'внедорожник'),
        ('фургон', 'фургон'),
        ('минивен', 'минивен'),
    )
    body = models.CharField(max_length=32, choices=BODY_CHOICES, default='любое', verbose_name='Кузов')
    FUEL_CHOICES = (
        ('любое', 'любое'),
        ('бензин', 'бензин'),
        ('дизель', 'дизель'),
        ('гибрид', 'гибрид'),
        ('электро', 'электро'),
        ('газ', 'газ'),
    )
    fuel = MultiSelectField(max_length=32, choices=FUEL_CHOICES, max_choices=2, default='любое', verbose_name='Топливо')
    RUDDER_CHOICES = (
        ('слева', 'слева'),
        ('справа', 'справа'),
    )
    rudder = models.CharField(max_length=32, choices=RUDDER_CHOICES, default='слева', verbose_name='Руль')
    GEARBOX_CHOICES = (
        ('любое', 'любое'),
        ('механика', 'механика'),
        ('автомат', 'автомат'),

    )
    gearbox = models.CharField(max_length=32, choices=GEARBOX_CHOICES, default='любое', verbose_name='Коробка')
    COLOR_CHOICES = (
        ('любое', 'любое'),
        ('черный', 'черный'),
        ('белый', 'белый'),
        ('карсный', 'красный'),
        ('голубой', 'голубой'),
    )
    color = models.CharField(max_length=32, choices=COLOR_CHOICES, default='любое', verbose_name='Цвет')
    date_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.car_make}, {self.car_model}'

    def get_count_people(self):
        people = self.car_review.all()
        if people.exists():
            return people.count()
        return 0


    def get_avg_rating(self):
        total = self.car_review.all()
        if total.exists():
            return round(sum([i.stars for i in total]) / total.count(), 1)


class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='car_images')
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return f'{self.car}'

class CarReview(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='car_review')
    user = models.ForeignKey(Client, on_delete=models.CASCADE)
    text = models.TextField()
    stars = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])


class Cart(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE)

    def get_total_price(self):
        total_price = sum(item.get_total_price() for item in self.item.all())
        return total_price


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_item')
    car = models.ForeignKey(Car, on_delete=models.CASCADE)


class Favorite(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)


class FavoriteItem(models.Model):
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE)

class History(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)