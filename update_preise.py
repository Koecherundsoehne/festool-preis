import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import os
from urllib.parse import urlparse

# Liste deiner Preis-URLs
urls = [
    "https://wta.hoechsmann.com/de/article/214111/posten_handmaschinen_festool_ofk_500_q__ets_150__bs_75_e",
    "https://wta.hoechsmann.com/de/article/214120/posten_handmaschinen_bosch_makita_wegoma",
    "https://wta.hoechsmann.com/de/article/66800/posten_handmaschinen_festool_set_6",
    "https://wta.hoechsmann.com/de/article/70316/posten_handmaschinen_festool___fein_set_6"
]

# CSV-Datei für Preisverlauf
csv_datei = "historie.csv"

# Falls CSV noch nicht existiert, schreibe Header
if not os.path.exists(csv_datei):
    with open(csv_datei, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Datum", "Uhrzeit", "Produkt", "Preis"])

# Preise holen
for url in urls:
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        preis_element = soup.select_one(".price")
        preis = preis_element.text.strip() if preis_element else "nicht gefunden"
        produkt_name = urlparse(url).path.split("/")[-1]
        jetzt = datetime.now()
        datum = jetzt.strftime("%d.%m.%Y")
        uhrzeit = jetzt.strftime("%H:%M")

        # In CSV-Datei schreiben
        with open(csv_datei, "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([datum, uhrzeit, produkt_name, preis])

    except Exception as e:
        print(f"Fehler bei {url}: {e}")
