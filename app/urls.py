from django.urls import path
from . import views

urlpatterns = [

    # ======================
    # HOME
    # ======================
    path("", views.home, name="home"),


    # ======================
    # TOP NAV BAR PAGES
    # ======================
    path("about/", views.about, name="about"),
    path("blog/", views.blog_list, name="blog"),
    path("career/", views.career, name="career"),
    path("gallery/", views.gallery_view, name="gallery"),


    # ======================
    # CUSTOMER SUPPORT
    # ======================
    path("contact/", views.contact_view, name="contact"),
    path("faq/", views.faq_view, name="faq"),
    path("reviews/", views.review_form, name="reviews"),
    path("reviews/dashboard/", views.review_dashboard, name="review_dashboard"),

    # ======================
    # HELP DESK / POLICIES
    # ======================
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path("terms-conditions/", views.terms_conditions, name="terms_conditions"),
    path("shipping-policy/", views.shipping_policy, name="shipping_policy"),
    path("refund-policy/", views.refund_policy, name="refund_policy"),

    # ======================
    # AUTHENTICATION  USER LOGIN/REGISTER
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("forgot_password/", views.forgot_password, name="forgot_password"),
    path("reset_password/", views.reset_password, name="reset_password"),

    path("dashboard/", views.dashboard, name="dashboard"),

    # ======================
    # SELLER
    # ======================
    path("seller/register/", views.seller_register, name="seller_register"),
    path("seller/success/", views.seller_success, name="seller_success"),
    path("seller/dashboard/", views.seller_dashboard, name="seller_dashboard"),

    # ======================
    # CONSTRUCTION SERVICES
    # ======================
    path("house-cost-calculator/", views.house_cost_calculator, name="house_cost_calculator"),
    path("labour_contract_view/", views.labour_contract_view, name="labour_contract"),
    path("labour-offline-pdf/", views.labour_offline_pdf, name="labour_offline_pdf"),
    path("labour_form/", views.labour_form_view, name="labour_form_view"),
    path("labour-contract/pdf/<int:contract_id>/", views.labour_contract_pdf, name="labour_contract_pdf"),

    # extra.......
    path("house_categories/", views.house_categories, name="house_categories"),



    # ======================
    #  CART  @ PRODUCTS & CATEGORIES
    # ======================

    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("order-success/", views.order_success, name="order_success"),

    path("orders/", views.orders, name="orders"),
    path("orders/<str:order_id>/", views.order_detail, name="order_detail"),
    path("order_details/", views.order_details, name="order_details"),

    path("place-order/", views.place_order, name="place_order"),

    path("category/<slug:slug>/", views.category_page, name="category_page"),
]
