import requests
from bs4 import BeautifulSoup
from datetime import datetime

url = "https://wta.hoechsmann.com/de/article/214111/posten_handmaschinen_festool_ofk_500_q__ets_150__bs_75_e"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

preis = "nicht gefunden"

# Preis aus dem <title> extrahieren (ersatzweise)
title = soup.title.string if soup.title else ""
if "€" in title:
    teile = title.split("€")
    euro_zahl = teile[0].split()[-1]
    preis = euro_zahl + " €"

# Zeitformat
zeit = datetime.now().strftime("%d.%m.%Y %H:%M")

# Datei schreiben
with open("preis.txt", "w", encoding="utf-8") as f:
    f.write(f"{preis},{zeit}\n")
