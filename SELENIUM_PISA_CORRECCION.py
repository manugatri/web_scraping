from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from selenium.common.exceptions import StaleElementReferenceException


# RUTA AL CHROMEDRIVER
path = '/Users/manuelangelgallardotrinidad/PRACTICAS_WEBSCRAPIN/chromedriver'

# CONFIGURACION DE CHROME
service = Service(path)
driver = webdriver.Chrome(service=service)

# URL DEL SITIO WEB
website = 'https://parquepisa.org/directorio/'

# APERTURA DEL NAVEGADOR
driver.get(website)
driver.maximize_window()
time.sleep(3)

# CREAMOS LAS LISTA DE LOS CAMPOS
Empresa = []
Sector = []
Telefono = []
Email = []
Web = []
Direccion = []
Link = []

# CONTENEDOR PRINCIPAL
contenedor = driver.find_element(By.XPATH, '//*[@id="js-grid-meet-the-team"]')

# BUSCA TODAS LAS EMPRESAS EN EL CONTENEDOR
empresas = contenedor.find_elements(By.XPATH, '//*[@id="js-grid-meet-the-team"]/div')

# RECORREMOS LAS PRIMERAS 10 EMPRESAS PARA EXTRAER EL NOMBRE, SECTOR Y LINK
for empresa in empresas:

    nombre_empresa = empresa.text.split('\n')[0]
    Empresa.append(nombre_empresa)

    try:
    	sector_empresa = empresa.text.split('\n')[1]
    	Sector.append(sector_empresa)
    except:
    	sector_empresa = "N/A"

    link = empresa.find_element(By.TAG_NAME, 'a').get_attribute('href')
    Link.append(link)
	

for i in Link:
		
	driver.get(i)

	telefono = driver.find_element(By.XPATH, '/html/body/div[4]/div[3]/ul/li[2]/a').text
	if not telefono:
		telefono = "N/A"
	Telefono.append(telefono)


	email = driver.find_element(By.XPATH, '/html/body/div[4]/div[3]/ul/li[4]').text
	email = email.replace('Email', '').strip()
	if not email:
		email = "N/A"	
	Email.append(email)

	web = driver.find_element(By.XPATH, '/html/body/div[4]/div[3]/ul/li[5]/a').get_attribute('href')
	if not web:
		web = "N/A"
	Web.append(web)

	direccion = driver.find_element(By.XPATH, '/html/body/div[5]/div[1]/ul/li').text
	if not direccion:
		direccion = "N/A"
	Direccion.append(direccion)

driver.quit()



# Asegurarse de que todas las listas tengan la misma longitud
max_length = max(len(Empresa), len(Sector), len(Link), len(Telefono), len(Email), len(Web), len(Direccion))

# Rellenar listas más cortas con "N/A"
while len(Empresa) < max_length:
    Empresa.append("N/A")
while len(Sector) < max_length:
    Sector.append("N/A")
while len(Link) < max_length:
    Link.append("N/A")
while len(Telefono) < max_length:
    Telefono.append("N/A")
while len(Email) < max_length:
    Email.append("N/A")
while len(Web) < max_length:
    Web.append("N/A")
while len(Direccion) < max_length:
    Direccion.append("N/A")

# CREAR EL DATA FRAME CON PANDAS
df = pd.DataFrame({
    'Empresa': Empresa,
    'Sector': Sector,
    'Link': Link,
    'Teléfono': Telefono,
    'Email': Email,
    'Web': Web,
    'Dirección': Direccion
})

print(df)
df.to_csv('pisa_corregido.csv', index=False)
df.to_excel('pisa_corregido.xlsx', index=False)