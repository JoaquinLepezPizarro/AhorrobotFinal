import mysql.connector
from datetime import *


conexionBD = mysql.connector.connect(
    host="localhost", 
    user="root", 
    passwd="", 
    database="ahorrobot"
)



def respaldarTablaProductos():
    print(f"\nRespaldando tabla de productos vigentes...")
    #fechaHoy = datetime.now().strftime('%Y-%m-%d')
    fechaHoy = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
    nombreTablaProductos = f"productos_{fechaHoy}"
    cursor = conexionBD.cursor()
    consulta = f"CREATE TABLE `{nombreTablaProductos}` AS SELECT * FROM productos_vigentes"
    cursor.execute(consulta)
    conexionBD.commit()
    cursor.close()



def vaciarTablaPoductos():
    print(f"\nVaciando la tabla de productos vigentes...")
    cursor = conexionBD.cursor()
    consulta = "TRUNCATE TABLE productos_vigentes"
    cursor.execute(consulta)
    conexionBD.commit()
    cursor.close()



def poblarTablaProductos(lista):
    print(f"\nAñadiendo los datos extraidos en la tabla de productos vigentes...")
    for producto in range(len(lista)):
        cursor = conexionBD.cursor()
        consulta = "INSERT INTO productos_vigentes (idFarmacia, descripcion, precio, linkProducto, linkFoto) VALUES (%s, %s, %s, %s, %s)"
        
        #En caso de que el producto no tenga foto, se le asigna una imagen generica que indica que el producto no tiene foto
        if lista[producto][4] == None or lista[producto][4] == "None":
            lista[producto][4] = "https://www.bicifan.uy/wp-content/uploads/2016/09/producto-sin-imagen.png"
        datos = (lista[producto][0], lista[producto][1], lista[producto][2], lista[producto][3], lista[producto][4])
        cursor.execute(consulta, datos)
        conexionBD.commit()
        cursor.close()



def actualizarTablaProductos(lista):
    print(f"\nIniciando proceso de actualizacion de la base de datos...")
    vaciarTablaPoductos()
    poblarTablaProductos(lista)
    respaldarTablaProductos()
    conexionBD.close()



def mostrarLista(lista):
    """Esta funcion es unicamente para uso interno, para hacer pruebas"""
    print("\n\n\nLISTADO COMPLETO DE PRODUCTOS ANTES DE GUARDAR EN BD")
    for producto in range(len(lista)):
        print(f"\nProducto n°:      {producto}")
        print(f"    ID Farmacia:    {lista[producto][0]}")
        print(f"    Descripcion:    {lista[producto][1]}")
        print(f"    Precio:         {lista[producto][2]}")
        print(f"    Link Producto:  {lista[producto][3]}")
        print(f"    Link Foto:      {lista[producto][4]}")


"""
    Datos que tendra cada producto, EN ORDEN:
        idProducto      automatico (autoincremental en la BD)
        idFarmacia      lista[producto][0]
        descripcion     lista[producto][1]
        precio          lista[producto][2]
        linkProducto    lista[producto][3]
        linkFoto        lista[producto][4]
"""