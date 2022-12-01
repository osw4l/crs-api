# CRS-API

Requerimientos

- Tener instalado Docker Y Docker compose
- Sistema operativo: Unix, Linux o Mac


El objetivo de esta prueba es crear un servicio que permita:
- Búsqueda de disponibilidad, mediante el cual se pueda consultar si hay habitaciones disponibles, es decir con cupo y precio, para un hotel y rango de fechas dado.
- Consultar y modificar la información básica necesaria para cargar la información de propiedades (hotel, habitaciones) e inventario (tarifas y precios).

Para levantar el proyecto se debe clonar de este repositorio y luego navegar hasta el en el terminal

<img width="804" alt="Captura de Pantalla 2022-11-30 a la(s) 11 23 26 p m" src="https://user-images.githubusercontent.com/8086136/204965409-b9aa6bb7-bbf9-4807-8843-7b606aa69945.png">

para correr el proyecto solo se debe hacer uso de los comandos escritos en el Makefile, tiene comandos tanto para desarrollo, tests, cobertura, creacion de usuarios administradores, reiniciar contenedores y mas

### Levantar el proyecto

para levantar el proyecto, solo se debe correr en la raiz del mismo el siguiente comando:

`make up`

este comando construirá la imagen de docker de este proyecto, ademas instalará de manera automatizada las dependencias, ejecutará las migraciones y cargará los archivos estáticos

<img width="812" alt="Captura de Pantalla 2022-11-30 a la(s) 11 33 02 p m" src="https://user-images.githubusercontent.com/8086136/204966400-ba12119d-42fd-4381-be6f-fcfbd9312ad8.png">

Los contenedores son:
- backend (contiene el api)
- elastic (contiene elastic search para hacer búsquedas sencillas y evitar golpear la base de datos)
- postgres-skeleton-db (contiene la base de datos en postgres)

nuestra imagen con los contenedores por dentro seria esta

![Captura de Pantalla 2022-11-30 a la(s) 11 27 58 p m](https://user-images.githubusercontent.com/8086136/204965868-97f8d7d4-4ee5-49b6-a285-54336854e979.png)

el backend está corriendo en el puerto 6060, en esta dirección -> http://0.0.0.0:6060/

una vez le des click al enlace vas a ver esta pantalla -> 

![Captura de Pantalla 2022-11-30 a la(s) 11 35 03 p m](https://user-images.githubusercontent.com/8086136/204966631-45c8d41c-82b0-4268-a48b-232c1ec3c11c.png)

si haces un poco mas de scroll serás capaz de ver todos

![Captura de Pantalla 2022-11-30 a la(s) 11 35 57 p m](https://user-images.githubusercontent.com/8086136/204966703-4ca43a42-0bae-497b-bcfa-e1c8a85add94.png)

Un poco mas abajo se encuentran los modelos que contienen la definición de las estructuras de datos que vamos a manejar en el api

![Captura de Pantalla 2022-11-30 a la(s) 11 37 08 p m](https://user-images.githubusercontent.com/8086136/204966827-a36a11c1-c08f-4f0f-beb3-e99567afcfeb.png)

### Setup de datos

este proyecto tiene 2 maneras de crear data, por el api docs de swagger (que es bastante intuitiva) y por el admin de Django, la segunda me gusta más porque es bastante visual y mas directa a la hora de insertar los datos.

Para acceder al administrador solo basta con ir a este link http://0.0.0.0:6060/admin/

![Captura de Pantalla 2022-11-30 a la(s) 11 40 51 p m](https://user-images.githubusercontent.com/8086136/204967233-3825c906-db76-49d0-b50f-f5dc1f3f880d.png)

Para crear un usuario administrador debemos ir al terminar y escribir `make admin`, recuerda presionar enter cuando termines un paso, tambien recuerda que por seguridad no se muestra la longitud de la contraseña por lo que cuando termines de escribir cualquiera de los campos de password deberas presionar enter

<img width="677" alt="Captura de Pantalla 2022-11-30 a la(s) 11 45 04 p m" src="https://user-images.githubusercontent.com/8086136/204967756-a3b306dd-6b0b-458f-afb6-0886fe994536.png">

con nuestro usuario ya creado podremos volver al admin http://0.0.0.0:6060/admin/ e ingresar las credenciales que creamos para iniciar sesión

![Captura de Pantalla 2022-11-30 a la(s) 11 45 57 p m](https://user-images.githubusercontent.com/8086136/204967858-c7e10474-9e88-458d-9cfa-96426336422a.png)

![Captura de Pantalla 2022-11-30 a la(s) 11 46 12 p m](https://user-images.githubusercontent.com/8086136/204967881-216d6e62-e37c-4759-99de-e6e18db2b732.png)

una vez dentro nos dirigimos a Hotels y presionamos Add + para crear nuestro hotel y sus habitaciones

![Captura de Pantalla 2022-11-30 a la(s) 11 47 51 p m](https://user-images.githubusercontent.com/8086136/204968056-4e4b1fc9-d331-4445-9951-1a4a5297ebfa.png)

Hemos agregado un hotel con una habitación, podemos seguir agregando mas habitaciones en el futuro

![Captura de Pantalla 2022-11-30 a la(s) 11 56 52 p m](https://user-images.githubusercontent.com/8086136/204969012-5ebc1495-fb25-4d3d-a976-810ca2f47932.png)

El campo deleted hace referencia a un campo marcado que sirve para simbolizar un borrado logico, cuando se encuentra en true el registro no estará visible por fuera del admin, quiere decir que no será listado tampoco en ninguna de las apis

En caso de eliminación por error se podrán restablecer los objetos afectados sin problema, si se elimina un hotel, todos los registros asociados al hotel dejarán de mostrarse en la api

![Captura de Pantalla 2022-11-30 a la(s) 11 58 36 p m](https://user-images.githubusercontent.com/8086136/204969248-a6690ab6-01be-4426-8f38-9bda696f26ed.png)

Ahora vamos a crear un Rate, que pertenece solo a una habitación y tiene todos los precios y la ocupación para fechas especificas

![Captura de Pantalla 2022-12-01 a la(s) 12 02 16 a m](https://user-images.githubusercontent.com/8086136/204969726-46bc204f-f1a5-4375-97c5-6bef0bb56fa0.png)

podremos agregar tantos inventarios queramos, la única regla es que no se deben repetir fechas, cada fecha debe ser única en cada inventario asociado a un rate

con la data configurada podemos ver la información usando la ui de swagger http://0.0.0.0:6060/

![Captura de Pantalla 2022-12-01 a la(s) 12 08 08 a m](https://user-images.githubusercontent.com/8086136/204970442-4226a46a-172c-4ce0-9970-8ec810685118.png)

![Captura de Pantalla 2022-12-01 a la(s) 12 09 12 a m](https://user-images.githubusercontent.com/8086136/204970555-0b596a72-2d44-46d6-8487-c3655aefb015.png)

![Captura de Pantalla 2022-12-01 a la(s) 12 09 30 a m](https://user-images.githubusercontent.com/8086136/204970594-863502fd-aeb3-4c5f-8d13-6be11f3198be.png)

Con data ingresada ya estamos listos para probar el api que nos genera este esquema de datos

![Captura de Pantalla 2022-12-01 a la(s) 12 10 22 a m](https://user-images.githubusercontent.com/8086136/204970758-e68417d0-bb45-4e8a-a871-b7c056812f8c.png)

es esta

![Captura de Pantalla 2022-12-01 a la(s) 12 11 06 a m](https://user-images.githubusercontent.com/8086136/204970807-d0cad58e-bfc4-49b5-adbf-f50cf96484de.png)

![Captura de Pantalla 2022-12-01 a la(s) 12 11 59 a m](https://user-images.githubusercontent.com/8086136/204970964-0d54b360-040a-47ee-bcf4-09427495d0d4.png)

![Captura de Pantalla 2022-12-01 a la(s) 12 12 21 a m](https://user-images.githubusercontent.com/8086136/204971016-d5d12578-c9ee-4b09-85a9-f23048e01cb1.png)

### Anotaciones varias
- Todos los endpoints tienen las operaciones crud con posibilidad de reversión en el delete
- Toda la data de los endpoints get que listan objetos, contienen paginación
- Los filtros de los objetos eliminados se hacen a través del **BookingModelManager**
- Todos los endpoints devuelven la información con el esquema que promete excepto el de la disponibilidad porque los atributos no son claves fijas sino que son claves dinámicas armadas a partir de los valores que van arrojando las habitaciones, rates y más
- El unico endpoint que tiene tests es el de Availability y el de Hotels
- se hicieron tests de integración para probar los servicios
- en el servicio de availability solo se hacen 2 queries
- hay una clase de paginación propia que puede modificarse a conveniencia
- todas las apis a diferencia de la de disponibilidad contienen buscador y filtros que pueden agregarse a conveniencia

- la primera linea roja es un registro de una clase que permite crear nuevos validadores para los tipos de datos esperados en los parametros de las urls 
![Captura de Pantalla 2022-12-01 a la(s) 12 23 06 a m](https://user-images.githubusercontent.com/8086136/204972364-6762de86-fe30-4f20-bc9f-6beaae65df2f.png)

se usó django-extensions para obtener los alias de las urls para evitar llamarlas explicitamente
 
<img width="998" alt="Captura de Pantalla 2022-11-30 a la(s) 5 25 31 p m" src="https://user-images.githubusercontent.com/8086136/204972813-aedf3247-c15b-4f3d-ae2a-41320aab6c08.png">


Estas son las tests que tiene el código actualmente

![Captura de Pantalla 2022-12-01 a la(s) 12 19 04 a m](https://user-images.githubusercontent.com/8086136/204971830-c7ba2a16-548a-439f-973a-53e46ef2d59c.png)

### cosas que hubiese querido hacer
- mejorar la estructura de los serializadores
- optimizar las queries
- testear todos los serializer
- testear todas las vistas
- testear todos los modelos
- testear todos los managers y querysets
- testear el decorador action_paginated para paginar actions en los viewsets como los rooms de los hotels


