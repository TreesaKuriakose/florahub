# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User 
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Adding unique email field
    
    def __str__(self):
        return self.username  # Return username for user-friendly representation


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Example: 'Indoor' or 'Outdoor'
    description = models.TextField(blank=True, null=True)  # Optional description

    def __str__(self):
        return self.name



class Plant(models.Model):
    name = models.CharField(max_length=100)  # Plant name (e.g., Rose, Tulip)
    price = models.DecimalField(max_digits=6, decimal_places=2)  # Price
    image = models.ImageField(upload_to='plants/')  # Image of the plant
    description = models.TextField()  # Description of the plant
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='plants')
    stock = models.PositiveIntegerField(default=0)   
    def __str__(self):
        return self.name




from django.conf import settings  # Import settings to access AUTH_USER_MODEL
from django.db import models
from .models import Plant  # Assuming you have the Plant model

# Cart model
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use AUTH_USER_MODEL instead of User
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

    def total_price(self):
        # Sum up all the items in the cart
        total = sum(item.total_price() for item in self.items.all())
        return total


# CartItem model for each item in the cart
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.plant.name}"

    def total_price(self):
        return self.plant.price * self.quantity


# Payment model to track payment details (if needed)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)  # Link to the Plant (Product)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.plant.name}"