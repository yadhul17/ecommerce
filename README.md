# Aura — Django Perfume Store

## 🌸 Overview

**Aura** is a Django-based perfume store web application that allows users to browse products, make purchases using Razorpay, and receive email confirmations after successful orders.

---

## 🛠 Features

- User registration and login
- Product catalog and search
- Shopping cart
- Checkout with Razorpay payment gateway
- **Order confirmation emails**
- Admin panel for products & orders

---

## 🚀 Built With

- Python
- Django
- Razorpay payment gateway (using `django-razorpay`) :contentReference[oaicite:0]{index=0}
- Django email (SMTP / transactional email service like SendGrid / SMTP)

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/aura.git
cd aura
activate the env 
run server

aura/
├── aura/                  # Django project settings
├── products/              # Product/catalog app
├── cart/                  # Cart management
├── orders/                # Orders & checkout logic
├── users/                 # Authentication
├── templates/             # HTML templates             # CSS/JS/assets
├── manage.py
├── requirements.txt
└── README.md
