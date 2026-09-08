document.addEventListener("DOMContentLoaded", function () {
  // ---- Theme toggle ------------------------------------------------------
  const themeToggle = document.querySelector("[data-theme-toggle]");
  const themeLabel = document.querySelector("[data-theme-label]");
  if (themeToggle) {
    function updateThemeControl(theme) {
      const isDark = theme === "dark";
      document.documentElement.dataset.theme = isDark ? "dark" : "light";
      themeToggle.setAttribute("aria-pressed", String(isDark));
      themeToggle.setAttribute("aria-label", isDark ? "Switch to light theme" : "Switch to dark theme");
      themeToggle.setAttribute("title", isDark ? "Switch to light theme" : "Switch to dark theme");
      if (themeLabel) themeLabel.textContent = isDark ? "Light theme" : "Dark theme";
    }

    updateThemeControl(localStorage.getItem("parksmart-theme") || "light");
    themeToggle.addEventListener("click", function () {
      const nextTheme = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
      localStorage.setItem("parksmart-theme", nextTheme);
      updateThemeControl(nextTheme);
    });
  }

  // ---- Mobile nav toggle -------------------------------------------------
  const toggler = document.querySelector(".navbar-toggler-sps");
  const links = document.querySelector(".sps-nav-links");
  if (toggler && links) {
    toggler.addEventListener("click", function () {
      links.classList.toggle("open");
      toggler.setAttribute("aria-expanded", String(links.classList.contains("open")));
    });
  }

  // ---- Auto-dismiss flash messages --------------------------------------
  document.querySelectorAll(".sps-alert").forEach(function (el) {
    setTimeout(function () {
      el.style.transition = "opacity .4s ease";
      el.style.opacity = "0";
      setTimeout(function () { el.remove(); }, 400);
    }, 4500);
  });

  // ---- Live pricing calculator (booking page) ----------------------------
  const startInput = document.getElementById("id_start_time");
  const endInput = document.getElementById("id_end_time");
  const vehicleSelect = document.getElementById("id_vehicle_type");
  const priceBox = document.getElementById("live-price-box");

  if (startInput && endInput && vehicleSelect && priceBox) {
    const rateBike = parseFloat(priceBox.dataset.rateBike || "0");
    const rateCar = parseFloat(priceBox.dataset.rateCar || "0");

    function recalc() {
      const start = new Date(startInput.value);
      const end = new Date(endInput.value);
      const durationEl = document.getElementById("price-duration");
      const rateEl = document.getElementById("price-rate");
      const totalEl = document.getElementById("price-total");

      if (!startInput.value || !endInput.value || isNaN(start) || isNaN(end) || end <= start) {
        durationEl.textContent = "—";
        rateEl.textContent = "—";
        totalEl.textContent = "Rs. 0";
        return;
      }

      const hours = Math.max(1, Math.ceil((end - start) / (1000 * 60 * 60)));
      const rate = vehicleSelect.value === "bike" ? rateBike : rateCar;
      const total = hours * rate;

      durationEl.textContent = hours + (hours === 1 ? " hour" : " hours");
      rateEl.textContent = "Rs. " + rate + " / hour";
      totalEl.textContent = "Rs. " + total;
    }

    [startInput, endInput, vehicleSelect].forEach(function (el) {
      el.addEventListener("input", recalc);
      el.addEventListener("change", recalc);
    });
    recalc();
  }

  // ---- Manual reservation slot selection -------------------------------
  const selectedSlot = document.getElementById("id_selected_slot");
  const reservationSlots = document.querySelectorAll(".reservation-slot-chip");
  if (selectedSlot && reservationSlots.length) {
    function syncSlotChoices() {
      reservationSlots.forEach(function (slotButton) {
        slotButton.classList.toggle("selected", slotButton.dataset.slotNumber === selectedSlot.value);
      });
    }

    reservationSlots.forEach(function (slotButton) {
      slotButton.addEventListener("click", function () {
        selectedSlot.value = slotButton.dataset.slotNumber;
        syncSlotChoices();
      });
    });
    selectedSlot.addEventListener("change", syncSlotChoices);
    syncSlotChoices();
  }
});
