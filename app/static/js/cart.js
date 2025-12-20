/* ======================================================
   ONEBUILD — GLOBAL ECOMMERCE CART + MODAL SYSTEM
   CLEAN VERSION — NO DUPLICATES
====================================================== */

const CART_KEY = "onebuild_global_cart_v1";

/* ---------------- CART CORE ---------------- */
function getCart() {
    try { return JSON.parse(localStorage.getItem(CART_KEY)) || []; }
    catch { return []; }
}

function saveCart(cart) {
    localStorage.setItem(CART_KEY, JSON.stringify(cart));
}

/* ---------------- ADD TO CART ---------------- */
function addToCart(item) {
    let cart = getCart();
    let existing = cart.find(p => p.id === item.id);

    if (existing) {
        existing.qty += item.qty || 1;
    } else {
        cart.push({ ...item, qty: item.qty || 1 });
    }

    saveCart(cart);
    updateCartBadge();
}

/* ---------------- REMOVE ---------------- */
function removeFromCart(id) {
    saveCart(getCart().filter(p => p.id !== id));
    updateCartBadge();
}

/* ---------------- QTY UPDATE ---------------- */
function updateQty(id, qty) {
    let cart = getCart();
    let item = cart.find(p => p.id === id);
    if (!item) return;

    item.qty = qty < 1 ? 1 : qty;
    saveCart(cart);
    updateCartBadge();
}

/* ---------------- BADGE ---------------- */
function updateCartBadge() {
    const badge = document.getElementById("cart-badge") || document.getElementById("cart-count");
    if (!badge) return;

    let total = getCart().reduce((s, p) => s + p.qty, 0);
    badge.innerText = total;
}
document.addEventListener("DOMContentLoaded", updateCartBadge);

/* ---------------- FIX IMAGE PATH ---------------- */
function resolveImgPath(path) {
    return path.replace(/^img:\//, "/images/");
}

/* ======================================================
   PRODUCT RENDERING (GRID)
====================================================== */
function renderProducts(productsArray, target = "products-grid") {
    const box = document.getElementById(target);
    if (!box || !productsArray) return;

    box.innerHTML = productsArray.map(p => `
        <div class="card">

            <div class="thumb" onclick="openModal('${p.id}')">
                <img src="${resolveImgPath(p.img)}">
            </div>

            <h3>${p.name}</h3>
            <div class="price">₹${p.price.toLocaleString()}</div>

            <div class="chips">
                ${p.tags.map(t => `<div class="chip">${t}</div>`).join("")}
            </div>

            <button class="btn add"
                onclick='addToCart(${JSON.stringify({
                    id: p.id, name: p.name, price: p.price, img: p.img
                })})'>
                ADD TO CART
            </button>
        </div>
    `).join("");
}

/* ======================================================
   PRODUCT MODAL
====================================================== */
function openModal(id) {
    const product = productsArray?.find(p => p.id === id);
    if (!product) return;

    document.getElementById("modalImg").src = resolveImgPath(product.img);
    document.getElementById("modalTitle").innerText = product.name;
    document.getElementById("modalDesc").innerText = product.desc || "";
    document.getElementById("modalPrice").innerText = product.price.toLocaleString();

    const tagBox = document.getElementById("modalTags");
    tagBox.innerHTML = product.tags.map(t => `<span class="tag">${t}</span>`).join("");

    const qtyEl = document.getElementById("modalQty");
    qtyEl.value = 1;

    document.getElementById("modalAddToCart").onclick = () => {
        addToCart({
            id: product.id,
            name: product.name,
            price: product.price,
            img: product.img,
            qty: parseInt(qtyEl.value)
        });
        closeModal();
    };

    document.getElementById("modal").style.display = "flex";
}

function closeModal() {
    document.getElementById("modal").style.display = "none";
}

/* Close modal (button, overlay, Esc key) */
document.addEventListener("click", e => {
    if (e.target.id === "closeModal") closeModal();
});
document.addEventListener("keydown", e => {
    if (e.key === "Escape") closeModal();
});

/* ======================================================
   CART PAGE RENDER
====================================================== */
function renderCartPage(container = "cart-container") {
    const box = document.getElementById(container);
    if (!box) return;

    let cart = getCart();
    if (cart.length === 0) {
        box.innerHTML = "<h2>Your cart is empty.</h2>";
        return;
    }

    let total = 0;

    box.innerHTML = `
        <table class="cart-table">
            <tr>
                <th>Product</th>
                <th>Qty</th>
                <th>Price</th>
                <th>Total</th>
                <th></th>
            </tr>

            ${cart.map(item => {
                let subtotal = item.qty * item.price;
                total += subtotal;

                return `
                    <tr>
                        <td>${item.name}</td>

                        <td>
                            <input type="number" min="1" value="${item.qty}"
                                onchange="updateQty('${item.id}', this.value); renderCartPage('${container}')"
                                class="qty-input">
                        </td>

                        <td>₹${item.price}</td>
                        <td>₹${subtotal}</td>

                        <td>
                            <button class="btn" onclick="removeFromCart('${item.id}'); renderCartPage('${container}')">
                                X
                            </button>
                        </td>
                    </tr>
                `;
            }).join("")}
        </table>

        <div class="cart-summary">
            <span class="grand">Grand Total: ₹${total.toLocaleString()}</span>
            <button class="btn add" onclick="window.location.href='/checkout/'">Checkout</button>
        </div>
    `;
}

/* ======================================================
   CHECKOUT (Connects to Django)
====================================================== */
function submitCheckoutForm() {
    let form = document.getElementById("checkoutForm");
    let data = new FormData(form);

    let customer = {};
    data.forEach((v, k) => (customer[k] = v));
    customer.items = getCart();

    fetch("/place-order/", {
        method: "POST",
        body: JSON.stringify(customer)
    })
        .then(r => r.json())
        .then(res => {
            if (res.status === "success") {
                saveCart([]);
                window.location.href = "/order-success/";
            } else {
                alert(res.message);
            }
        });
}
