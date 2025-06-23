import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Zielseite aufrufen
url = "https://wta.hoechsmann.com/de/article/214111/posten_handmaschinen_festool_ofk_500_q__ets_150__bs_75_e"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Preis aus .price-Klasse extrahieren
preis_element = soup.select_one(".price")
preis = "nicht gefunden"
if preis_element:
    preis = preis_element.text.strip()

# Aktuelles Datum und Uhrzeit
zeit = datetime.now().strftime("%d.%m.%Y %H:%M")

# Datei schreiben
with open("preis.txt", "w", encoding="utf-8") as f:
    f.write(f"{preis},{zeit}\n")
