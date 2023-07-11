En este archivo encontrara las indicaciones necesarias para poder ejecutar esta version de Ahorrobot en su equipo.
Antes de empezar, es importante que tome en cuenta lo siguiente:
	- El sistema esta diseñado para ser utilizado en sistema operativo Windows 10 u 11
	- No se asegura su correcta ejecucion en otros sistemas operativos
	- Se requiere conexion a internet de forma ininterrumpida durante la extraccion de datos
	- Una vez inciada la extraccion, no apague el equipo 
	- No cierre ninguna de las ventanas de chromedriver que se abran durante el proceso de scraping
	- El sistema cuenta con un modulo de instalacion automatica de librerias (se ejecuta automaticamente)

*NOTA: A pesar de haber seguido todas las indicaciones anteriores, no se asegura al 100% el funcionamiento del bot de extraccion de datos pues este puede ver variado su rendimiento y funcionamiento en funcion de factores externos (corte de luz, de internet, apagado abrupto del equipo, etc) e internos (falla del equipo, equipo lento, interrupciones del sistema operativo, etc). Incluso cambios abruptos en la velocidad de internet podrian ocasionar que hayan datos que no se capturen en la extraccion. Por esto es recomedable hacer la extraccion como accion unica en el equipo, no realizar ninguna otra actividad en el equipo mientras se realiza la extraccion y realizarla de noche.


--------------------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------
--------------PREPARATIVOS-------------------
---------------------------------------------
Para el sistema de extracción de datos:
1. Debe tener instala da la ultima version de Python 3 o superior

Para compilar el sistema extracción de datos:  *Debe tener en consideración que cada ejecución debe ser en sus respectivas carpetas
Escribir en consola el comando python main.py

Para el sistema web:
1. Debe tener instalado Node JS
2. Debe tener instalado angular, alguna de las distribuciones de la version 16 o superior
3. Debe tener instalado Typescript
4. Debe tener instalado la app "Xampp" o similar


Para compilar el sistema web: 	*Debe tener en consideración que cada ejecución debe ser en sus respectivas carpetas
Front-end: ng serve
Back-end: tcs -watch y en otra consola ejecutar node js/app.js

