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

    print("\nAnalizando si llego a la ultima pagina...")

    #Con esta instruccion se puede obtener el codigo completo de la pagina
    codigoPagina = driver.page_source
    
    #Se evalua si dentro del codigo de la pagina se encuentra el string que indica que no hay mas paginas para la extraccion
    if "NO HAY PRODUCTOS" in codigoPagina or "No hay productos" in codigoPagina:
        print("\nUltima pagina completada")
        return True
    else:
        print("\nQuedan mas paginas, extrayendo datos de la pagina siguiente...")
        return False

    

def scrapingRedfarma(lista):
    """Esta funcion, por si sola, realiza la extraccion de datos de todos los productos de todas las paginas de productos de Redfarma"""

    print("\n\n\nIniciando proceso de scraping a Redfarma...")

    #Se inicializa el numero de pagina en 0 para que en cada iteracion este numero aumente. Se usa unicamente para mostrar en consola informacion sobre el proceso de extraccion
    numeroPagina = 0
    
    #Se inicializa el valor de ultima pagina en falso, considerando que la pagina tiene al menos un producto, hasta que se demuestre lo contrario
    ultimaPagina = False

    while ultimaPagina == False:
        numeroPagina = numeroPagina + 1

        #Aqui se usa de forma literal el numero de pagina
        driver.get(f"https://www.redfarma.cl/productos?pagina={numeroPagina}")
        
        #Se da tiempo a que cargue la pagina. En equipos con conexiones mas lentas este numero debe aumentarse. Fue inicializado en un alto valor considerando una conexion lenta, para disminuir cantidad de fallos.
        sleep(5)

        #Se evalua si la ultima pagina analizada era efectivamente la ultima pagina con productos
        ultimaPagina = esUltimaPagina()

        #En caso de que no haya sido la ultima pagina con productos, se realiza el proceso de scraping de los datos de productos que quedan por extraer
        if ultimaPagina == False:
            print(f"\nObteniendo datos de productos de la pagina {numeroPagina}")
            
            #Se considera un rango de 1 a 10 debido a que se muestran 8 productos por pagina. En todos los casos evaluados los indices de productos parten en 2, pero se considera el 1 por si llegase a cambiar en el tiempo.
            for i in range(1,10):
                try:

                    #En cada iteracion, la variable que almacenara todos los datos de UN PRODUCTO, se reestablece y se vacia, para poder almacenar los datos del producto analizado en esa iteracion
                    datosProducto = []
                    datosProducto.clear
                    
                    idFarmacia = 4
                    datosProducto.append(idFarmacia)

                    descripcion = (driver.find_element(By.XPATH,f'//*[@id="listado-productos-home"]/div[{i}]/div/div[2]/div[2]/a')).text
                    datosProducto.append(descripcion.upper())

                    #Se consideran varios xpath, segun si es precio oferta, precio normal o precio web. La pagina presenta muchos formatos para este campo, por lo que se evaluan todos los casos en orden de prioridad.
                    try:
                        precio = (driver.find_element(By.XPATH,f'//*[@id="listado-productos-home"]/div[{i}]/div/div[3]/div/div[1]/div')).text
                    except:
                        try:
                            precio = (driver.find_element(By.XPATH,f'//*[@id="listado-productos-home"]/div[{i}]/div/div[3]/div/div[2]')).text
                        except:
                            try:
                                precio = (driver.find_element(By.XPATH,f'//*[@id="listado-productos-home"]/div[{i}]/div/div[3]/div/div[1]')).text
                            except:
                                try:
                                    precio = (driver.find_element(By.XPATH,f'//*[@id="listado-productos-home"]/div[{i}]/div/div[3]/div/div[1]/span[2]')).text
                                except:
                                    precio = (driver.find_element(By.XPATH,f'//*[@id="listado-productos-home"]/div[{i}]/div/div[3]/div/div[3]')).text
                                    
                    datosProducto.append(int(precio.split("$")[1].replace(".", "")))
                    
                    linkProducto = (driver.find_element(By.XPATH,f'//*[@id="listado-productos-home"]/div[{i}]/div/div[2]/div[2]/a')).get_attribute('href')
                    datosProducto.append(linkProducto)
                    
                    linkFoto = (driver.find_element(By.XPATH,f'//*[@id="listado-productos-home"]/div[{i}]/div/div[1]/a/img')).get_attribute('src')
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

            print("\nIntentando cargar pagina siguiente...")
        
        #En caso de que si haya sido la ultima pagina con productos, se cambia el valor de ultimaPagina para finalizar el ciclo y el proceso de extraccion en Redfarma
        else:    
            ultimaPagina = True
            print("\nProceso de extraccion finalizado en Redfarma")