# 🛍️ E-Store — Django REST API

E-Store is a Django REST Framework backend for an e-commerce application. It exposes product, category, authentication, checkout, and order-history APIs consumed by the separate Vue frontend.

## 🚀 Live API

- **API:** https://e-store-django.onrender.com
- **Frontend:** https://e-store-vue.vercel.app/
- **Frontend repository:** https://github.com/AhmedReda47/E-Store_Vue

## ✨ Key Features

- Latest product, category detail, product detail, and product search APIs.
- Djoser user and token endpoints.
- Token-protected checkout and authenticated order history.
- Stripe charge creation in checkout.
- Django admin registration for products, categories, and orders.
- PostgreSQL-compatible database configuration with SQLite fallback.
- Cloudinary-backed uploaded media and Pillow thumbnail generation.
- CORS for `http://localhost:8080` and the deployed Vue frontend.
- WhiteNoise middleware for static files.

There are no cart endpoints in this backend; cart behavior is outside this repository. Although Simple JWT is installed, the checked-in settings and URLs configure DRF token authentication, not JWT authentication.

## 🛠️ Tech Stack

| Technology                   | Purpose                                         |
| ---------------------------- | ----------------------------------------------- |
| Python 3.10.13               | Runtime in `runtime.txt`                        |
| Django 3.1.7                 | Web framework and admin                         |
| Django REST Framework 3.12.2 | REST API                                        |
| Djoser 2.1.0                 | User and authentication routes                  |
| DRF authtoken                | Active protected-view authentication            |
| PostgreSQL / SQLite          | Production-compatible database / local fallback |
| psycopg2-binary 2.9.12       | PostgreSQL driver                               |
| Stripe 15.3.1                | Payment charges                                 |
| Cloudinary 1.46.0            | Media storage                                   |
| django-cors-headers 3.7.0    | CORS handling                                   |
| WhiteNoise 6.12.0            | Static files                                    |
| Gunicorn 26.0.0              | Production WSGI server                          |
| Pillow 12.3.0                | Image processing                                |

All pinned dependencies are listed in [requirements.txt](requirements.txt).

## 🏗️ Architecture

`djackets_django` contains global settings and URL routing. `product` contains catalog models, serializers, views, admin registration, migrations, and the `create_admin` command. `order` contains order models, serializers, checkout, order history, admin registration, and migrations. Djoser is mounted under `/api/v1/`.

## 📁 Project Structure

```text
E-Store_django/
├── djackets_django/       # settings, URLs, ASGI, and WSGI
├── product/               # products, categories, API, admin, migrations
│   └── management/commands/create_admin.py
├── order/                 # orders, checkout, API, admin, migrations
├── extras/                # deployment and server files
├── media/uploads/uploads/ # repository media path
├── staticfiles/           # collected static files
├── Dockerfile
├── manage.py
├── requirements.txt
├── runtime.txt
├── LICENSE
└── README.md
```

`models.py` defines persistence, `serializers.py` defines API representations, and `views.py` implements endpoint behavior. The project URL file also mounts `/admin/` and `/media/`.

## 🗄️ Database

`dj_database_url.config()` reads `DATABASE_URL` when present and otherwise uses `db.sqlite3`. Production is intended to use PostgreSQL with `psycopg2-binary`.

- `Category` has `name` and `slug`; products reference it through a foreign key named `category`.
- `Product` stores catalog data, price, optional image/thumbnail, and `date_added`. Deleting its category cascades.
- `Order` belongs to Django's built-in `User` and stores customer details, `paid_amount`, and `stripe_token`.
- `OrderItem` belongs to an `Order` and a `Product`, storing purchase `price` and `quantity`. Related deletion cascades.

## 🔐 Authentication & Authorization

Djoser's routes and authtoken routes are included at `/api/v1/`. Login/logout use Djoser's token endpoints. Checkout and order history explicitly require `TokenAuthentication` and `IsAuthenticated`:

```http
Authorization: Token <your-token>
```

Product and category reads do not declare authentication requirements. `/admin/` uses Django staff authentication. No JWT authentication class or JWT route is configured in the source.

## 📦 Product API

All paths below are relative to `/api/v1/`.

| Method | Endpoint                                    | Auth   | Purpose                                          |
| ------ | ------------------------------------------- | ------ | ------------------------------------------------ |
| GET    | `/latest-products/`                         | Public | Returns four newest products.                    |
| GET    | `/products/<category_slug>/`                | Public | Returns a category with nested products.         |
| GET    | `/products/<category_slug>/<product_slug>/` | Public | Returns one product in a category.               |
| POST   | `/products/search/`                         | Public | Searches `name` and `description` using `query`. |

Search request:

```json
{ "query": "laptop" }
```

An empty query returns `{"products": []}`. Product serialization exposes `id`, `name`, `get_absolute_url`, `description`, `price`, `get_image`, and `get_thumbnail`.

## 🛒 Order API

| Method | Endpoint            | Authentication             | Purpose                                                  |
| ------ | ------------------- | -------------------------- | -------------------------------------------------------- |
| GET    | `/api/v1/orders/`   | Token + authenticated user | Returns that user's orders.                              |
| POST   | `/api/v1/checkout/` | Token + authenticated user | Validates an order, charges Stripe in USD, and saves it. |

Checkout accepts `first_name`, `last_name`, `email`, `address`, `zipcode`, `place`, `phone`, `stripe_token`, and `items`. Each item contains `price`, `product`, and `quantity`.

```json
{
  "first_name": "<first-name>",
  "last_name": "<last-name>",
  "email": "<email>",
  "address": "<address>",
  "zipcode": "<postal-code>",
  "place": "<city>",
  "phone": "<phone>",
  "stripe_token": "<stripe-source-token>",
  "items": [{ "price": "<price>", "product": "<product-id>", "quantity": 1 }]
}
```

The server calculates the charge from database product prices and submitted quantities, converts it to cents, and returns `201` on success or `400` on validation/Stripe exceptions.

## 💳 Stripe Integration

The backend reads `STRIPE_SECRET_KEY`, creates a Stripe charge from the submitted `stripe_token`, and persists the paid order. The frontend obtains the payment source token and submits it to checkout. Never expose the secret key in frontend code or commit it.

## 🔌 API Documentation

- **Authentication:** `/api/v1/users/`, `/api/v1/users/me/`, `/api/v1/token/login/`, and `/api/v1/token/logout/`. Djoser also supplies its account-management operations under `/api/v1/users/`.
- **Products/categories:** `/api/v1/latest-products/`, `/api/v1/products/<category_slug>/`, and `/api/v1/products/<category_slug>/<product_slug>/`.
- **Search:** `POST /api/v1/products/search/`.
- **Orders:** `GET /api/v1/orders/`.
- **Checkout:** `POST /api/v1/checkout/`.
- **Other:** `/admin/` and `/media/<path>`.

There are no separate cart, payment-intent, or webhook routes.

## 🌎 Environment Variables

These names are read by settings or the custom admin command:

```dotenv
SECRET_KEY=<your-django-secret-key>
DEBUG=False
ALLOWED_HOSTS=<comma-separated-hosts>
DATABASE_URL=<your-postgresql-database-url>
STRIPE_SECRET_KEY=<your-stripe-secret-key>
CLOUDINARY_CLOUD_NAME=<your-cloudinary-cloud-name>
CLOUDINARY_API_KEY=<your-cloudinary-api-key>
CLOUDINARY_API_SECRET=<your-cloudinary-api-secret>
DJANGO_SUPERUSER_USERNAME=<admin-username>
DJANGO_SUPERUSER_EMAIL=<admin-email>
DJANGO_SUPERUSER_PASSWORD=<admin-password>
```

`DEBUG` defaults to `False`, `ALLOWED_HOSTS` defaults to `localhost,127.0.0.1`, and `DATABASE_URL` falls back to SQLite when absent. The custom command requires username and password; email is optional. `.env` is ignored by Git.

## ⚙️ Local Development

```bash
git clone https://github.com/AhmedReda47/E-Store_django.git
cd E-Store_django
python -m venv .venv
```

Windows PowerShell activation:

```powershell
.venv\Scripts\Activate.ps1
```

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The local server runs at `http://127.0.0.1:8000/`. To create the configured environment-based admin user, run `python manage.py create_admin`.

## 🗃️ Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## 🛡️ Security

Keep all secrets in environment variables, use `DEBUG=False` in production, restrict `ALLOWED_HOSTS`, and use token authentication for checkout and order history. CORS is limited to `http://localhost:8080` and `https://e-store-vue.vercel.app`. Django password validators, `CSRF_TRUSTED_ORIGINS` for the Render API, Cloudinary credential settings, and WhiteNoise middleware are configured. Secure-cookie and other additional hardening settings are not present in the checked-in settings.

## 🚀 Deployment

The backend is deployed on Render.

**Build command**

```bash
pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
```

**Start command**

```bash
gunicorn djackets_django.wsgi:application
```

Configure `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, PostgreSQL `DATABASE_URL`, Stripe variables, and Cloudinary variables in Render. The included `Dockerfile` collects static files and runs Gunicorn on port `10000`.

## 🌐 CORS Configuration

The configured origins are:

- `http://localhost:8080`
- `https://e-store-vue.vercel.app`

The Vue production URL must match this list exactly unless `CORS_ALLOWED_ORIGINS` is changed and redeployed.

## 🧪 Testing

`product/tests.py` and `order/tests.py` exist but contain only placeholder imports; no automated application tests are currently implemented.

## 🔧 Troubleshooting

- **Database:** Verify `DATABASE_URL` and run `python manage.py migrate`; without it, local SQLite is used.
- **Environment:** Check exact variable names and restart after changes.
- **CORS:** Use an exact configured origin, including scheme and port.
- **Static files:** Run `python manage.py collectstatic --noinput` and inspect the Render build logs.
- **Render:** Verify the build/start commands, `ALLOWED_HOSTS`, database URL, and application logs.
- **JWT/token:** This project uses `Authorization: Token <your-token>`, not JWT bearer authentication.
- **Stripe:** Verify the backend `STRIPE_SECRET_KEY` and a valid checkout `stripe_token`; never put the secret in Vue.

## 🔗 Related Frontend

[E-Store Vue repository](https://github.com/AhmedReda47/E-Store_Vue)

## 👨‍💻 Author

Ahmed Reda

## 📄 License

This repository includes the [MIT License](LICENSE), attributed in that file to SteinOveHelset (2021).
