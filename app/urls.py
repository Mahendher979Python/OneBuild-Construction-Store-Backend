from django.urls import path
from . import views

urlpatterns = [

    # Homepage
    path("", views.home, name="home"),

    # Cart Flow
    path("cart/", views.cart_page, name="cart"),
    path("checkout/", views.checkout_page, name="checkout"),
    path("order-success/", views.success_page, name="order_success"),

    # Razorpay
    path("place-order/", views.place_order, name="place_order"),
    path("create-razorpay-order/", views.create_razorpay_order, name="create_razorpay_order"),
    path("verify-razorpay-payment/", views.verify_razorpay_payment, name="verify_razorpay_payment"),

    # Static Pages
    path("house-cost-calculator/", views.house_cost_calculator, name="house_cost_calculator"),
    path("house-categories/", views.house_categories, name="house_categories"),

    # === YOUR NEW SELLER ROUTES ===
    path("seller-register/", views.seller_register, name="seller-register"),
    path("contractor-list/", views.contractor_list, name="contractor-list"),


    # 🚨 LAST — MUST BE THE LAST ROUTE ALWAYS
    path("<slug:slug>/", views.category_page, name="category"),
]
