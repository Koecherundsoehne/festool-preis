from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from urllib.parse import urlparse
from datetime import datetime
import time
import csv

# 👇 Hier deine Produkt-URLs eintragen
urls = [
    "https://wta.hoechsmann.com/de/article/214111/posten_handmaschinen_festool_ofk_500_q__ets_150__bs_75_e",
    "https://wta.hoechsmann.com/de/article/214120/posten_handmaschinen_bosch_makita_wegoma",
    "https://wta.hoechsmann.com/de/article/66800/posten_handmaschinen_festool_set_6",
    "https://wta.hoechsmann.com/de/article/70316/posten_handmaschinen_festool___fein_set_6"
]

# Selenium Headless Setup
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)

daten = []
datum = datetime.now().strftime("%Y-%m-%d %H:%M")

for url in urls:
    try:
        driver.get(url)
        time.sleep(3)  # Seitenaufbau abwarten

        # Produktname aus URL extrahieren
        produkt = urlparse(url).path.split('/')[-1].replace('_', ' ')

        # Preis extrahieren
        preis_element = driver.find_element(By.XPATH, '//td[contains(text(), "Gesamtsumme")]/following-sibling::td')
        preis_text = preis_element.text.strip()

        daten.append([datum, produkt, preis_text])
        print(f"{produkt}: {preis_text}")

    except (NoSuchElementException, TimeoutException):
        print(f"❌ Preis nicht gefunden: {url}")
        daten.append([datum, produkt, "Fehler"])

driver.quit()

# CSV schreiben
with open("preise_aktuell.csv", mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Datum", "Produkt", "Preis"])
    writer.writerows(daten)
