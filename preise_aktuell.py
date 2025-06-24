from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from datetime import datetime
import pytz
import csv

urls = [
    "https://wta.hoechsmann.com/de/article/214111/posten_handmaschinen_festool_ofk_500_q__ets_150__bs_75_e",
    "https://wta.hoechsmann.com/de/article/214120/posten_handmaschinen_bosch_makita_wegoma",
    "https://wta.hoechsmann.com/de/article/66800/posten_handmaschinen_festool_set_6",
    "https://wta.hoechsmann.com/de/article/70316/posten_handmaschinen_festool___fein_set_6"
]

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

berlin = pytz.timezone("Europe/Berlin")
datum = datetime.now(berlin).strftime("%Y-%m-%d %H:%M")

with open("preise_aktuell.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Produkt", "Preis", "Datum"])

    for url in urls:
        produktname = url.split("/")[-1].replace("_", " ").capitalize()
        print(f"🔍 Verarbeite: {produktname}")
        preis = "Unbekannt"

        try:
            driver.get(url)
            wait = WebDriverWait(driver, 20)

            box = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.artikelbox-preis__gesamt")
            ))

            p_tag = box.find_element(By.TAG_NAME, "p")
            preis = p_tag.text.strip()
            print(f"✅ Preis gefunden: {preis}")

        except TimeoutException:
            preis = "Timeout beim Preis finden"
            print(f"❌ Timeout bei {url}")
        except NoSuchElementException:
            preis = "Preis nicht gefunden"
            print(f"❌ Kein Preiselement bei {url}")
        except Exception as e:
            preis = f"Fehler: {str(e)}"
            print(f"❌ Allgemeiner Fehler: {e}")

        writer.writerow([produktname, preis, datum])

driver.quit()
