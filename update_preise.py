from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
from urllib.parse import urlparse
import time
import os
import csv

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

# === Chrome-Setup (Headless für GitHub)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)

# === CSV initialisieren (falls nötig)
if not os.path.isfile(csv_datei):
    with open(csv_datei, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(csv_kopfzeile)

# === Verarbeitung der URLs
for url in urls:
    try:
        driver.get(url)
        time.sleep(3)  # Warten, bis Seite geladen ist

        # Preis finden – HTML-Analyse: Preise stehen in div.verkaufspreis
        preis_element = driver.find_
