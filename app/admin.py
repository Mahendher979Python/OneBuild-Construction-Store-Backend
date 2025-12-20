from django.contrib import admin
from .models import Order, OrderItem
from .models import Seller

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product_id", "name", "price", "qty")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id", "first_name", "surname", "phone",
        "district", "state", "pincode",
        "delivery_date", "total", "payment_status", "created_at"
    )

    readonly_fields = ("created_at", "payment_id", "payment_status")
    inlines = [OrderItemInline]




@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ("first_name", "surname", "business_name", "city", "phone")
    search_fields = ("first_name", "surname", "business_name", "city")


