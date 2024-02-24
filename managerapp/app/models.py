from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from ckeditor.fields import RichTextField


class User(AbstractUser):
    avatar = CloudinaryField('avatar', null=True)


class BaseModel(models.Model):
    created_date = models.DateField(auto_now_add=True, null=True)
    updated_date = models.DateField(auto_now=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Venue(BaseModel):
    name = models.CharField(max_length=100)
    description = RichTextField()
    image = models.ImageField(upload_to='venue/%Y/%m', null=True)

    # Giá thuê sảnh cưới cho các ca và cuối tuần
    price_morning = models.DecimalField(max_digits=10, decimal_places=2)
    price_noon = models.DecimalField(max_digits=10, decimal_places=2)
    price_evening = models.DecimalField(max_digits=10, decimal_places=2)
    price_weekend = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Service(BaseModel):
    name = models.CharField(max_length=100)
    description = RichTextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Menu(BaseModel):
    name = models.CharField(max_length=100)
    description = RichTextField()

    def __str__(self):
        return self.name


class FoodItem(BaseModel):
    name = models.CharField(max_length=100)
    description = RichTextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='food_items')
    image = models.ImageField(upload_to='food/%Y/%m', null=True)

    def __str__(self):
        return self.name


class Feedback(BaseModel):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"{self.customer.username}'s feedback for {self.venue.name}"


class Order(BaseModel):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    services = models.ManyToManyField(Service)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    payment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} for {self.customer.username}"
