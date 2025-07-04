# tests/test_hash_logic.py
import hashlib
from glasfaserportal_notification import clean_html

def sha(text: str) -> str:
    """Erzeugt denselben SHA-256-Hash wie im Produktivcode."""
    return hashlib.sha256(text.encode()).hexdigest()

def test_hash_changes_if_html_changes():
    html_old = "<html><body>Status: 1</body></html>"
    html_new = "<html><body>Status: 2</body></html>"

    hash_old = sha(clean_html(html_old))
    hash_new = sha(clean_html(html_new))

    assert hash_old != hash_new, "Hash muss sich bei Inhaltsänderung ändern"

def test_hash_stays_if_html_identical():
    html = "<html><body>Status: 1</body></html>"
    assert sha(clean_html(html)) == sha(clean_html(html))
