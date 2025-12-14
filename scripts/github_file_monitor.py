import os
import sys

import django
import requests
from django.core.mail import send_mail

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")
django.setup()

from website.rc import EMAIL_HOST_USER
from website.settings import ADMINS

FILES = [
    {
        "name": "evan.sty",
        "path": "/tmp/evan.sty",
        "real_url": "https://github.com/vEnhance/dotfiles/blob/main/texmf/tex/latex/evan/evan.sty",
        "raw_url": "https://raw.githubusercontent.com/vEnhance/dotfiles/main/texmf/tex/latex/evan/evan.sty",
    },
    {
        "name": "strparse.py",
        "path": "/tmp/strparse.py",
        "real_url": "https://github.com/vEnhance/von/blob/main/von/strparse.py",
        "raw_url": "https://raw.githubusercontent.com/vEnhance/von/main/von/strparse.py",
    },
    {
        "name": "export-ggb-clean-asy.py",
        "path": "/tmp/export-ggb-clean-asy.py",
        "real_url": "https://github.com/vEnhance/dotfiles/blob/main/py-scripts/export-ggb-clean-asy.py",
        "raw_url": "https://raw.githubusercontent.com/vEnhance/dotfiles/main/py-scripts/export-ggb-clean-asy.py",
    },
]


def update_query(file_dict: dict) -> bool:
    r = requests.get(file_dict["raw_url"], timeout=20)
    r.raise_for_status()
    new_content = r.text

    try:
        with open(file_dict["path"], "r", encoding="utf-8") as f:
            old_content = f.read()
    except FileNotFoundError:
        old_content = None

    if old_content != new_content:
        with open(file_dict["path"], "w", encoding="utf-8") as f:
            f.write(new_content)
        return True
    return False


if __name__ == "__main__":
    try:
        changes = []
        no_changes = []

        for file in FILES:
            print(f'Checking {file["name"]}...')
            if update_query(file):
                changes.append(file)
            else:
                no_changes.append(file)

        plain_lines = [
            "Greetings,",
            "The GitHub file monitor cron job has finished checking files.",
            "",
        ]
        html_lines = [
            "<p>Greetings,</p><p>The GitHub file monitor cron job has finished checking files.</p><ul>"
        ]

        if changes:
            plain_lines.append("The following files have changed:")
            html_lines.append("<p>The following files have changed:</p><ul>")
            for f in changes:
                plain_lines.append(f"- {f['name']} ({f['real_url']})")
                html_lines.append(
                    f'<li><a href="{f["real_url"]}" target="_blank">{f["name"]}</a>: Change(s) detected!</li>'
                )
            html_lines.append("</ul>")

        if no_changes:
            plain_lines.append("\nFiles with no changes:")
            html_lines.append("<p>Files with no changes:</p><ul>")
            for f in no_changes:
                plain_lines.append(f"- {f['name']} ({f['real_url']})")
                html_lines.append(
                    f'<li><a href="{f["real_url"]}" target="_blank">{f["name"]}</a>: No change detected.</li>'
                )
            html_lines.append("</ul>")

        plain_message = "\n".join(plain_lines)
        html_message = "<html><body>" + "\n".join(html_lines) + "</body></html>"

        if changes:
            print("Sending email...")
            send_mail(
                "GitHub file monitor: changes detected",
                plain_message,
                EMAIL_HOST_USER,
                [admin[1] for admin in ADMINS],
                fail_silently=False,
                html_message=html_message,
            )
        else:
            print("No changes detected; no email sent.")

    except Exception as e:
        import traceback

        tb = traceback.format_exc()
        MESSAGE_TEXT = (
            f"<p>The cron job has run into unexpected errors:</p><pre>{tb}</pre>"
        )
        print("Sending error email...")
        send_mail(
            "GitHub file monitor: execution FAILED!",
            str(e),
            EMAIL_HOST_USER,
            [admin[1] for admin in ADMINS],
            fail_silently=False,
            html_message=MESSAGE_TEXT,
        )
        print(tb, file=sys.stderr)
