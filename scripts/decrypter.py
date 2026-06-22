import os

from website.settings import BASE_DIR

SCRIPTS_FOLDER = BASE_DIR / "scripts"

from cryptography.fernet import Fernet
from dotenv import load_dotenv

_ = load_dotenv()

assert "ENCRYPTION_KEY" in os.environ, "ENCRYPTION_KEY missing!"
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

fernet = Fernet(ENCRYPTION_KEY)

bdayfile = SCRIPTS_FOLDER / "bdaydata.json"
encbdayfile = SCRIPTS_FOLDER / "encbday"

with encbdayfile.open(mode="rb") as f:
    encrypted = f.read()

decrypted = fernet.decrypt(encrypted)

print(decrypted)

# with bdayfile.open(mode="wb") as f:
#     f.write(decrypted)
