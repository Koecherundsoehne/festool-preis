import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import os
from urllib.parse import urlparse

# === Produkt-URLs ===
urls = [
    "https://wta.hoechsmann.com/de/article/214111/posten_handmaschinen_festool_ofk_500_q__ets_150__bs_75_e",
    "https://wta.hoechsmann.com/de/article/214120/posten_handmaschinen_bosch_makita_wegoma",
    "https://wta.hoechsmann.com/de/article/66800/posten_handmaschinen_festool_set_6",
    "https://wta.hoechsmann.com/de/article/70316/posten_handmaschinen_festool___fein_set_6"
]

# === CSV-Datei ===
csv_datei = "historie.csv"
csv_kopfzeile = ["Datum", "Uhrzeit", "Produkt", "Preis (€)"]

# === CSV initialisieren ===
if not os.path.isfile(csv_datei):
    with open(csv_datei, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(csv_kopfzeile)
    print("✔ CSV-Datei erstellt mit Kopfzeile")

# === Schleife über Produkte ===
for url in urls:
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Preis finden – robust durch mehrere Selektoren
        preis = "nicht gefunden"
        mögliche_selector = [".price", ".value", "strong", "b", ".article-price"]
        for sel in mögliche_selector:
            el = soup.select_one(sel)
            if el and "€" in el.text:
                preis = el.text.strip()
                break

        # Produktname aus URL ableiten
        produkt = urlparse(url).path.split("/")[-1].replace("_", " ")

        # Zeitstempel
        jetzt = datetime.now()
        datum = jetzt.strftime("%d.%m.%Y")
        uhrzeit = jetzt.strftime("%H:%M")

        # In CSV schreiben
        with open(csv_datei, "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([datum, uhrzeit, produkt, preis])

        print(f"➕ {produkt}: {preis} ({datum} {uhrzeit})")

    except Exception as e:
        print(f"⚠ Fehler bei {url}: {e}")
