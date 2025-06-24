from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import csv
from datetime import datetime
import pytz

# Liste der URLs
urls = [
    "https://wta.hoechsmann.com/de/article/214111/posten_handmaschinen_festool_ofk_500_q__ets_150__bs_75_e",
    "https://wta.hoechsmann.com/de/article/214120/posten_handmaschinen_bosch_makita_wegoma",
    "https://wta.hoechsmann.com/de/article/66800/posten_handmaschinen_festool_set_6",
    "https://wta.hoechsmann.com/de/article/70316/posten_handmaschinen_festool___fein_set_6"
]

# Browser Setup für GitHub Actions
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)

# Aktuelles Datum mit Zeitzone Berlin
berlin = pytz.timezone("Europe/Berlin")
datum = datetime.now(berlin).strftime("%Y-%m-%d %H:%M")

# CSV vorbereiten
with open("preise_aktuell.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Produkt", "Preis", "Datum"])

    for url in urls:
        try:
            driver.get(url)
            time.sleep(3)  # Warten auf das Laden der Seite

            # Preisfeld identifizieren – CSS-Klasse beachten
            preis_element = driver.find_element(By.CSS_SELECTOR, ".artikelbox-preis__gesamt p")
            preis = preis_element.text.strip()

        except Exception as e:
            preis = "Fehler"

        produktname = url.split("/")[-1].replace("_", " ").capitalize()
        writer.writerow([produktname, preis, datum])

driver.quit()
