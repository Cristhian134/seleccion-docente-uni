/* ============================================================
   SIDENAV TOGGLE (Desktop + Mobile)
   ============================================================ */

const sidenav = document.getElementById("sidenav");
const backBtn = document.getElementById("backBtn");
const sidenavOverlay = document.getElementById("sidenavOverlay");

const toggleBtns = [
  document.getElementById("toggleBtnLogo"),
  document.getElementById("toggleBtnMobile"), // botón mobile
];

/* --- Expand / Collapse (desktop y mobile) --- */
toggleBtns.forEach((btn) => {
  if (!btn) return;
  btn.addEventListener("click", () => {
    sidenav.classList.toggle("collapsed");
    sidenav.classList.toggle("expanded");
    backBtn.classList.toggle("collapsed");

    if (window.innerWidth <= 768) {
      document.body.classList.toggle("sidenav-open");
      sidenav.classList.toggle("mobile-open");
    }
  });
});

/* --- Cerrar sidenav al hacer clic fuera (solo mobile) --- */
document.addEventListener("click", (e) => {
  const clickedOutside =
    !sidenav.contains(e.target) &&
    !e.target.closest("#toggleBtnLogo") &&
    !e.target.closest("#toggleBtnMobile");

  if (window.innerWidth <= 768 && clickedOutside) {
    closeMobileSidenav();
  }
});

/* --- Overlay para cerrar en móvil --- */
if (sidenavOverlay) {
  sidenavOverlay.addEventListener("click", () => closeMobileSidenav());
}

function closeMobileSidenav() {
  sidenav.classList.remove("expanded", "mobile-open");
  sidenav.classList.add("collapsed");
  backBtn.classList.add("collapsed");
  document.body.classList.remove("sidenav-open");
}

/* --- Estado inicial --- */
window.addEventListener("DOMContentLoaded", () => {
  if (window.innerWidth > 768) {
    sidenav.classList.add("expanded");
    backBtn.classList.remove("collapsed");
  } else {
    sidenav.classList.add("collapsed");
    backBtn.classList.add("collapsed");
  }
});

/* ============================================================
   HEADER — BOTÓN HAMBURGUESA (solo mobile)
   ============================================================ */

const headerBurger = document.getElementById("headerBurger");

if (headerBurger) {
  headerBurger.addEventListener("click", () => {
    sidenav.classList.add("expanded", "mobile-open");
    document.body.classList.add("sidenav-open");
  });
}
