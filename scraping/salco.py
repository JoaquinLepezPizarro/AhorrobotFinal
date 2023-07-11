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



def esUltimaPagina():
    """Esta funcion permite analizar si se llego a la ultima pagina o no para continuar la extraccion de datos"""

    #Esta funcion intentara ubicar la posicion del boton "Ultima" para indicar que era la ultima
    numeroBotonPagina = 1
    try:
        while True:

            #Ira avanzando en los botones de la pagina hasta que encuentre el que indica la ultima, el cual solo saldra como "Ultima" si efectivamente es la ultima
            textoBotonPagina = (driver.find_element(By.XPATH,f'//*[@id="content"]/nav/ul/li[{numeroBotonPagina}]/a')).text
            if textoBotonPagina == "Última":
                return False
            else:
                numeroBotonPagina = numeroBotonPagina + 1
    except:
        return True
    


def avanzarPaginaSalco():
    """Esta funcion permite ir avanzando en las paginas de productos de la farmacia"""

    print("\nIntentando acceder a pagina siguiente...")
    numeroBotonPagina = 1
    while True:
        try:
            textoBotonPagina = (driver.find_element(By.XPATH,f'//*[@id="content"]/nav/ul/li[{numeroBotonPagina}]/a')).text
            
            #Se intenta encontrar el string "»" que indica que ese boton es el que conduce a la pagina siguiente
            if textoBotonPagina == "»":
                botonSiguiente = (driver.find_element(By.XPATH,f'//*[@id="content"]/nav/ul/li[{numeroBotonPagina}]/a'))
                
                #Aca se ejecuta una instruccion de JS debido a que el boton no era clickeable con Selenium
                driver.execute_script("arguments[0].click();", botonSiguiente)
                
                #Se indica una cantidad alta de tiempo para evitar fallos. Este valor puede modificarse
                sleep(5)
                break
            else:
                numeroBotonPagina = numeroBotonPagina + 1
        except:
            print("\nPagina siguiente no encontrada. Ultima pagina completada")
            break



def scrapingCategoriaSalco(link, lista):
    """Esta funcion permite hacer la extraccion de datos a UNA CATEGORIA. El metodo debe repetirse iterativamente con cada categoria"""
    
    driver.get(link)
    
    #Se indica una cantidad alta de tiempo para evitar fallos. Este valor puede modificarse
    sleep(5)

    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="search-result"]/div[1]/div[2]/div/div[2]/div[2]/div/div/select/option[4]'))).click()
    
    #Se indica una cantidad alta de tiempo para evitar fallos. Este valor puede modificarse
    sleep(5)

    #Se indica que esta NO es la ultima pagina, hasta que se demuestre lo contrario
    ultimaPagina = False

    while ultimaPagina == False:

        #Se inicializa en cero para ir contabilizando la cantidad de productos evaluados y asi saber cuando detenerse
        productoPagina = 0

        print("\nObteniendo datos de productos de la pagina actual")
        while productoPagina <= 96:
            try:
                productoPagina = productoPagina + 1

                datosProducto = []
                datosProducto.clear
                
                idFarmacia = 3
                datosProducto.append(idFarmacia)

                descripcion = (driver.find_element(By.XPATH,f'//*[@id="content"]/div/div[1]/ul/li[{productoPagina}]/div/div/div/div[2]/a/span[2]')).text
                datosProducto.append(descripcion.upper())
                
                #Se consideran dos xpath distintos debido a que la pagina tiene mas de un formato
                try:
                    precio = (driver.find_element(By.XPATH,f'//*[@id="content"]/div/div[1]/ul/li[{productoPagina}]/div/div/div/div[2]/a/div[2]/div/div/div[2]')).text
                    datosProducto.append(int(precio.split("$")[1].replace(".", "")))
                except:
                    precio = (driver.find_element(By.XPATH,f'//*[@id="content"]/div/div[1]/ul/li[{productoPagina}]/div/div/div/div[2]/a/div[2]/div/div')).text
                    datosProducto.append(int(precio.split("$")[1].replace(".", "")))
                
                linkProducto = (driver.find_element(By.XPATH,f'//*[@id="content"]/div/div[1]/ul/li[{productoPagina}]/div/div/div/div[1]/a')).get_attribute('href')
                datosProducto.append(linkProducto)

                linkFoto = (driver.find_element(By.XPATH,f'//*[@id="content"]/div/div[1]/ul/li[{productoPagina}]/div/div/div/div[1]/a/img')).get_attribute('src')
                datosProducto.append(linkFoto)

                lista.append(datosProducto)
                
                print(f"\nFarmacia =      {idFarmacia}")
                print(f"Descripcion =   {descripcion}")
                print(f"Precio =        {precio}")
                print(f"Link =          {linkProducto}")
                print(f"Foto =          {linkFoto}")
            
            except:
                #Aqui se evalua el caso de que no haya podido completar la extraccion de datos porque no haya la cantidad habitual de productos por pagina (si una pagina tiene menos de 8 productos, como la ultima, por ejemplo) 
                break
        
        print("\nIntentando cargar pagina siguiente...")
        avanzarPaginaSalco()
        ultimaPagina = esUltimaPagina()



def scrapingSalco(lista):
    print("\n\n\nIniciando proceso de scraping a Salco...")

    #Se realiza la extraccion de datos de cada categoria
    print("\n\nExtrayendo datos de categoria DERMOCOACHING...")
    scrapingCategoriaSalco("https://salcobrand.cl/t/dermocoaching", lista)

    print("\n\nExtrayendo datos de categoria CLINIQUE...")
    scrapingCategoriaSalco("https://salcobrand.cl/t/clinique", lista)

    print("\n\nExtrayendo datos de categoria MEDICAMENTOS...")
    scrapingCategoriaSalco("https://salcobrand.cl/t/medicamentos", lista)

    print("\n\nExtrayendo datos de categoria CUIDADO PERSONAL...")
    scrapingCategoriaSalco("https://salcobrand.cl/t/cuidado-personal", lista)

    print("\n\nExtrayendo datos de categoria VITAMINAS Y SUPLEMENTOS...")
    scrapingCategoriaSalco("https://salcobrand.cl/t/vitaminas-y-suplementos", lista)

    print("\n\nExtrayendo datos de categoria BELLEZA...")
    scrapingCategoriaSalco("https://salcobrand.cl/t/belleza", lista)

    print("\n\nExtrayendo datos de categoria INFANTIL Y MAMA...")
    scrapingCategoriaSalco("https://salcobrand.cl/t/infantil-y-mama", lista)

    print("\n\nExtrayendo datos de categoria CUIDADO DE LA SALUD...")
    scrapingCategoriaSalco("https://salcobrand.cl/t/cuidado-de-la-salud", lista)

    print("\n\nExtrayendo datos de categoria ADULTO MAYOR...")
    scrapingCategoriaSalco("https://salcobrand.cl/t/adulto-mayor", lista)

    print("\n\nExtrayendo datos de categoria MARCAS EXCLUSIVAS...")
    scrapingCategoriaSalco("https://salcobrand.cl/t/marcas-exclusivas", lista)

    print("\n\nExtrayendo datos de categoria EMPRENDEDORES...")
    scrapingCategoriaSalco("https://salcobrand.cl/t/emprendedores", lista)

    print("\n\nExtrayendo datos de categoria SALES...")
    scrapingCategoriaSalco("https://salcobrand.cl/products/sales", lista)

    print("\n\nProceso de extraccion finalizado en Redfarma")