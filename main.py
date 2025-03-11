from CloudflareBypasser import CloudflareBypasser
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from DrissionPage import ChromiumPage, ChromiumOptions
import time
import os

co = ChromiumOptions()
# co.headless()

driver = ChromiumPage(addr_or_opts=co)
driver.get('https://www.remax.pe/web/search/property/propiedad-terreno-en-venta-trujillo-trujillo-la-libertad-1116998/')

cf_bypasser = CloudflareBypasser(driver)
cf_bypasser.bypass()

# Guardar el código fuente de la página en un archivo de texto
file_index = 1
file_name = "page_source.html"

while os.path.exists(file_name):
    file_index += 1
    file_name = f"page_source{file_index}.html"

with open(file_name, "w", encoding="utf-8") as f:
    f.write(driver.html)

driver.quit()