from django.db import models
from django.utils.timezone import now

class Order(models.Model):
    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    mandal = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    delivery_date = models.DateField(null=True, blank=True)  # ✅ FIX

    total = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    payment_id = models.CharField(max_length=255, blank=True, null=True)
    payment_status = models.CharField(max_length=50, default="Pending")

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product_id = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    price = models.FloatField()
    qty = models.IntegerField()

    def sub_total(self):
        return self.price * self.qty

    def __str__(self):
        return f"{self.name} ({self.qty})"


class Seller(models.Model):
    surname = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    email = models.EmailField()
    business_name = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    village = models.CharField(max_length=100, blank=True)
    mandal = models.CharField(max_length=100, blank=True)
    zipcode = models.CharField(max_length=6)
    aadhaar = models.CharField(max_length=12)
    phone = models.CharField(max_length=10)
    description = models.TextField(blank=True)
    rating = models.IntegerField(default=5)

    def __str__(self):
        return f"{self.first_name} {self.surname}"
