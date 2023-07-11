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



def scrollDown():
    """Esta funcion permite cargar todos los elementos de la pagina hacia abajo, realizando el scrolldown que permite que los productos queden visibles para asi extraer los datos"""
    
    print("\nRealizando proceso de scroll down...")
    cantidadIteraciones = 0

    while True:
        #Se compara cual era la pagina antes de realizar el cambio de pagina para evaluar si esta es distinta o si es la misma (en el caso de que ya sea la ultima)
        paginaAntes = driver.current_url
        try:
            botonMostrarMas = (driver.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div/div[2]/div/div/section/div[2]/div/div[5]/section/div/div/div/div/a/div'))
            
            #Aqui se consideran dos formatos para clickear el boton "Mostrar Mas" debido a que ocasionalmente el boton dejaba de ser clickeable
            try:
                driver.execute_script("arguments[0].click();", botonMostrarMas)
            except:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[1]/div/div[2]/div/div/section/div[2]/div/div[5]/section/div/div/div/div/a/div'))).click()
            
            #Se da tiempo a que cargue la pagina. En equipos con conexiones mas lentas este numero debe aumentarse. Fue inicializado en un alto valor considerando una conexion lenta, para disminuir cantidad de fallos.
            cantidadIteraciones += 1
            tiempoDeEspera = 10 + cantidadIteraciones // 5
            print(f"Esperando {tiempoDeEspera} segundos para que carguen los productos de la pagina N°{cantidadIteraciones + 1}")
            sleep(tiempoDeEspera)
            
            paginaDespues = driver.current_url
            if paginaDespues == paginaAntes:
                print("Scroll down completado...")
                break
        except:
            try:
                botonMostrarMas = (driver.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div/div[3]/div/div/section/div[2]/div/div[3]/div/div[2]/div/div[3]/div/div/div/div/div/a'))
                
                #Aqui se consideran dos formatos para clickear el boton "Mostrar Mas" debido a que ocasionalmente el boton dejaba de ser clickeable
                try:
                    driver.execute_script("arguments[0].click();", botonMostrarMas)
                except:
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[1]/div/div[3]/div/div/section/div[2]/div/div[3]/div/div[2]/div/div[3]/div/div/div/div/div/a'))).click()
                
                #Se da tiempo a que cargue la pagina. En equipos con conexiones mas lentas este numero debe aumentarse. Fue inicializado en un alto valor considerando una conexion lenta, para disminuir cantidad de fallos.
                cantidadIteraciones += 1
                tiempoDeEspera = 10 + cantidadIteraciones // 5
                print(f"Esperando {tiempoDeEspera} segundos para que carguen los productos de la pagina N°{cantidadIteraciones + 1}")
                sleep(tiempoDeEspera)
                
                paginaDespues = driver.current_url
                if paginaDespues == paginaAntes:
                    print("Scroll down completado...")
                    break
            except:
                print("Scroll down completado...")
                break


def scrapingCategoriaSimi(link, lista):
    """Esta funcion permite realizar la extraccion de datos a UNA CATEGORIA. Debe ser repetido por cada categoria."""

    driver.get(link)
    sleep(10)
    scrollDown()
    numeroProducto = 0

    #Se consideran dos xpath distintos ya que la pagina presenta dos formatos ocasionalmente
    try:
        cantidadProductos = (driver.find_element(By.XPATH,f'/html/body/div[2]/div/div[1]/div/div[2]/div/div/section/div[2]/div/div[3]/section/div/div/div/span')).text
        cantidadProductos = int(cantidadProductos.split()[0])

    except:
        cantidadProductos = (driver.find_element(By.XPATH,f'/html/body/div[2]/div/div[1]/div/div[3]/div/div/section/div[2]/div/div[3]/div/div[2]/div/div[1]/div/div/div/div/div/div/div/div/div[1]/div/span')).text
        cantidadProductos = int(cantidadProductos.split()[0])

    for i in range(cantidadProductos + 1):
        try:
            disponibilidad = (driver.find_element(By.XPATH,f'//*[@id="gallery-layout-container"]/div[{i+1}]/section/a/article/div[4]/div/div[2]/button/div')).text
            if disponibilidad == "Añadir al carrito" or disponibilidad == "AÑADIR AL CARRITO": 
                numeroProducto += 1
                datosProducto = []
                datosProducto.clear

                idFarmacia = 1
                datosProducto.append(idFarmacia)

                descripcion = (driver.find_element(By.XPATH,f'//*[@id="gallery-layout-container"]/div[{i+1}]/section/a/article/div[2]/h3/span')).text
                datosProducto.append(descripcion.upper())
                
                precio = (driver.find_element(By.XPATH,f'//*[@id="gallery-layout-container"]/div[{i+1}]/section/a/article/div[3]/div/div[2]/span/span/span')).text
                datosProducto.append(int(precio.split("$")[1].replace(".", "")))
                
                linkProducto = (driver.find_element(By.XPATH,f'//*[@id="gallery-layout-container"]/div[{i+1}]/section/a')).get_attribute('href')
                datosProducto.append(linkProducto)
                
                linkFoto = (driver.find_element(By.XPATH,f'//*[@id="gallery-layout-container"]/div[{i+1}]/section/a/article/div[1]/div[1]/div/div/img')).get_attribute('src')
                datosProducto.append(linkFoto)

                lista.append(datosProducto)

                print(f"\nFarmacia =      {idFarmacia}")
                print(f"N° Producto =   {numeroProducto}")
                print(f"Descripcion =   {descripcion}")
                print(f"Precio =        {precio}")
                print(f"Link =          {linkProducto}")
                print(f"Foto =          {linkFoto}")
        except:
            #Aqui se evalua el caso de que no haya podido completar la extraccion de datos porque no haya la cantidad habitual de productos por pagina (si una pagina tiene menos de 8 productos, como la ultima, por ejemplo) 
            pass



def scrapingSimi(lista):
    """Esta funcion permite realizar de forma iterativa la extraccion de datos en cada categoria"""

    print("\n\n\nIniciando proceso de scraping a Simi...")

    #Se realiza la extraccion de datos de cada categoria
    print("\n\nExtrayendo datos de categoria DR SIMI...")
    scrapingCategoriaSimi("https://www.drsimi.cl/dr-simi", lista)

    print("\n\nExtrayendo datos de categoria DISPOSITIVOS...")
    scrapingCategoriaSimi("https://www.drsimi.cl/dispositivos", lista)

    print("\n\nExtrayendo datos de categoria SUPLEMENTOS Y ALIMENTOS...")
    scrapingCategoriaSimi("https://www.drsimi.cl/suplementos-y-alimentos", lista)

    print("\n\nExtrayendo datos de categoria MEDICAMENTOS...")
    scrapingCategoriaSimi("https://www.drsimi.cl/medicamento", lista)

    print("\n\nProceso de extraccion finalizado en Simi")