# TIENDA DE ROPA ONLINE

## Índice
1. [Introducción](#introducción)
2. [Requerimientos](#requerimientos)
3. [Solución Arquitectónica](#solución-arquitectónica)
4. [Validaciones](#validaciones)
5. [Pruebas](#pruebas)
6. [Estructura del Repositorio](#estructura-del-repositorio)

---

## Introducción
La tienda de ropa online permite a los usuarios:
- Comprar productos.
- Aplicar descuentos.

El objetivo es desarrollar una solución que cumpla con los requerimientos funcionales y no funcionales, asegurando calidad y robustez en el diseño e implementación.

---

## Requerimientos

### Funcionales
1. **Cálculo del subtotal**: Multiplicar la cantidad de productos por el precio unitario.
2. **Aplicación de descuentos**: Descuentos sobre el subtotal.
3. **Validación de edad**: Solo pueden comprar usuarios mayores de 18 años y menores de 120 años.
4. **Validación de códigos promocionales**: Los códigos válidos son:
   - `PROMO10`
   - `DESCUENTO20`

### No Funcionales
- Elaborar una solución arquitectónica que incluya:
  - Modelo de clases.
  - Distribución lógica de responsabilidades.
  - Plan de despliegue.

---

## Solución Arquitectónica

### Elementos a Identificar
1. **Diagrama de arquitectura**:
   - Al menos en 3 capas.
2. **Cajas negras y blancas**:
   - Identificar los componentes internos y externos.
3. **Valores límites**:
   - Considerar casos extremos en las entradas.
4. **Pruebas unitarias**:
   - Dos pruebas por cada hito.

### Consideraciones
- Persistencia: Libre elección del método.
- Integración: Definir cómo se combinan las funciones.

---

## Validaciones

### Entradas que podrían generar errores
- Edad fuera del rango permitido.
- Cantidad de productos negativa o cero.
- Códigos promocionales inválidos.

### Condiciones extremas
- Edad: 18 y 120 años.
- Cantidad: Valores muy altos o cero.
- Códigos: Formatos incorrectos o no válidos.

---

## Pruebas

### Tipos de Pruebas
1. **Pruebas unitarias**:
   - Implementar en Python.
   - Dos pruebas por cada hito.
2. **Pruebas de integración**:
   - Verificar la combinación de funciones.

### Ejecución
- Pseudocódigo hasta la implementación final.

---

## Estructura del Repositorio

- **documento**: Diagramas UML y otros documentos.
- **src**: Todo el código Python.
- **anexos**: Fuentes de datos y referencias.

