import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import os
from urllib.parse import urlparse

urls = [
    "https://wta.hoechsmann.com/de/article/214111/posten_handmaschinen_festool_ofk_500_q__ets_150__bs_75_e",
    "https://wta.hoechsmann.com/de/article/214120/posten_handmaschinen_bosch_makita_wegoma",
    "https://wta.hoechsmann.com/de/article/66800/posten_handmaschinen_festool_set_6",
    "https://wta.hoechsmann.com/de/article/70316/posten_handmaschinen_festool___fein_set_6"
]

csv_datei = "historie.csv"
header = ["Datum", "Uhrzeit", "Produkt", "Preis"]

# Datei initialisieren, falls nicht vorhanden
if not os.path.isfile(csv_datei):
    with open(csv_datei, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
    print("Created CSV header")

# Preise holen
for url in urls:
    response = requests.get(url, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    preis_el = soup.select_one(".price")
    preis = preis_el.text.strip() if preis_el else "nicht gefunden"

    produkt = urlparse(url).path.split("/")[-1]
    jetzt = datetime.now()
    datum = jetzt.strftime("%d.%m.%Y")
    uhrzeit = jetzt.strftime("%H:%M")

    with open(csv_datei, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datum, uhrzeit, produkt, preis])
    print(f"Appended {produkt}: {preis} at {datum} {uhrzeit}")
