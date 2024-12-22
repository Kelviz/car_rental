from django.db import models
from customers.models import UserAccount
from cloudinary.models import CloudinaryField



class Car(models.Model):
    city_mpg = models.IntegerField()
    car_class = models.CharField(max_length=255)
    combination_mpg = models.IntegerField()
    cylinders = models.IntegerField()
    displacement = models.FloatField()
    drive = models.CharField(max_length=255)
    fuel_type = models.CharField(max_length=50)
    highway_mpg = models.IntegerField()
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    transmission = models.CharField(max_length=50)
    year = models.IntegerField()
    daily_rent = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    available = models.BooleanField(default=True)
    image = models.ImageField(default='images/car_images/hero.png', upload_to='images')

    def __str__(self):
        return f"{self.year} {self.make} {self.model}"

class Booking(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled')
    ])

    def __str__(self):
        return f'Booking {self.id} by {self.user.get_full_name()} {self.status}'
    


class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed')
    ])

    reference = models.CharField(max_length=100, unique=True, null=True)

    def __str__(self):
        return f'Payment {self.id} for Booking {self.booking.id} {self.status}'
