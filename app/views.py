import json
import razorpay
import hmac
import hashlib

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .models import Order, OrderItem, Seller  # 🔥 THIS LINE FIXES EVERYTHING



# ======================
# HOME & STATIC PAGES
# ======================
def home(request):
    return render(request, "index.html")


def house_cost_calculator(request):
    return render(request, "house_cost_calculator.html")


def house_categories(request):
    return render(request, "house_categories.html")


def home_builder_contractor(request):
    return render(request, "contractor_list.html")


# ======================
# DYNAMIC CATEGORY PAGES
# ======================
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
# CART / CHECKOUT PAGES
# ======================
def cart_page(request):
    return render(request, "cart/cart.html")


def checkout_page(request):
    razorpay_key = getattr(settings, "RAZORPAY_KEY_ID", "")
    return render(request, "cart/checkout.html", {"RAZORPAY_KEY_ID": razorpay_key})


def success_page(request):
    return render(request, "cart/success.html")


def orders_page(request):
    # optional placeholder - use /admin for full order list
    return render(request, "cart/order.html")


# ---------------- PLACE ORDER ----------------
@csrf_exempt
def place_order(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)

    required = [
        "first_name", "surname", "phone",
        "address", "mandal", "district", "state", "pincode",
        "delivery_date", "items"
    ]

    for f in required:
        if f not in data:
            return JsonResponse({"status": "error", "message": f"Missing field: {f}"}, status=400)

    items = data.get("items") or []
    if not isinstance(items, list) or len(items) == 0:
        return JsonResponse({"status": "error", "message": "Cart is empty"}, status=400)

    # compute total safely
    try:
        total = 0.0
        for it in items:
            price = float(it.get("price", 0) or 0)
            qty = int(it.get("qty", 0) or 0)
            total += price * qty
    except Exception:
        return JsonResponse({"status": "error", "message": "Invalid item data"}, status=400)

    # create order
    order = Order.objects.create(
        first_name=data.get("first_name"),
        surname=data.get("surname"),
        phone=data.get("phone"),
        address=data.get("address"),
        mandal=data.get("mandal"),
        district=data.get("district"),
        state=data.get("state"),
        pincode=data.get("pincode"),
        delivery_date=data.get("delivery_date") or None,
        total=total
    )

    # create order items
    for it in items:
        try:
            OrderItem.objects.create(
                order=order,
                product_id=str(it.get("id", ""))[:200],
                name=str(it.get("name", ""))[:300],
                price=float(it.get("price", 0) or 0),
                qty=int(it.get("qty", 0) or 0)
            )
        except Exception:
            # rollback behaviour not implemented here (keep simple) — at least continue
            continue

    return JsonResponse({"status": "success", "order_id": order.id})


# ---------------- RAZORPAY ORDER ----------------
@csrf_exempt
def create_razorpay_order(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Only POST allowed"}, status=405)

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)

    db_order_id = payload.get("order_id")
    if not db_order_id:
        return JsonResponse({"status": "error", "message": "order_id required"}, status=400)

    try:
        order = Order.objects.get(id=int(db_order_id))
    except Order.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Order not found"}, status=404)

    # init razorpay client
    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    amount_paise = int(round(order.total * 100))
    try:
        razor_order = client.order.create({
            "amount": amount_paise,
            "currency": "INR",
            "receipt": f"order_{order.id}",
            "payment_capture": 1
        })
    except Exception as e:
        return JsonResponse({"status": "error", "message": "Razorpay order creation failed", "detail": str(e)}, status=500)

    # save razorpay order id to DB if field exists
    razor_id = razor_order.get("id")
    if razor_id:
        try:
            setattr(order, "razorpay_order_id", razor_id)
            order.save(update_fields=["razorpay_order_id"])
        except Exception:
            pass

    return JsonResponse({"status": "success", "razor_order": razor_order})


# ---------------- VERIFY PAYMENT ----------------
@csrf_exempt
def verify_razorpay_payment(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)

    db_order_id = data.get("order_id")
    payment_id = data.get("razorpay_payment_id")
    razor_order_id = data.get("razorpay_order_id")
    signature = data.get("razorpay_signature")

    if not (db_order_id and payment_id and razor_order_id and signature):
        return JsonResponse({"status": "error", "message": "Missing payment fields"}, status=400)

    try:
        order = Order.objects.get(id=int(db_order_id))
    except Order.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Order not found"}, status=404)

    # server-side signature verification
    expected = hmac.new(
        settings.RAZORPAY_KEY_SECRET.encode(),
        (str(razor_order_id) + "|" + str(payment_id)).encode(),
        hashlib.sha256
    ).hexdigest()

    if expected != signature:
        # mark failed if model has payment_status
        try:
            order.payment_status = "failed"
            order.save(update_fields=["payment_status"])
        except Exception:
            pass
        return JsonResponse({"status": "error", "message": "Invalid signature"}, status=400)

    # success: save payment details
    try:
        order.payment_id = payment_id
        order.payment_status = "paid"
        order.save(update_fields=["payment_id", "payment_status"])
    except Exception:
        pass

    return JsonResponse({"status": "success"})


# Seler Registrations..............

def seller_register(request):
    if request.method == "POST":
        Seller.objects.create(
            surname=request.POST.get("surname"),
            first_name=request.POST.get("firstName"),
            email=request.POST.get("gmail"),
            business_name=request.POST.get("nativeSelect"),
            city=request.POST.get("city"),
            village=request.POST.get("village"),
            mandal=request.POST.get("mandal"),
            zipcode=request.POST.get("zipcode"),
            aadhaar=request.POST.get("aadhaar"),
            phone=request.POST.get("phone"),
            description=request.POST.get("description"),
        )
        return render(request, "seller_success.html")

    return render(request, "seller_register.html")

from app.models import Seller
def contractor_list(request):
    sellers = Seller.objects.all()
    Seller.objects.count()
    return render(request, "contractor_list.html", {"sellers": sellers})
