from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from time import sleep

service = Service(executable_path="chromedriver.exe")
options = Options()
#options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
#options.add_argument('headless')
#options.add_argument('window-size=0x0')
driver = webdriver.Chrome(service=service, options=options)
#driver.minimize_window()



def scrapingEco(lista):
    """Esta funcion, por si sola, realiza la extraccion de datos de todos los productos de todas las paginas de productos de Eco"""

    print("\n\n\nIniciando proceso de scraping a Eco...")

    #Se inicializa el numero de pagina en 0 para que en cada iteracion este numero aumente. Se usa unicamente para mostrar en consola informacion sobre el proceso de extraccion.
    numeroPagina = 0

    while True:
        numeroPagina = numeroPagina + 1

        #Aqui se usa de forma literal el numero de pagina
        driver.get(f"https://www.ecofarmacias.cl/shop/page/{numeroPagina}/")

        #Se intenta detectar si encuentra el boton para confirmar si la pagina actual tiene productos. Si no esta, esto indica que ya termino de extraer datos de todas las paginas
        try:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="woocommerce_price_filter-4"]/form/div/div[2]/button')))
        except:
            break

        #Se considera un rango de 1 a 31 debido a que se muestran 30 productos por pagina
        for i in range(1,31):
            try:

                #En cada iteracion, la variable que almacenara todos los datos de UN PRODUCTO, se reestablece y se vacia, para poder almacenar los datos del producto analizado en esa iteracion
                datosProducto = []
                datosProducto.clear
                
                idFarmacia = 2
                datosProducto.append(idFarmacia)

                descripcion = (driver.find_element(By.XPATH,f'//*[@id="left-area"]/ul/li[{i}]/a[1]/h2')).text
                datosProducto.append(descripcion.upper())
                
                precio = (driver.find_element(By.XPATH,f'//*[@id="left-area"]/ul/li[{i}]/a[1]/span[2]/span/bdi')).text
                datosProducto.append(int(precio.split("$")[1].replace(".", "")))
                
                linkProducto = (driver.find_element(By.XPATH,f'//*[@id="left-area"]/ul/li[{i}]/a[1]')).get_attribute('href')
                datosProducto.append(linkProducto)
                
                linkFoto = (driver.find_element(By.XPATH,f'//*[@id="left-area"]/ul/li[{i}]/a[1]/span[1]/img')).get_attribute('src')
                datosProducto.append(linkFoto)

                lista.append(datosProducto)
                
                print(f"\nFarmacia =      {idFarmacia}")
                print(f"Descripcion =   {descripcion}")
                print(f"Precio =        {precio}")
                print(f"Link =          {linkProducto}")
                print(f"Foto =          {linkFoto}")
                print(f"Pagina =        {numeroPagina}")

            except:
                #Aqui se evalua el caso de que no haya podido completar la extraccion de datos porque no haya la cantidad habitual de productos por pagina (si una pagina tiene menos de 8 productos, como la ultima, por ejemplo) 
                pass
    print("\nProceso de extraccion finalizado en Eco")