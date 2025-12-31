from django.urls import reverse_lazy

UNFOLD = {
    "SITE_TITLE": "OneBuild Admin",
    "SITE_HEADER": "OneBuild Construction Store",
    "SITE_SUBHEADER": "Admin Dashboard",
    "SITE_ICON": "🏗️",

    "COLORS": {
        "primary": {
            "50": "239 246 255",
            "100": "219 234 254",
            "200": "191 219 254",
            "300": "147 197 253",
            "400": "96 165 250",
            "500": "59 130 246",
            "600": "37 99 235",
            "700": "29 78 216",
            "800": "30 64 175",
            "900": "30 58 138",
        },
    },

    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": "Main",
                "items": [
                    {
                        "title": "Dashboard",
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                ],
            },
            {
                "title": "Store",
                "items": [
                    {"title": "Categories", "icon": "category", "link": "/admin/app/categories/"},
                    {"title": "Items", "icon": "inventory", "link": "/admin/app/items/"},
                    {"title": "Orders", "icon": "shopping_cart", "link": "/admin/app/orders/"},
                ],
            },
            {
                "title": "Users",
                "items": [
                    {"title": "Sellers", "icon": "group", "link": "/admin/app/sellers/"},
                    {"title": "Reviews", "icon": "star", "link": "/admin/app/reviews/"},
                ],
            },
        ],
    },
}
