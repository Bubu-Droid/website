# [bubudroid.me][websitelink]

A personal website built with Django,
deployed on PythonAnywhere,
and secured via Cloudflare.

## 🌐 Features

- Markdown-rendered blog posts
- Searchable blog and archive with keyword- and
  tag-based filtering
- Math rendering with LaTeX
- Clean, responsive layout (Tokyo Night-inspired)
- Static pages (About, Olympiads, Pet Peeves, etc.)
- Sitemap + robots.txt for SEO
- HTTPS with HSTS via Cloudflare
- Error logging with email alerts

## ⚙️ Stack

| Component       | Tech                        |
| --------------- | --------------------------- |
| Backend         | Django                      |
| Frontend        | HTML, CSS, JS (Vanilla)     |
| Deployment      | PythonAnywhere              |
| DNS & HTTPS     | Cloudflare                  |
| Email Alerts    | Gmail (SMTP + App Password) |
| Version Control | Git + GitHub                |

## 🔒 Security

- TLS via Cloudflare + Full HTTPS mode
- HSTS preloading with subdomain support
- Secure headers: X-Content-Type-Options, X-Frame-Options, etc.
- Django admin only accessible via superuser
- Custom error logging and rotation

## 🚀 Live

Visit: [https://www.bubudroid.me][websitelink]

---

## 🛠️ Setup (Dev)

```bash
git clone https://github.com/Bubu-Droid/website.git
cd website
mkdir -p cache logs
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
touch website/rc.py
```

Set up `rc.py` with:

```python
# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = "<your-secret-key>"
```

To generate a new secret key, you may use this
[website][djangosecretwebsite].

Then run the deployment server:

```bash
python3 manage.py runserver --insecure
```

## 📧 Error Email Setup (Optional)

To enable error emails (e.g., for 500 Internal Server Errors),
add the following lines into `rc.py`.

```python
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = "<sender-email@gmail.com>"
EMAIL_HOST_PASSWORD = "<app-password>"

SERVER_EMAIL = EMAIL_HOST_USER
```

Also make sure `settings.py` contains:

```python
DEBUG = False
ADMINS = [("<your-name>", "<receiver-email@gmail.com>")]
```

> [!IMPORTANT]
> To generate an app password
> for your `<sender-email@gmail.com` account,
> follow [this video][apppasswdvid] and then
> use the generated password as your `<app-password>`.

---

### :memo: TODOs:

- [ ] Create table of contents for long pages.
- [ ] Add Ko-fi. (Maybe?)

[websitelink]: https://www.bubudroid.me
[djangosecretwebsite]: https://djecrety.ir/
[apppasswdvid]: https://youtu.be/74QQfPrk4vE?si=3TEWCLpivs94UUpQ
