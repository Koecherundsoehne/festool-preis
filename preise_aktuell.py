from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
import csv

urls = [
    "https://wta.hoechsmann.com/de/article/214111/posten_handmaschinen_festool_ofk_500_q__ets_150__bs_75_e",
    "https://wta.hoechsmann.com/de/article/214120/posten_handmaschinen_bosch_makita_wegoma",
    "https://wta.hoechsmann.com/de/article/66800/posten_handmaschinen_festool_set_6",
    "https://wta.hoechsmann.com/de/article/70316/posten_handmaschinen_festool___fein_set_6"
]

csv_datei = "preise_aktuell.csv"
kopfzeile = ["Produkt", "Preis (€)"]

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)

daten = []

for url in urls:
    try:
        driver.get(url)
        driver.implicitly_wait(5)

        preis_element = driver.find_element(By.CLASS_NAME, "verkaufspreis")
        preis = preis_element.text.strip()

        produkt = urlparse(url).path.split("/")[-1].replace("_", " ")
        daten.append([produkt, preis])

        print(f"✔ {produkt}: {preis}")

    except Exception as e:
        print(f"⚠ Fehler bei {url}: {e}")
        produkt = urlparse(url).path.split("/")[-1].replace("_", " ")
        daten.append([produkt, "nicht gefunden"])

driver.quit()

# Überschreibt die Datei mit den aktuellen Preisen
with open(csv_datei, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(kopfzeile)
    writer.writerows(daten)
