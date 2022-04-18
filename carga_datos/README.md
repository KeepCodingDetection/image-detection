# **CARGA DE DATOS**

Una vez que las funciones de recolección de precios (scrapping) y de detección (predicciones) se realizan, dejarán sus resultados dentro de un bucket generado en Google Cloud Storage con ficheros de formatos CSV o XLSX. Es entonces cuando se realiza una función para cargar estos datos en una BD que se ha generado con PostgreSQL en un servicio de Google Cloud SQL.

La estrategia de contar con una Base de Datos para esta información es la de tener de manera versátil el acceso a los datos, además de contar con un historial de dicha información para su utilización en diferentes puntos de la aplicación.

La elección de PostgreSQL es debido, en primer lugar, a que se trata de un sistema de gestión de Base de Datos Relacional de licencia libre, así como la potencia de procesamiento con la que cuenta. Este sistema también cuenta con funciones para trabajar con información JSON, aspecto que en futuras evoluciones de la aplicación será muy conveniente.

Actualmente se cuentan con 4 tablas para la aplicación:

- Tabla Store. En esta tabla se almacena la información de precios
obtenida a través de la función de scraping.
   
- Tabla Detección. Para cada detección realizada por la función correspondiente se genera un fichero que será almacenado en esta
tabla. Se indica un ID por cada detección, y por cada clase detectada
en una imagen se genera un registro con el número de elementos
detectados de dicha clase.
   
- Tabla Shoplist. Esta tabla almacena la lista de compra de los productos que el usuario requiere para una determinada fecha.
   
- Tabla Equivalencies. Dado que los precios de la tabla Store se determinan por kilogramos, esta tabla se genera para determinar la
 equivalencia en piezas de cada producto por kilo.

La base de datos se ha generado en un servicio Google Cloud SQL para contar con la premisa de accesibilidad, además de las ventajas que ofrece un servicio Cloud de estas características, tales como los servicios de mantenimiento de servidores, escalabilidad y seguridad.
