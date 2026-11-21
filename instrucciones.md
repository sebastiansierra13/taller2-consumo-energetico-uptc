# Taller II: Preparación de Datos para la Implementación de Modelos de Predicción y Optimización del Consumo Energético

**Especialización en Inteligencia Artificial**  
**Universidad Pedagógica y Tecnológica de Colombia (UPTC)**

---

## 1. Propósito
Diseñar y ejecutar un proceso integral de preparación de datos que permita transformar registros de consumo energético en un conjunto de datos limpio, consistente y estructurado, apto para la implementación de modelos de aprendizaje automático orientados a la predicción del consumo energético y al apoyo de estrategias de optimización y sostenibilidad institucional.

---

## 2. Contexto del Problema
La Universidad Pedagógica y Tecnológica de Colombia (UPTC) desarrolla sus actividades académicas y administrativas en cuatro sedes ubicadas en el departamento de Boyacá, con poblaciones estudiantiles y dinámicas operativas diferenciadas:
* **Tunja:** 18.000 estudiantes
* **Duitama:** 5.500 estudiantes
* **Sogamoso:** 6.000 estudiantes
* **Chiquinquirá:** 2.000 estudiantes

El funcionamiento de estas sedes implica consumos energéticos asociados a distintos sectores institucionales:
* Comedores
* Salones
* Laboratorios
* Auditorios
* Oficinas

La heterogeneidad entre sedes y sectores genera variaciones en los patrones de consumo energético, influenciadas por factores como ocupación, horarios académicos, actividades desarrolladas y utilización de infraestructura.

---

## 3. Objetivos Específicos
1. Realizar la exploración inicial del conjunto de datos para identificar su estructura, dimensiones, tipos de variables y posibles problemas de calidad.
2. Aplicar técnicas de limpieza y depuración de datos mediante el tratamiento de valores faltantes, detección de registros inconsistentes, eliminación de duplicados y corrección de anomalías en variables de consumo.
3. Analizar estadísticamente las variables energéticas para identificar patrones de comportamiento, distribuciones y relaciones entre sectores de consumo.
4. Implementar procesos de transformación y preparación de variables que permitan generar un conjunto de datos adecuado para técnicas de modelado predictivo.
5. Seleccionar las variables objetivo y definir el conjunto de características (*features*) relevantes para la construcción de modelos de predicción del consumo energético.
6. Construir un conjunto de datos final que garantice calidad, integridad y consistencia para etapas posteriores de entrenamiento, validación e interpretación de modelos de Inteligencia Artificial.

---

## 4. Metodología y Fases

### Fase I. Carga y Exploración Inicial de Datos
1. Cargar los datos desde el archivo CSV (`consumos_uptc.csv`).
2. Identificar dimensiones del conjunto de datos (filas y columnas).
3. Analizar variables y tipos de datos (numéricas, categóricas, temporales).
4. Explorar valores únicos por sede.
5. Obtener estadísticas descriptivas generales.
6. Detectar posibles inconsistencias (ej. formatos de texto heterogéneos, categorías duplicadas con diferente ortografía).

### Fase II. Limpieza y Preparación Inicial
7. Identificar valores nulos por columna.
8. Filtrar registros correspondientes a la sede **DUITAMA**.
9. Comparar cantidad de registros antes y después del filtrado.
10. Detectar valores negativos en:
    * Energía comedor
    * Energía salones
    * Energía laboratorios
    * Energía auditorios
    * Energía oficinas
    * Agua (litros)
    * CO2 (kg)
11. Eliminar registros inválidos (valores negativos en variables de consumo o emisiones).
12. Verificar registros duplicados.
13. Eliminar duplicados en caso de existir.

### Fase III. Análisis Exploratorio de Datos (EDA)
14. Obtener estadísticas descriptivas de las variables energéticas en la sede Duitama:
    * Energía comedor
    * Energía salones
    * Energía laboratorios
    * Energía auditorios
    * Energía oficinas
15. Visualizar histogramas y diagramas de distribución para cada tipo de variable energética.
16. Imputar valores nulos:
    * **Mediana** para variables numéricas continuas.
    * **Moda** para variables categóricas.
17. Construir e interpretar la matriz de correlación entre las variables energéticas y los factores exógenos (temperatura, ocupación, potencia, etc.).

### Fase IV. Preparación para Modelado
18. Seleccionar las variables objetivo (ej. `energia_total_kwh` o consumo específico por sector).
19. Definir variables predictoras (*features*) numéricas y categóricas.
20. Excluir variables no relevantes o redundantes (identificadores, redundancias de sede, fechas sin transformar).
21. Construir el conjunto final para entrenamiento y exportar el dataset preparado.

---

## 5. Resultado Esperado
Conjunto de datos limpio, consistente y preparado para entrenar modelos de Machine Learning (regresión, series temporales, clustering) capaces de predecir el consumo energético y apoyar la toma de decisiones institucionales.

## 6. Archivo de Entrega
Guardar el cuaderno de trabajo o informe en formato PDF y subirlo a la plataforma Moodle.
