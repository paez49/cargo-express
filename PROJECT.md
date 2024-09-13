# Prueba técnica - Cloud Developer

En este momento te encuentras en la segunda etapa del proceso 😊, donde debes adelantar la siguiente prueba técnica cuyo resultado determinara tu continuidad en el proceso. Muchos éxitos ! 

---

🚚 "Cargo Express" es una empresa de mensajería que opera en todo Colombia distribuyendo diversos tipos de productos. Actualmente se encuentra en el proceso de adquirir un nuevo software que les permita registrar las entregas de los pedidos en tiempo real.

Las personas invulucradas en la toma de decisiones no son usuarios expertos en tecnología, por ello es de vital importancia realizar una detallada documentación de todo el proceso.

Los requisitos de la aplicación son:
 
- Se deben poder registrar las entregas de los productos en tiempo cercano al real. La tolerancia máxima para poder registrar la entrega los productos en nuestros sistemas es de máximo 10 segundos.
- El catálogo de productos es de 10 y son de pequeñas dimensiones.
- La flota de repartidores es de 10 personas.
- Los pedidos entregados pueden ser de productos individuales o una agrupación de productos en diversas cantidades.

Adicionalmente, se necesita una aplicación para monitoreo de los pedidos entregados, que permita visualizar en tiempo cercano al real algunas métricas relacionadas con los repartidores y los productos (use al menos 3 métricas).

Ejm:

- Cantidad de entregas por hora por repartidor
- Productos más vendidos

La aplicación de monitoreo debe contar con algun método de autenticación y se debe entregar las credenciales de un usuario para poder acceder.

## Datos de referencia

### Productos

| IdProducto | Producto              | Precio  |
|--------|---------------------------|---------|
| pk0001 | Moneda                    | $1.00   |
| pk0002 | Estuche para gafas        | $8.00   |
| pk0003 | Pequeño espejo de bolsillo| $5.00   |
| pk0004 | Pendrive                  | $12.00  |
| pk0005 | Tarjeta SIM               | $3.00   |
| pk0006 | Adaptador de corriente    | $10.00  |
| pk0007 | Tijeras pequeñas          | $4.00   |
| pk0008 | Pila de botón             | $2.50   |
| pk0009 | Goma de borrar            | $0.50   |
| pk0010 | Clip sujetapapeles        | $0.20   |

### Repartidores

| IdRepartidor | Nombre  |
|-----|------------------|
| 101 | María López      |
| 102 | Carlos García    |
| 103 | Ana Fernández    |
| 104 | Juan Martínez    |
| 105 | Laura Sánchez    |
| 106 | Pedro Gómez      |
| 107 | Elena Rodríguez  |
| 108 | Jorge Pérez      |
| 109 | Sofía Morales    |
| 110 | Daniel Castillo  |


## Hitos de la prueba técnica

1. Desarrollo del backend encargado de recibir los datos de los pedidos entregados (no se requiere desarrollar ningun frontend).
2. Desarrollo de aplicación de monitoreo.
3. Resolver preguntas teóricas.

## Recomendaciones

- Entregar la documentación de cada uno de los pasos que realizó para la solución. Esto es muy importante para poder replicar en otro ambiente.
- En la medida de lo posible utilizar IaC (Infraestructura como codigo) para facilitar el proceso de replicación.
- Se recomienda utilizar un repositorio git público para compartir todos los insumos utilizados para la construcción de la solución.
- No es obligatorio usar la nube de AWS pero tendrá un plus.
- Se debe anexar a la documentación el modelo de datos utilizado y el diagrama de arquitectura.

---


## Desarrollo de la prueba

### Backend encargado de recibir los datos de los pedidos entregados

En este punto no se requiere desarrollar ningun frontend, adjunto encontrará un script de python que puede utilizar para la generación de datos para su aplicación (corre cada 5 segundos). El objetivo es enfocar la prueba técnica en el desarrollo del backend encargado de recibir los datos de los pedidos entregados y en la aplicación de monitoreo.

Se recomienda el uso de python 3.12 y el uso de ambientes virtuales.

```shell
pip install -r requirements.txt
python script.py
```

El script entregado no cuenta con seguridad para realizar los llamados a la api, se considerará un plus que incluya una capa de seguridad y así evitar que el enpoint sea utilizado por un tercero.

### Aplicación de monitoreo

Se debe realizar el desarrollo de una APP Web para realizar el monitoreo de los pedidos entregados, que permita visualizar en tiempo cercano al real por lo menos 3 métricas asociadas con los productos y los repartidores.

Ejm:

- Cantidad de entregas por hora por repartidor
- Productos más vendidos

La aplicación de monitoreo debe contar con algun método de autenticación y se debe entregar las credenciales de un usuario para poder acceder.

Para el desarrollo de la APP puede utilizar la tecnología de su preferencia, se considerará un plus si utiliza arquitecturas serverless y la nube de AWS.

### Preguntas teóricas

La empresa tiene una proyección de expansión en sus operaciones de un 500% en el próximo año y duplicala en el segundo año. ¿Qué recomendaciones le darías para que pueda garantizar su operación? ¿La solución planteada se encuentra en la capacidad de responder la demanda durante los próximos dos años?