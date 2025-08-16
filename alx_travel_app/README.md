# ALX Travel App 0x02 – Chapa Payment Integration

This project is a continuation of the `alx_travel_app_0x01` Django application, with added support for secure payment processing using the [Chapa API](https://developer.chapa.co/).

---

## 🚀 Features

- Duplicate of `alx_travel_app_0x01` with payment integration
- Payment initiation with Chapa
- Transaction verification via Chapa API
- Secure storage of API keys using environment variables
- Database tracking of payment status
- Sandbox testing support
- Optional: Email confirmation using Celery

---

## 🔐 Environment Variables

Create a `.env` file in the root directory and add your Chapa credentials:

```env
CHAPA_SECRET_KEY=your_chapa_secret_key_here


Make sure to install python-decouple to load environment variables securely:

pip install python-decouple

📦 Setup Instructions

Clone the repository:

git clone https://github.com/yourusername/alx_travel_app_0x02.git
cd alx_travel_app_0x02/alx_travel_app


Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate


Install dependencies:

pip install -r requirements.txt


Apply migrations:

python manage.py makemigrations
python manage.py migrate


Run the server:

python manage.py runserver
