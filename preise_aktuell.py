from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from urllib.parse import urlparse
from datetime import datetime
import pytz
import csv

# URLs der Produkte
urls = [
    "https://wta.hoechsmann.com/de/article/214111/posten_handmaschinen_festool_ofk_500_q__ets_150__bs_75_e",
    "https://wta.hoechsmann.com/de/article/214120/posten_handmaschinen_bosch_makita_wegoma",
    "https://wta.hoechsmann.com/de/article/66800/posten_handmaschinen_festool_set_6",
    "https://wta.hoechsmann.com/de/article/70316/posten_handmaschinen_festool___fein_set_6"
]

# Chrome Headless Setup
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

# Aktuelles Datum/Zeit in deutscher Zeitzone
tz = pytz.timezone("Europe/Berlin")
datum = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

daten = []

for url in urls:
    produkt = urlparse(url).path.split('/')[-1].replace('_', ' ')
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        # Preis suchen: Zelle nach „Gesamtsumme“
        preis_element = wait.until(EC.presence_of_element_located((
            By.XPATH, '//td[contains(text(), "Gesamtsumme")]/following-sibling::td'
        )))

        preis = preis_element.text.stri_
