# [bubudroid.me][websitelink]

A personal website built with Django.

## Features

- Markdown-rendered blog posts
- Searchable blog and archive with keyword- and
  tag-based filtering
- Math rendering with LaTeX
- Clean, responsive layout (Tokyo Night-inspired)
- Static pages (About, Olympiads, Pet Peeves, etc.)
- Sitemap + robots.txt for SEO
- Error logging with email alerts

## Setup

```bash
git clone https://github.com/Bubu-Droid/website.git
cd website
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
touch .env
```

Set up the `.env` file using with the following template:

```python
SECRET_KEY = "<your-secret-key>"
DEBUG = TRUE
EMAIL_HOST_USER = "<sender-email>"
EMAIL_HOST_PASSWORD = "<sender-email-app-password>"
DJANGO_SETTINGS_MODULE = website.settings
ENCRYPTION_KEY = "<encryption-key>"
CRON_SECRET = "<cron-secret>"
```

- To generate a new secret key, you may use this
  [website][djangosecretwebsite].

- To generate an app password for your `<sender-email>` account,
  follow [this video][apppasswdvid] and then
  use the generated password as your `<sender-email-app-password>`.

- To generate an encryption key, install `cryptogrpahy` module
  using `pip install cryptography` and run the following python commands:

  ```python
  from cryptography.fernet import Fernet

  print(Fernet.generate_key())
  ```

- To generate a cron secret key, use [this][cronsecret] website to generate
  a password of at least 16 characters.

- To turn off debug mode, set the `DEBUG` parameter to `FALSE`.

- Also, make sure `settings.py` contains:

  ```python
  ADMINS = [("<your-name>", "<receiver-email>")]
  ```

Then run the deployment server:

```bash
python3 manage.py runserver
```

[websitelink]: https://www.bubudroid.me
[djangosecretwebsite]: https://djecrety.ir/
[apppasswdvid]: https://youtu.be/74QQfPrk4vE
[cronsecret]: https://1password.com/
