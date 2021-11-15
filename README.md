# PI-Practicas

### Prácticas de Programación Integrativa
### Facultade de Informática UDC - Curso 2020-21

Jose Ángel Álvarez Sánchez - j.alvarez.sanchez@udc.es

Ismael Verde Costas - ismael.verdec@udc.es

Carlos Torres Paz - carlos.torres@udc.es

## Iteración 1

Por ahora tenemos el diseño base de la página web, así como un módulo completo de código para recuperar los datos de las APIs.
Tenemos un solo caso de uso totalmente funcional, el de buscar los datos de un país por su nombre.

## Iteración 2

### Instrucciones de despliegue de docker

En la raíz del repositorio hay un script "run.sh" que se descarga el contenedor Docker y lo inicia en el puerto que le pasemos como único parámetro.

Prerequisitos: Tener instalado el Docker Engine

Ejemplo de uso:

```bash
    # Para lanzar el servidor en el puerto TCP 8080
    ./run.sh 8080
```

### Instrucciones de uso de la práctica

La práctica consiste en una web que maneja datos demográficos. El medio usado para acceder a los casos de uso descritos en la documentación es una barra de navegación. Esta siempre está en la parte superior de la web con todos los CU disponibles. 

La navbar tiene, en primer lugar, el nombre de la web y su logo, que al pulsarse dirigen al usuario a la página principal. Dicha página es un ejemplo del CU de buscar un país. 

En segundo lugar, la navbar tiene un texto de "Data comparation" que dirige al usuario al CU con dicho nombre. Los CUs están todos explicados en detalle en la documentación, por lo que consideramos redundante el explicar lo mismo en ambos lugares.

En tercer lugar, hay un texto de "Top Countries" que dirige al usuario al CU con dicho nombre.

En cuarto lugar, hay un dropdown de "Graphing" que proporciona 4 opciones. La primera es una guía de los CUs disponibles en el dropdown, con un ejemplo y un vinculo directo a cada uno. Las 3 siguientes son los accesos directos a dichos CUs, los cuales corresponden a crear un gráfico de 1 indicador sobre varios países, crear gráfico de varios indicadores sobre 1 país y el hacer el histograma de un indicador a lo largo del mundo.

En quinto lugar, hay una barra de búsqueda con su botón de uso. En esta se puede escribir el nombre de un país o su código ISO para buscar datos acerca del propio país. Este CU corresponde al de search country. Además, al mostrar la info de un país, se muestran sus fronteras, en las cuáles se puede pulsar para buscar info sobre ellas.

Por último, están los botones de "Sign up" y "Login" que sirven para iniciar sesión. Estos se substituyen por "Profile" y "Logout" una vez se inicia sesión. En el apartado de Profile, el usuario tiene su apartado personal donde aparecen las gráficas que ha guardado separadas por categoría. También puede eliminar dichas gráficas si lo desea.
