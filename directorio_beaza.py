import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL del sitio web
url = 'https://poligonocabezobeaza.com/directorio'

# Encabezados y cookies para la solicitud HTTP

headers = {
    'Host': 'poligonocabezobeaza.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:129.0) Gecko/20100101 Firefox/129.0'
}

# Solicitud HTTP
respuesta = requests.get(url, headers=headers)

# Parseo del contenido HTML
soup = BeautifulSoup(respuesta.content, 'html.parser')

# Encuentra el contenedor principal
contenedor = soup.find('div', class_="sabai-directory-listings-with-map-listings sabai-col-sm-7")

# Inicializa listas para almacenar los datos
nombres_empresas = []
sector_empresa = []
direccion_empresas = []
emails_empresas = []

# Extrae los nombres de las empresas
empresas = contenedor.find_all('div', class_="sabai-directory-title")
nombres_empresas = [empresa.text.strip() for empresa in empresas]

# Extrae los sectores
sectores = contenedor.find_all('div', class_="sabai-directory-category")  # Verifica que esta clase sea correcta
sector_empresa = [sector.text.strip() for sector in sectores]

# Extrae las direcciones
direcciones = contenedor.find_all('div', class_="sabai-directory-location")
direccion_empresas = [direccion.text.strip() for direccion in direcciones]

# Extrae los correos electrónicos
emails = contenedor.find_all('div', class_="sabai-directory-contact-email")
emails_empresas = [email.find('a')['href'].replace('mailto:', '').strip() if email.find('a') else '' for email in emails]

# Imprime las longitudes de las listas para diagnóstico
print(f'Número de nombres: {len(nombres_empresas)}')
print(f'Número de sectores: {len(sector_empresa)}')
print(f'Número de direcciones: {len(direccion_empresas)}')
print(f'Número de correos electrónicos: {len(emails_empresas)}')

# Asegura que todas las listas tengan la misma longitud
max_length = max(len(nombres_empresas), len(direccion_empresas), len(emails_empresas), len(sector_empresa))

# Rellenar listas con valores vacíos si son más cortas que la longitud máxima
nombres_empresas.extend([''] * (max_length - len(nombres_empresas)))
direccion_empresas.extend([''] * (max_length - len(direccion_empresas)))
emails_empresas.extend([''] * (max_length - len(emails_empresas)))
sector_empresa.extend([''] * (max_length - len(sector_empresa)))

# Crear un DataFrame de pandas
df = pd.DataFrame({
    'Empresa': nombres_empresas,
    'Sector': sector_empresa,
    'Dirección': direccion_empresas,
    'Email': emails_empresas
})

# Imprimir el DataFrame
print(df)

# Contar el número de empresas
numero_de_empresas = len(df)
print(f'Número de empresas en el listado: {numero_de_empresas}')

# Exportar el DataFrame a un archivo CSV y Excel
df.to_csv('directorio_empresas.csv', index=False, encoding='utf-8')
df.to_excel('directorio_empresas.xlsx', index=False)
