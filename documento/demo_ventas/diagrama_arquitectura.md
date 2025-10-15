![Imagen demostrativa de comunicación entre capas](./diagrama_arquitectura.png)


| Capa | Elementos|Responsabilidad|Código fuente|
|--|--|--|--|
|Server|Lógica del negocio (módulos como: descuentos, validaciones, etc.)|Encargado de recibir las peticiones de la user interface e indicárselas al repositorio|TODO|
|Repository|Data access layer|Encargado de recibir mensajes desde el server y llamar a la Base de datos|creación, validaciones|
|Base de datos|Base de datos sqlite|Encargar de persistir datos del negocio|TODO|
|User interface|Vista al usuario|Encargado de presentar al usuario una fácil comunicación con la lógica de negocio|TODO|
|Repository|Data access layer|Encargado de recibir mensajes desde el server y llamar a la Base de datos|TODO|
|Common|Clases de dominio (Pedido,Carrito, Descuento, etc.)|Encargado de permitir la comunicación entre UI, Server y Repository|TODO|
|Customer|Cliente (compras, carrito, descuentos, pagos)|Cliente que tiene su vista para interactuar con el negocio.|TODO|
|Administrador|Administrador (ventas, stock, descuentos, cobros)|Administrador que tiene su vista para interactuar con el negocio.|TODO|





![](https://img.plantuml.biz/plantuml/svg/bLJRRjim37qtu7yGykIkSx6z2a7HBDs00XiGeEi7C9BgQfDDWv8xO9T_dsnTOgS9YZv58KMUStX4trW7v8RMb4LP20FMiWSx06baVyg2iPffoTbTvrIZA0GwRFUaEBjtfBicn5GBsYn3lU_r2qakenBtdDs2K-FVI_OCHakWpn9aTS7P9qIZe2kBVmSwMwELXmzqBXaqf1gWZTa2aNPOzOHo40uvsyNJUoQWSxxlWVb5A2RbyNu3xPJK4aV4S5e0RcIhEsqTWKGwWaqG9r0ZH8jIFse1TEzG_AoqtEMRaSjfUZC2gU9D3lIaXCQ7JhlHFCw-60GNKdPaicZXzGWtX5a4dgzGkbLM3Dw6p4bucGqUKK0I_WxyK3FuxF5sgl3QMgoMrUUC3mQVdKAom7BsrTkrJcExZWoZ8kNptw1V7rv7x1BlsM7lq85PZ4mclPlUU3Ebvvf745G9C68mVdonV7nCCz4mrL4kgdB7MQT3oTpzwKMULJs4xUHfJPFOQLOy3Ir4N-fwLE89vWkOP7m_qZ0HIb-2zT-wJdju55qiIrcaPLrzNB6wlfv-CwMex6GkcPsJxrPv3qvaFrnT-UFCaXV0OttSxRAuKPsSld7_0G00)