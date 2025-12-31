import json, uuid, time, hmac, hashlib
import razorpay
import random

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import  get_user_model

from django.contrib import messages
from django.utils.timezone import now
from django.utils.crypto import get_random_string
from django.template.loader import get_template
from django.conf import settings
from django.contrib.auth.models import User

from xhtml2pdf import pisa
import json

from django.contrib.auth.decorators import login_required

from .models import (
    Category, Item, GalleryItem,
    ContactMessage, Review, Seller,
    Address, Order, OrderItem,
    PasswordOTP, LabourContract, CustomUser,
)

User = get_user_model()

# ---------- REGISTER ----------
def register(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        # 🔴 Basic validation
        if not username or not email or not password:
            messages.error(request, "All fields are required")
            return redirect("register")

        # 🔴 Username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        # 🔴 Email exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("register")

        # ✅ Create user safely
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.save()

        messages.success(request, "Account created successfully ✅ Please login")
        return redirect("login")

    return render(request, "auth/register.html")


# ----------  Login View (Username OR Gmail)----------

from django.contrib.auth import authenticate, login, logout
from django.db.models import Q


def login_view(request):
    if request.method == "POST":
        user_input = request.POST.get("username")  # username OR email
        password = request.POST.get("password")

        # ✅ filter instead of get (no crash)
        users = User.objects.filter(
            Q(username=user_input) | Q(email=user_input)
        )

        if not users.exists():
            messages.error(request, "User not found ❌")
            return redirect("login")

        if users.count() > 1:
            messages.error(request, "Multiple accounts found. Use username ❌")
            return redirect("login")

        user = users.first()

        # ✅ authenticate using username
        auth_user = authenticate(
            request,
            username=user.username,
            password=password
        )

        if auth_user is None:
            messages.error(request, "Invalid password ❌")
            return redirect("login")

        login(request, auth_user)
        messages.success(request, "Login successful ✅")
        return redirect("home")

    return render(request, "auth/login.html")

# ---------- LOGOUT ----------

def logout_view(request):
    logout(request)
    return redirect("login")

# ---------- FORGOT PASSWORD ----------

import random
from django.core.mail import send_mail


def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            send_mail(
                "OneBuild Password Reset OTP",
                "Your OTP is 123456",
                None,
                [email],
                fail_silently=False,
            )
            messages.success(request, "OTP sent to your email")
        except Exception as e:
            messages.error(
                request,
                "Email temporarily blocked by Gmail. Try again after few minutes."
            )
            print("SMTP ERROR:", e)

        return redirect("forgot_password")

    return render(request, "auth/forgot_password.html")

# ---------- RESET PASSWORD ----------

def reset_password(request):
    if request.method == "POST":
        otp = request.POST["otp"]
        password = request.POST["password"]

        user_id = request.session.get("reset_user")
        user = User.objects.get(id=user_id)

        otp_obj = PasswordOTP.objects.filter(
            user=user, otp=otp, is_used=False
        ).first()

        if not otp_obj:
            messages.error(request, "Invalid OTP")
            return redirect("reset_password")

        user.set_password(password)
        user.save()

        otp_obj.is_used = True
        otp_obj.save()

        messages.success(request, "Password reset successful")
        return redirect("login")

    return render(request, "auth/reset_password.html")

# ---------- DASHBOARD ----------

from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, "auth/dashboard.html")

# ======================================================
# HOME
# ======================================================

def home(request):
    return render(request, "index.html")


def house_categories(request):
    return render(request, "house_categories.html")

# ======================================================
# CUSTOMER SUPPORT
# ======================================================

def faq_view(request):
    return render(request, "customer_support/faq.html")


def contact_view(request):
    if request.method == "POST":
        ContactMessage.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            message=request.POST.get("message"),
        )
        messages.success(request, "Message sent successfully")
        return redirect("contact")

    return render(request, "customer_support/contact.html")


def review_form(request):
    if request.method == "POST":
        Review.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            rating=request.POST.get("rating"),
            comment=request.POST.get("comment"),
            review_type=request.POST.get("review_type"),
            product_name=request.POST.get("product_name"),
            service_name=request.POST.get("service_name"),
        )
        return redirect("review_dashboard")

    return render(request, "customer_support/reviews.html")


def review_dashboard(request):
    reviews = Review.objects.order_by("-created_at")
    return render(request, "customer_support/review_dashboard.html", {
        "reviews": reviews
    })

# ======================================================
# HELPDESK / POLICIES
# ======================================================

def privacy_policy(request):
    return render(request, "helpdesk/privacy_policy.html")


def terms_conditions(request):
    return render(request, "helpdesk/terms_conditions.html")


def shipping_policy(request):
    return render(request, "helpdesk/shipping_policy.html")


def refund_policy(request):
    return render(request, "helpdesk/refund_policy.html")

# ======================================================
# TOP NAVBAR / GALLERY
# ======================================================

def gallery_view(request):
    gallery_items = GalleryItem.objects.all()
    return render(request, "topnavabar/gallery.html", {
        "gallery_items": gallery_items
    })


def career(request):
    return render(request, "topnavabar/career.html")


def about(request):
    return render(request, "topnavabar/about.html")


def blog_list(request):
    return render(request, "topnavabar/blog.html")

# ======================================================
# CART & ORDERS
# ======================================================

def cart(request):
    return render(request, "cart/cart.html")


def checkout(request):
    return render(request, "cart/checkout.html")


def order_success(request):
    return render(request, "cart/success.html")


def order_details(request):
    return render(request, "cart/order_details.html")

@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "cart/order_detail.html", {"orders": orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    return render(request, "cart/order_detail.html", {
        "order": order,
        "items": order.items.all()
    })


@csrf_exempt
def place_order(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Invalid request"})

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON"})

    cart_items = data.get("items", [])
    if not cart_items:
        return JsonResponse({"status": "error", "message": "Cart empty"})

    total = 0
    for item in cart_items:
        total += float(item["price"]) * int(item["qty"])

    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        total_amount=total,
    )

    # ✅ Save order items
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product_id=item["id"],
            product_name=item["name"],
            price=item["price"],
            qty=item["qty"],
        )

    # ✅ Save address
    Address.objects.create(
        order=order,
        first_name=data.get("first_name"),
        surname=data.get("surname"),
        phone=data.get("phone"),
        address=data.get("address"),
        mandal=data.get("mandal"),
        district=data.get("district"),
        state=data.get("state"),
        pincode=data.get("pincode"),
        delivery_date=data.get("delivery_date"),
    )

    return JsonResponse({
        "status": "success",
        "order_id": order.order_id
    })

# ======================================================
# PRODUCTS & CATEGORIES
# ======================================================

def product_view(request):
    categories = Category.objects.all()
    return render(request, "cart/product.html", {
        "categories": categories
    })


CATEGORIES = {
    "aggregates": "Aggregates",
    "bricks-blocks": "Bricks & Blocks",
    "cement": "Cement",
    "sand": "Sand",
    "tmt": "TMT Bars",
    "roofing": "Roofing",
    "doors-windows": "Doors & Windows",
    "plumbing": "Plumbing",
    "electrical": "Electrical",
    "paints": "Paints",
    "flooring": "Flooring",
    "interior-designs": "Interior Designs",
    "glass-glazing": "Glass & Glazing",
    "insulation": "Insulation",
    "sanitaryware": "Sanitaryware",
}


def category_page(request, slug):
    if slug not in CATEGORIES:
        return HttpResponse("Category not found", status=404)

    return render(
        request,
        f"categories/{slug}.html",
        {"category_name": CATEGORIES[slug]}
    )






# ======================
# SELLER REGISTER
# ======================
def seller_register(request):
    if request.method == "POST":
        Seller.objects.create(
            business_name=request.POST.get("business_name"),
            owner_name=request.POST.get("owner_name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            category=request.POST.get("category"),
            description=request.POST.get("description"),
            profile_image=request.FILES.get("profile_image"),
            aadhaar_pdf=request.FILES.get("aadhaar_pdf"),
        )
        return redirect("seller_success")

    return render(request, "seller/seller_register.html")

# ======================
# SUCCESS PAGE
# ======================
def seller_success(request):
    return render(request, "seller/seller_success.html")


# ======================
# DASHBOARD
# ======================
def seller_dashboard(request):
    sellers = Seller.objects.all().order_by("-created_at")
    return render(request, "seller/seller_dashboard.html", {"sellers": sellers})

# ======================================================
# CONSTRUCTION SERVICES
# ======================================================

def house_cost_calculator(request):
    return render(request, "construction_services/calculator.html")


def generate_contract_no():
    return f"OB-LAB-{now().year}-{uuid.uuid4().hex[:4].upper()}"


def labour_contract_view(request):
    if request.method == "POST":
        contract = LabourContract.objects.create(
            contract_no=generate_contract_no(),
            contractor_name=request.POST.get("contractor_name"),
            contractor_address=request.POST.get("contractor_address"),
            worker_name=request.POST.get("worker_name"),
            worker_id=request.POST.get("worker_id"),
            worker_address=request.POST.get("worker_address"),
            start_date=request.POST.get("start_date"),
            end_date=request.POST.get("end_date"),
            working_hours=request.POST.get("working_hours"),
            wage_rate=request.POST.get("wage_rate"),
            payment_mode=request.POST.get("payment_mode"),
            is_locked=True
        )
        return redirect("labour_contract_pdf", contract_id=contract.id)

    return render(request, "construction_services/labour_register.html")


def labour_contract_pdf(request, contract_id):
    contract = get_object_or_404(LabourContract, id=contract_id)
    template = get_template("construction_services/labour_contract_pdf.html")
    html = template.render({"contract": contract})

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{contract.contract_no}.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response


def labour_offline_pdf(request):
    template = get_template("construction_services/labour_offline_pdf.html")
    html = template.render({})

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="labour_contract_template.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response


def labour_form_view(request):
    return render(request, "construction_services/labour_form.html")
