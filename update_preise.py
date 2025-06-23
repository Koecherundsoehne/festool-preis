import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import os

# Liste der URLs
urls = [
    "https://wta.hoechsmann.com/de/article/214111/posten_handmaschinen_festool_ofk_500_q__ets_150__bs_75_e",
    "https://wta.hoechsmann.com/de/article/214120/posten_handmaschinen_bosch_makita_wegoma",
    "https://wta.hoechsmann.com/de/article/66800/posten_handmaschinen_festool_set_6",
    "https://wta.hoechsmann.com/de/article/70316/posten_handmaschinen_festool___fein_set_6"
]

# Heutiges Datum und Uhrzeit
datum = datetime.now().strftime("%d.%m.%Y")
zeit = datetime.now().strftime("%H:%M")

# Vorhandene Datei prüfen
file_exists = os.path.isfile("historie.csv")

with open("historie.csv", "a", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, delimiter=";")

    # Kopfzeile nur beim ersten Mal schreiben
    if not file_exists:
        writer.writerow(["Datum", "Uhrzeit", "Produkt", "Preis"])

    for url in urls:
        produktname = url.split("/")[-1].replace("_", " ")
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        preis_el = soup.select_one(".price")
        preis = preis_el.text.strip() if preis_el else "nicht gefunden"
        writer.writerow([datum, zeit, produktname, preis])
