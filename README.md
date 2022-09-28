# VolDivAI

## VolDIvAI es un programa que utiliza la inteligencia artificial para encontrar los valores de dos resistencias en un divisor de voltaje si solo conoces el voltaje de tu fuente y el voltaje que deseas obtener.
<br>

### Descripción
VolDivAI es un programa hecho en Python, este utiliza un algoritmo genético y por medio de lo que se conoce como *"machine learning"* logra encontrar los valores de dos resistencias que compongan un divisor de voltaje, con tan solo conocer el valor del voltaje de entrada que quieras utilizar y el valor del voltaje que deseas obtener a la salida.

Como dato curioso, el algoritmo genético que utiliza no proviene de ninguna librería, sino que está programado a mano, siguiendo los principios que fundamentan a un algoritmo genético en sí. Que es una forma de aprendizaje automático, que trata de emular un proceso natural como lo es la genética. 

Es perfecto para proyectos de electrónica analógica, en donde en ocaciones se necesitan utilizar valores muy específicos de voltajes para realizar comparaciones o montar señales.

Los valores que VolDivAI obtiene no siempre son 100% exactos, sin embargo, solo arroja valores mayores al 98% de exactitud, haciendo que dichos valores sean bastante confiables.

### Instrucciones de instalación
1. Ir la sección de releases en la página principal de este repositorio.

2. Bajo la pestaña de *assets* dar click en el archivo que se muestra, este comenzará la descarga del instalador para Windows.

3. Ejecutar el instalador.

4. Seleccionar el path donde se desea instalar el programa.


### Instrucciones de uso
1. Insertar un voltaje de entrada en el primer campo.

2. Insertar un voltaje de salida en el segundo campo.
    * Nota: El voltaje de salida **debe** de ser menor que el voltaje de entrada.

3. Presionar en el botón de calcular.

4. Después de realizar los cálculos se puede hacer un cálculo diferente, limpiar los campos o salir de la aplicación.