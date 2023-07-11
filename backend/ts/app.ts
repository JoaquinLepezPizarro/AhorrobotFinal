//framework para trabajar en js
const express = require('express')
const app = express()
const cors = require('cors');
app.use(cors());

//Conección con servidor local
const configuracion={
    hostname: "127.0.0.1",
    port: 3000,
}

//Conección con base de datos
const mysql = require('mysql');
let connection = mysql.createConnection({
  host     : '127.0.0.1',
  user     : 'root',
  password : '',
  port: 3306,
  database : 'ahorrobot'
});

connection.connect(function(err:any) {
    if (err) {
      console.error('ERROR AL CONECTARSE A LA BD: ' + err.stack);
      return;
    }
   
    console.log('CONECCION ESTABLECIDA CON EXITO ' + connection.threadId);
  });

//OBTIENE UNA LISTA DEL PRODUCTO BUSCADO
app.get('/productos_vigentes/:nombreProducto', (req:any, res:any) => {
  let nombreProducto = req.params.nombreProducto;
  connection.query("SELECT * FROM productos_vigentes WHERE MATCH(descripcion) AGAINST (?) ORDER BY precio ASC", nombreProducto, function(error:any, results:any, fields:any){
    //console.log(`El nombre del producto es: ${nombreProducto}`);  
    res.send(JSON.stringify(results));
  });
})

//OBTIENE TODO LO QUE ESTE EN LA TABLA FARMACIAS (ID, NOMBRE Y FOTO DE LAS FARMACIAS)
app.get('/farmacias', (req:any, res:any) => {
  connection.query("SELECT * FROM farmacias", function(error:any, results:any, fields:any) {  
  res.send(JSON.stringify(results));
    //console.log(`El id es ${idFarmacia}`); 
  });
});

app.listen(configuracion, () => {
  console.log(`Example app listening on port ${configuracion.port}`)
})

app.use(cors());