from librerias import *
# instalarLibrerias()

import chromedriver_autoinstaller
chromedriver_autoinstaller.install()

from simi import *
from eco import *
from salco import *
from redfarma import *
from ahumada import *
from funcionesBD import *


"""
ID de farmacias, EN ORDEN:
    FARMACIA    ID
    simi        1
    eco         2
    salco       3
    redfarma    4
    ahumada     5
"""


lista = []

print("\n\n\nIniciando el proceso de extraccion de datos en las distintas farmacias...")
scrapingSimi(lista)
scrapingEco(lista)
scrapingSalco(lista)
scrapingRedfarma(lista)
scrapingAhumada(lista)

print("\n\n\nExtraccion de datos realizada con exito")

print("\n\n\nActualizando base de datos...")
actualizarTablaProductos(lista)

print("\n\n\nProceso de actualizacion base de datos completado. Fin de la ejecucion del bot de extraccion.")