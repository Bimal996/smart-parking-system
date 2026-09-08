# ParkSmart Nepal — Smart Parking System (SPS)

A full-stack Django project that lets drivers search parking lots in **Dhangadhi, Kailali**,
see live slot availability, reserve a bay ahead of time, and
pay with **eSewa**, **Khalti**, or **cash on arrival**. Built as a BITM
university viva project, but wired up with genuine, working integrations
rather than mock screenshots.

---

## 1. Features

- **Professional public site** — Home (product overview + live stats),
  About (mission, project timeline, team), Contact (form, phone, email,
  address, social links), all in a custom "Asphalt & Sensor" design system.
- **Accounts** — sign up / log in with a proper form, editable profile
  (phone, address, default vehicle), and a **Bootstrap modal logout
  confirmation** so nobody logs out by accident.
- **Parking lots** — searchable/filterable list (by city, EV charging,
  covered parking, CCTV), lot detail page with an embedded Google Map
  (no API key required) and a live slot grid.
- **Reservations** — booking form with a **live price calculator** in
  JavaScript that recalculates as you change vehicle type or time window,
  slot auto-assignment, cancellation, and a bookings history page.
- **Payments** — three real, working flows:
  - **eSewa** — genuine ePay v2 integration (HMAC-SHA256 signed request,
    posts to eSewa's UAT test gateway).
  - **Khalti** — genuine KPG-2 server-side initiate/lookup calls; falls
    back to a clearly-labelled demo confirmation screen if no live secret
    key is configured, so the project still runs without one.
  - **Cash on arrival** — reserve now, pay at the gate.
- **Admin portal** — manage lots, slots, reservations, and payments from
  Django's built-in admin.
- **MySQL-ready** — runs on SQLite out of the box with zero setup; flip one
  environment variable to switch to MySQL for deployment.

---

## 2. Tech stack

| Layer      | Choice                                            |
|------------|----------------------------------------------------|
| Backend    | Django 5.1 (Python 3.12)                            |
| Database   | SQLite (default) / MySQL (optional, via env var)    |
| Frontend   | Django templates + Bootstrap 5 (grid/modal/JS) + custom CSS design system |
| Maps       | Google Maps embed (no API key needed)               |
| Payments   | eSewa ePay v2, Khalti KPG-2                          |

---

## 3. Project structure

```
spsproject/
├── manage.py
├── requirements.txt
├── .env.example
├── spsproject/          # project settings, root urls
├── pages/                # Home, About, Contact
├── accounts/              # signup, login, logout, profile
├── parking/               # ParkingLot, ParkingSlot, search & detail views
├── reservations/           # Reservation model, booking flow, live pricing
├── payments/                # Payment model, eSewa/Khalti/cash gateways
├── templates/                # base.html (navbar, footer, logout modal)
└── static/
    ├── css/style.css          # design system
    └── js/main.js              # nav toggle, alerts, live price calculator
```

Every app has its own `urls.py` with an `app_name`, so all URLs are
namespaced (e.g. `{% url 'parking:lot_detail' lot.slug %}`,
`{% url 'payments:choose' reservation.reference %}`).

---

## 4. Getting started

```bash
# 1. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy the environment example (optional — the project runs with defaults)
cp .env.example .env

# 4. Run migrations
python manage.py migrate

# 5. Replace parking data with five Dhangadhi, Kailali lots and their slots
python manage.py seed_demo

# 6. Create an admin account
python manage.py createsuperuser

# 7. Run the server
python manage.py runserver
```

Visit **http://127.0.0.1:8000/** for the site and
**http://127.0.0.1:8000/admin/** for the admin portal.

---

## 5. Trying the payment flows

- **eSewa**: the booking → payment → eSewa screen posts to eSewa's public
  **UAT test gateway** using the standard test merchant code `EPAYTEST`.
  On eSewa's test payment page you can log in with their published test
  credentials (eSewa ID `9806800001`–`9806800005`, password `Nepal@123`,
  MPIN `1122`, token `123456`) to complete a simulated payment.
- **Khalti**: with no `KHALTI_SECRET_KEY` set, the app shows a clearly
  labelled **demo confirmation screen** instead of a real redirect. Get a
  free test secret key from Khalti's test merchant dashboard and set it in
  `.env` to switch to the real KPG-2 flow automatically — no code changes
  needed.
- **Cash on arrival**: confirms the reservation immediately; the amount is
  shown as due at the gate.

---

## 6. Switching to MySQL

1. Install the MySQL client driver: `pip install mysqlclient`
   (uncomment it in `requirements.txt`).
2. Create a database, e.g. `CREATE DATABASE smart_parking_db CHARACTER SET utf8mb4;`
3. In `.env`, set `USE_MYSQL=True` and fill in `DB_NAME`, `DB_USER`,
   `DB_PASSWORD`, `DB_HOST`, `DB_PORT`.
4. Run `python manage.py migrate` again against the new database.

---

## 7. Customising for your viva

- **Developer profile** in the About page lives in `pages/views.py` →
  `about()` → the `team` list.
- **Contact details / social links** live in `spsproject/settings.py` →
  `SPS_SETTINGS`.
- **Demo lots & slots** live in `parking/management/commands/seed_demo.py`.
  Running `python manage.py seed_demo` replaces all existing parking lots and
  slots with the five Dhangadhi, Kailali entries.
- **Colors/fonts** live in `static/css/style.css` as CSS variables at the
  top of the file (`--asphalt-*`, `--sensor-amber*`, `--font-display`,
  `--font-body`).

---

## 8. References

- Django Software Foundation, *Django Documentation* (v5.1) — https://docs.djangoproject.com/
- eSewa Pvt. Ltd., *ePay v2 Integration Documentation* — https://developer.esewa.com.np/
- Khalti Digital Wallet, *KPG-2 Payment Gateway Documentation* — https://docs.khalti.com/
- Google, *Maps Embed API* — https://developers.google.com/maps/documentation/embed
- Bootstrap Team, *Bootstrap 5.3 Documentation* — https://getbootstrap.com/docs/5.3/
- Google Fonts, *Space Grotesk* & *Inter* type families — https://fonts.google.com/
- Nepal Rastra Bank, *Payment and Settlement Systems in Nepal* (context for local digital payment adoption) — https://www.nrb.org.np/

---

## 9. Default demo login

After running `createsuperuser` you can log into `/admin/` with the
credentials you set. To try the *customer-facing* flow, just sign up a
normal account from `/accounts/signup/` — it's a separate flow from the
Django admin account.
