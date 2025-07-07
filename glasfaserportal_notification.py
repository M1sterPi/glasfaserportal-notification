#!/usr/bin/env python3
import os
import re
import json
import hashlib
import asyncio
import smtplib
import sys

from pathlib import Path
from datetime import datetime
from email.message import EmailMessage
from typing import Optional

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from playwright.async_api import async_playwright

HERE = Path(__file__).parent
load_dotenv(dotenv_path=HERE / ".env")

FIBER_STATUS_URL = os.environ["FIBER_STATUS_URL"]
DATA_FILE        = Path(__file__).parent / "last_status.json"


SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ["SMTP_USER"]
SMTP_PASS = os.environ["SMTP_PASS"]
SMTP_TO   = os.environ.get("SMTP_TO", SMTP_USER)



def extract_status_from_html(path="telekom_raw.html") -> str:
    with open(path, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "lxml")

    headline = soup.find("h5", string="Aktuelle Informationen")
    if not headline:
        raise ValueError("Abschnitt 'Aktuelle Informationen' nicht gefunden!")
    paragraph = headline.find_next("p", class_="styles_statusBoxText__JUBF5")
    if not paragraph:
        raise ValueError("Status-Text nicht gefunden!")
    status_text = paragraph.get_text(separator=" ", strip=True)

    line_divs = soup.find_all("div", class_=re.compile(r"(^|\s)styles_line__"))
    #komplette class-Attribute speichern
    line_classes = [" ".join(d["class"]) for d in line_divs]
    lines_text = " | ".join(line_classes) if line_classes else "no lines found"

    #Status und Linien kombinieren
    combined = (
        status_text
        + "\n\nLINES:\n" + lines_text
    )
    print("DEBUG: Kombinierter Text für Hashing:\n", combined)
    return combined



async def fetch_hash() -> str:
    print("DEBUG: lade URL →", FIBER_STATUS_URL)
    """Lädt die Seite und hasht den kompletten, bereinigten HTML-Text."""
    async with async_playwright() as pw:
        browser = await pw.firefox.launch(headless=True)
        page   = await browser.new_page()

        # 1) Seite aufrufen
        await page.goto(FIBER_STATUS_URL, timeout=60_000)

        # 2) Auf Netzidle warten 
        await page.wait_for_load_state("networkidle", timeout=60_000)

        # 3) kompletten HTML-Quelltext einsammeln
        html = await page.content()

        #DEBUG: komplettes HTML in Datei schreiben ---
        Path("telekom_raw.html").write_text(html, encoding="utf-8")

        await browser.close()

    # 4) Alles Unwichtige raus und hashen
    status_text = extract_status_from_html()
    status_hash = hashlib.sha256(status_text.encode("utf-8")).hexdigest()
    return status_hash



def load_old_hash() -> Optional[str]:
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text()).get("hash")
    return None


def save_hash(h: str) -> None: 
    DATA_FILE.write_text(json.dumps({
        "hash": h,
        "timestamp": datetime.now().isoformat()
    }))


def send_email(subject: str, body: str) -> None:
    # Debug-Ausgabe, um zu prüfen, was geladen wird
    print("DEBUG: SMTP_USER:", SMTP_USER)
    print("DEBUG: SMTP_PASS repr:", repr(SMTP_PASS), "len=", len(SMTP_PASS))
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"]    = SMTP_USER
    msg["To"]      = SMTP_TO
    msg.set_content(body)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
        s.set_debuglevel(1)
        s.starttls()
        s.login(SMTP_USER, SMTP_PASS)
        s.send_message(msg)


async def main():
    new = await fetch_hash()
    old = load_old_hash()

    if new != old:
        send_email(
            "Telekom Glasfaser-Status geändert",
            f"Neuer Hash: {new}\n\nSieh dir die Seite an:\n{FIBER_STATUS_URL}"
        )
        save_hash(new)
        print(f"[{datetime.now():%H:%M}] Änderung erkannt, E-Mail versandt.")
        sys.exit(1)
    else:
        print(f"[{datetime.now():%H:%M}] Keine Änderung.")


if __name__ == "__main__":
    asyncio.run(main())
