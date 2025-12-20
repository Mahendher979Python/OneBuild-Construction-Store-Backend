/* =========================================================
   ONEBUILD — NAVBAR + HOMEPAGE JAVASCRIPT WITH ANIMATIONS
========================================================= */

document.addEventListener("DOMContentLoaded", () => {

  /* -------------------------------------------------------
     1️⃣  BOTTOM LINKS — HOVER + ACTIVE + FADE SLIDE
  ------------------------------------------------------- */
  const bottomLinks = document.querySelectorAll(".bottom-links a");
  const currentPage = window.location.pathname.split("/").pop();

  bottomLinks.forEach(link => {
    // Smooth hover color
    link.style.transition = "color 0.3s ease";

    link.addEventListener("mouseenter", () => link.style.color = "#d65f0b");
    link.addEventListener("mouseleave", () => link.style.color = "#333");

    // Active page highlight
    if (link.href.includes(currentPage)) {
      link.classList.add("active-link");
    }
  });


  /* -------------------------------------------------------
     2️⃣  CART BUTTON REDIRECT
  ------------------------------------------------------- */
  const cartBtn = document.querySelector(".shop-cart-img");
  cartBtn?.addEventListener("click", () => {
    window.location.href = "/templates/cart.html";
  });


  /* -------------------------------------------------------
     3️⃣ LOGO COLOR EFFECT (HUE ROTATE)
  ------------------------------------------------------- */
  const randomHue = () => Math.floor(Math.random() * 360);
  const logoImg = document.querySelector(".logo-img");
  if (logoImg) {
    logoImg.style.transition = "filter 0.4s ease";
    logoImg.addEventListener("mouseover", () => {
      logoImg.style.filter = `hue-rotate(${randomHue()}deg)`;
    });
  }


  /* -------------------------------------------------------
     4️⃣ RIGHT ICONS HOVER ANIMATION (HUE ROTATE)
  ------------------------------------------------------- */
  const rightIcons = document.querySelectorAll(".right-buttons img");
  rightIcons.forEach(icon => {
    icon.style.transition = "filter 0.4s ease, transform 0.3s ease";
    icon.addEventListener("mouseover", () => {
      icon.style.filter = `hue-rotate(${randomHue()}deg)`;
      icon.style.transform = "scale(1.15)";
    });
    icon.addEventListener("mouseleave", () => {
      icon.style.transform = "scale(1)";
    });
  });


  /* -------------------------------------------------------
     5️⃣ MOBILE MENU — SLIDE DOWN / SLIDE UP ANIMATION
  ------------------------------------------------------- */
  const menuToggle = document.querySelector(".menu-toggle");
  const mobileMenu = document.querySelector(".mobile-menu");

  if (menuToggle && mobileMenu) {
    mobileMenu.style.transition = "max-height 0.4s ease, opacity 0.3s ease";
    mobileMenu.style.overflow = "hidden";
    mobileMenu.style.maxHeight = "0";
    mobileMenu.style.opacity = "0";

    menuToggle.addEventListener("click", () => {
      mobileMenu.classList.toggle("active");

      if (mobileMenu.classList.contains("active")) {
        mobileMenu.style.maxHeight = "300px";
        mobileMenu.style.opacity = "1";
      } else {
        mobileMenu.style.maxHeight = "0";
        mobileMenu.style.opacity = "0";
      }
    });
  }


  /* -------------------------------------------------------
     6️⃣ SCROLL TO TOP BUTTON — FADE + SLIDE
  ------------------------------------------------------- */
  const topBtn = document.querySelector(".float-btn .top");

  if (topBtn) {
    topBtn.style.transition = "opacity 0.4s ease, transform 0.4s ease";
    window.addEventListener("scroll", () => {
      if (window.scrollY > 300) {
        topBtn.classList.add("visible");
        topBtn.style.opacity = "1";
        topBtn.style.transform = "translateY(0)";
      } else {
        topBtn.style.opacity = "0";
        topBtn.style.transform = "translateY(20px)";
      }
    });

    topBtn.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }


  /* -------------------------------------------------------
     7️⃣ COPY PLUS CODE — POP ANIMATION
  ------------------------------------------------------- */
  const plusCode = document.getElementById("plusCode");
  const copyFeedback = document.getElementById("copyFeedback");

  if (plusCode && copyFeedback) {
    copyFeedback.style.transition = "opacity 0.4s ease, transform 0.3s ease";

    plusCode.addEventListener("click", () => {
      navigator.clipboard.writeText(plusCode.textContent.trim())
        .then(() => {
          copyFeedback.textContent = "✔️ Plus code copied!";
          copyFeedback.style.color = "green";
          copyFeedback.style.opacity = "1";
          copyFeedback.style.transform = "translateY(-5px)";

          setTimeout(() => {
            copyFeedback.style.opacity = "0";
            copyFeedback.style.transform = "translateY(0)";
          }, 1800);
        })
        .catch(() => {
          copyFeedback.textContent = "❌ Copy failed";
          copyFeedback.style.color = "red";
          copyFeedback.style.opacity = "1";

          setTimeout(() => {
            copyFeedback.style.opacity = "0";
          }, 1800);
        });
    });
  }


  /* -------------------------------------------------------
     8️⃣ GOOGLE MAP ROUTE BUTTON
  ------------------------------------------------------- */
  const routeBtn = document.getElementById("routeBtn");
  if (routeBtn && plusCode) {
    routeBtn.addEventListener("click", () => {
      const code = plusCode.textContent.trim();
      const mapURL = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(code + " Gangapur Telangana")}`;
      window.open(mapURL, "_blank");
    });
  }

});

/* -------------------------------------------------------
   EXTRA (DUPLICATE SAFETY) — MOBILE TOGGLE
------------------------------------------------------- */
const menuToggle2 = document.querySelector('.menu-toggle');
const mobileMenu2 = document.querySelector('.mobile-menu');
menuToggle2?.addEventListener('click', () => {
  mobileMenu2.classList.toggle('active');
});
