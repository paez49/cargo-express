# Serverless REST API con Flask, DynamoDB y DynamoDB Streams

Servicio REST para recibir peticiones de pedidos para la empresa Cargo Express usando [serverless framework](https://github.com/serverless/serverless), siendo esta una herramienta para la construcción y despliegue de aplicaciones serverless usando el marco de trabajo de IaC. En este documento se van a ver todos los aspectos tecnicos, incluyendo diseño
de arquitectura, modelamiento de datos, además de incluir un tutorial para el correcto despliegue del servicio.

## Contenido

- [Modelo de arquitectura](#modelo-de-arquitectura)
- [Modelo de datos](#modelo-de-datos)
- [Preguntas teoricas](#preguntas-teoricas)
- [Tutorial de despliegue](#tutorial-de-despliegue)
  - [Como probar el servicio](#como-probar-el-servicio)

## Modelo de arquitectura

<img src="image/PruebaMAZIO.svg" alt="Descripción del SVG" width="600px">

Como se aprecia en la imagen, el punto de acceso es por medio del API Gateway, este redirigue las peticiones a su respectivo endpoint, mapeado logicamente por las rutas. Cada endpoint
está desplegado en una función Lambda, la función `Orders backend` es encargada de registrar en una base de datos DynamoDB los pedidos de la empresa, mientras que `Monitor service` es el encargado de ofrecer información relacionada con el monitoreo de los pedidos de la empresa. Cada vez que se registra un pedido, con el fin de poder tener datos de monitoreo en **casi tiempo real**, se tiene DynamoDB Stream, este cumple la función que cada vez que se registra un nuevo pedido, se activa un trigger que envía la información recién ingresada a la función Lambda `Streams function` esta almacenará los datos en otras tablas de DynamoDB, las cuales estarán disponibles para el endpoint relacionado con el monitoreo. Con el objetivo de añadir una capa de seguridad, se implementó Amazon Cognito el cual proporciona un servicio de autenticación a los usuarios de la aplicación. Esto se logra mediante la creación y validación de tokens JWT generados por este servicio. Todos los endpoints están protegidos mediante un autorizador JWT en el api gateway.

### Especifcación de endpoints

- `/orders/`
  - POST - Encargado de la creación de pedidos en la base de datos. Requiere un payload detallado en `script.py`
    para registrar el pedido hecho incluyendo información de productos, del repartidor además un estampa de tiempo.
- `/monitor/`
  - GET - Encargado de obtención de información de monitoreo de los pedidos. Este ofrece las siguientes metricas:
    - Productos mas vendidos.
    - Repartidores con el total de productos vendidos.
    - Repartidores con el total de dinero generado.

## Modelo de datos

<img src="image/ModeloDatos.png" alt="Descripción del SVG" width="600px">

> Como se evidencia hay atributos que se repiten entre tablas, esto se hizo con el fin de que las consultas a la base de datos fueran mas sencillas, sin embargo, si se busca economizar almacenamiento, tocaría realizar un proceso de normalización.

### Orders

En la tabla de ordenes tiene toda la información relacionada con el pedido realizado, se almacena el id de la orden, el total del dinero de esa orden, y la fecha en la que se realizó. En el campo de delivery se guarda un map con información de quien hizo el envío con su nombre e identificación. Por último, se tiene una lista de maps, los cuales especifican detalles del producto, con su id, nombre y precio unitario.

### Deliveries

Esta tabla tiene información relacionada con el repartidor, incluye también nombre y id de este. Además de incluir información relacionada con su rendimiento, como cuantos productos ha enviado hasta el momento y cuanto dinero a generado.

### Products

Esta última tabla contiene información de los productos como y id, pero además incluye información relacionada con la cantidad de veces que se ha vendido un producto.

## Preguntas teoricas

La empresa tiene una proyección de expansión en sus operaciones de un 500% en el próximo año y duplicala en el segundo año.

### ¿Qué recomendaciones le darías para que pueda garantizar su operación?

**R./** Teniendo en cuenta que se aumentaría la operación, con la arquitectura actual, es recomendable validar lo mencionado anteriormente respecto a una normalización de los datos si se quiere buscar usar menos almacenamiento a costo de mas procesamiento en las querys. También si se llega a usar en un entorno de producción con ese nivel alto de operación, es recomendable validar la opción de usar instancias EC2 con planes de ahorro o instancias reservadas, esto con el fin de ahorrar en terminos de costos de la arquitectura. Por último, si la empresa busca aumentar su operación en terminos geograficos, habría que validar un despliegue mas global, por ejemplo empezar con el API Gateway el cual al ser versión 2 (HTTP) es a nivel regional, mientras que la versión 1 (REST) es mas global ~~pero mas costoso~~.

### ¿La solución planteada se encuentra en la capacidad de responder la demanda durante los próximos dos años?

**R./** Actualmente, la infraestructura está en capacidad de suplir la demanda durante los próximos dos años, gracias a la arquitectura serverless, que permite escalar los servicios de manera automática bajo demanda. Sin embargo, es importante monitorear constantemente los costos asociados a esta escalabilidad, ya que puede volverse menos viable a largo plazo si el volumen de uso aumenta significativamente. En ese caso, podría ser recomendable evaluar la transición a instancias EC2, como mencioné anteriormente, para optimizar el costo-beneficio y obtener un mayor control sobre los recursos utilizados.

## Tutorial de despliegue

Para poder desplegar la arquitectura en AWS es [necesario tener instalado npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm). Luego de tenerlo instalado, se debe ejecutar este comando para instalar el paquete de serverless framework

```bash
npm i serverless -g
```

Para verificar que se encuentra instalado puedes ejecutar el siguiente comando

```bash
sls --version
```

Si todo esta bien te debería salir algo como esto

```bash
Serverless ϟ Framework

 • 4.3.2
```

Una vez confirmado que tengas instalado serverless ve a la carpeta de `/api/` y ejecuta el siguiente comando para descargar todas las dependencias necesarias para poder desplegar la aplicación.

```bash
cd api
npm install
```

Una vez se descargaron todas las dependencias, ejecuta el siguiente comando para desplegar la arquitectura

```bash
sls deploy
```

> [!WARNING]
> Recuerda tener instalado pip y python 3.12 si te llegar a salir un error como este "`python3.12 -m pip help install Exited with code 1`"

> [!NOTE]
> Lastimosamente en la versión 4 de serverless framework está pidiendo loguearse en la pagina de ellos una vez que se quiere desplegar la arquitectura, por lo tanto es necesario crearse una cuenta en esta plataforma para poder ver en ejecución la arquitectura, o [ejecutarlo en la versión 3](https://www.serverless.com/framework/docs/getting-started#pinning-to-a-specific-version).

> Para poder desplegar la arquitectura es necesario [tener funcional el CLI de AWS](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html), así como de
> [tener configuradas las credenciales de tu cuenta en AWS](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-quickstart.html), recomiendo usar la opción de "Short-term credentials"

Esto lo que hará es, usando tus credenciales, desplegar la arquitectura de manera automatizada, pudiendo ser monitoreada en CloudWatch. Además se puede saber exactamente los recursos que se desplegaron en el `serverless.yml` o también en CloudFormation. Una vez desplegado te saldrá algo como esto en la consola.

```bash
Packaging Python WSGI handler...

✔ Service deployed to stack api-dev (81s)

endpoints:
  ANY - https://dwp4x4hla4.execute-api.us-east-1.amazonaws.com/order
  ANY - https://dwp4x4hla4.execute-api.us-east-1.amazonaws.com/order/{proxy+}
  ANY - https://dwp4x4hla4.execute-api.us-east-1.amazonaws.com/monitor
  ANY - https://dwp4x4hla4.execute-api.us-east-1.amazonaws.com/monitor/{proxy+}
functions:
  orders-api: api-dev-orders-api (1.8 MB)
  monitor-api: api-dev-monitor-api (1.8 MB)
  stream_function: api-dev-stream_function (1.8 MB)
```

Esto quiere decir que la arquitectura se desplegó correctamente.

### Como probar el servicio

Usando el archivo `script.py` se puede usar para realizar las respectivas pruebas al servicio. Sin embargo, se deben seguir estos pasos para que funcione al ejecutarlo.

1. Ingresas a la consola de AWS y busca el servicio Cognito.
2. Dale en la opción de crear usuario

![alt text](image/CreateUser.png)

3. Ingresa nombre de usuario y una contraseña de 6 caracteres

<img src="image/CreateUserInfo.png" alt="Descripción del SVG" width="600px">

4. Una vez creado, ve a la pestaña de AppIntegration

![alt text](image/AppIntegrationTab.png)

5. Baja hasta App client list y oprime en el nombre del app client

![alt text](image/AppClient.png)

6. Baja hasta la opción de Hosted UI y oprime en View Hosted UI

![alt text](image/HostedUI.png)

7. Una vez acá, escribe tu usuario y contraseña que escribiste en el paso 3, te pedirá que ingreses una nueva contraseña y un correo, el correo no es necesario que sea real.
8. Una vez cambies tu contraseña, probablemente te salga un error en el navegador, sin embargo se confirma que el usuario cambió su contraseña correctamente.

9. Ve a la carpeta raiz del proyecto y crea un archivo `.env` con la siguiente estructura

![alt text](image/DOTENV.png)

10. En la variable `API` pon la URL sin rutas que te salió una vez desplegada la arquitectura con `sls deploy`.

11. En la variable `CLIENT_ID` pon el id del app client **entre comillas**, este se encuentra en la interfaz vista en el paso 5.

![alt text](image/AppClientID.png)

12. Una vez copiados y pegados se debería ver asi

![alt text](image/ApiClientIdEnv.png)

13. Por último, en el `.env`, escribe las credenciales del usuario (Nombre de usuario y la nueva contraseña que creaste). En este caso mi usuario es test y la contraseña es maziooo

![alt text](image/Credentials.png)

14. Ahora puedes ejecutar el `script.py` para ver el servicio en funcionamiento. En la consola se imprimirá el access token, además mostrará como se crean 3 productos y presentará información relacionada con el monitoreo del servicio. Usando Postman y el token anteriormente impreso, puedes usar el endpoint `/monitor/`.

![alt text](image/Postman.png)

15. En la consola de AWS, en el servicio de DynamoDB, en la opción de tablas, puedes ver los registros de ordenes, productos y deliveries.

![alt text](image/ExecutionResult.png)
