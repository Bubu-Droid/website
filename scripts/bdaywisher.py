import json
import os

from django.core.mail import mail_admins
from django.utils.timezone import localtime

from website.settings import BASE_DIR

SCRIPTS_FOLDER = BASE_DIR / "scripts"

from cryptography.fernet import Fernet
from dotenv import load_dotenv

_ = load_dotenv()

assert "ENCRYPTION_KEY" in os.environ, "ENCRYPTION_KEY missing!"
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

fernet = Fernet(ENCRYPTION_KEY)

encbdayfile = SCRIPTS_FOLDER / "encbday"

with encbdayfile.open(mode="rb") as f:
    encrypted = f.read()

decrypted = json.loads(fernet.decrypt(encrypted))


def bdaywisher_mailer():
    # I've said this before and I'll say it again,
    # an average person cannot come anywhere close to
    # styling/designing which a proper LLM can.
    # Just check these message templates below. All of these are
    # written by Gemini. Would you be able to write something
    # like the html_message below?

    subject = "🎂 Birthday Reminder: {name} is turning {age} today!"

    plain_message = """\
    Hey!

    Just an automated reminder that today is {name}'s birthday!
    They are turning {age} years old today.

    Don't forget to send them a message!
    """

    html_message = """\
    <!DOCTYPE html>
    <html>
    <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
            <h2 style="color: #2c3e50;">🎂 Birthday Reminder!</h2>
            <p>Hey!</p>
            <p>Just an automated reminder that today is <strong>{name}'s</strong> birthday.</p>
            <p style="font-size: 18px; padding: 15px; background-color: #f8f9fa; border-left: 4px solid #007bff; border-radius: 4px;">
                They are turning <strong>{age} years old</strong> today! 🎈
            </p>
            <p>Don't forget to reach out and wish them a great day.</p>
            <br>
            <p style="font-size: 12px; color: #777;"><em>This is an automated reminder from your Django app.</em></p>
        </div>
    </body>
    </html>
    """

    today = localtime().now().day

    wished = False

    for key, value in decrypted.items():
        bdate = localtime().strptime(value, "%Y-%m-%d")
        if today == bdate.day:
            wished = True
            age = localtime().now().year - bdate.year
            mail_admins(
                subject.format(name=key, age=age),
                plain_message.format(name=key, age=age),
                fail_silently=False,
                html_message=html_message.format(name=key, age=age),
            )
            print(f"Sent reminder mail to wish happy birthday to {key}!")

    if not wished:
        # TEST: Remove the line below
        print(f"No birthdays to wish today... :<. Current time: {localtime().now()}")
