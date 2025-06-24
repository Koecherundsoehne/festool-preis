from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
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

# Chrome Setup
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

# Zeitstempel
berlin = pytz.timezone("Europe/Berlin")
datum = datetime.now(berlin).strftime("%Y-%m-%d %H:%M")

# CSV-Datei schreiben
with open("preise_aktuell.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Produkt", "Preis", "Datum"])

    for url in urls:
        produktname = url.split("/")[-1].replace("_", " ").capitalize()
        print(f"Verarbeite: {produktname}")

        try:
            driver.get(url)

            # Warte auf das Preiselement (max 10 Sekunden)
            wait = WebDriverWait(driver, 10)
            preis_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".artikelbox-preis__gesamt p")))
            preis = preis_element.text.strip()
            print(f" → Preis gefunden: {preis}")

        except TimeoutException:
            preis = "Timeout beim Laden"
            print(f" ❌ Timeout für: {url}")
        except NoSuchElementException:
            preis = "Element nicht gefunden"
            print(f" ❌ Preis nicht gefunden: {url}")
        except Exception as e:
            preis = f"Fehler: {str(e)}"
            print(f" ❌ Allgemeiner Fehler bei {url}: {e}")

        writer.writerow([produktname, preis, datum])

driver.quit()
