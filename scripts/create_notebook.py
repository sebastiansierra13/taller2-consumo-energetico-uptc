import json
import os

os.makedirs('notebooks', exist_ok=True)
os.makedirs('src', exist_ok=True)
os.makedirs('data', exist_ok=True)

cells = [
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '# Taller II: Preparación de Datos para Modelos de Predicción del Consumo Energético\n',
            '\n',
            '**Especialización en Inteligencia Artificial**  \n',
            '**Universidad Pedagógica y Tecnológica de Colombia (UPTC)**  \n',
            '**Módulo:** Ciencia de Datos e Inteligencia Artificial  \n',
            '\n',
            '---\n',
            '\n',
            '### 1. Propósito\n',
            'Diseñar y ejecutar un proceso integral de preparación de datos que permita transformar registros de consumo energético en un conjunto de datos limpio, consistente y estructurado, apto para la implementación de modelos de aprendizaje automático orientados a la predicción del consumo energético y al apoyo de estrategias de optimización y sostenibilidad institucional.\n',
            '\n',
            '### 2. Contexto Institucional\n',
            'La Universidad Pedagógica y Tecnológica de Colombia (UPTC) cuenta con 4 sedes en Boyacá:\n',
            '- **Tunja:** 18.000 estudiantes\n',
            '- **Duitama:** 5.500 estudiantes\n',
            '- **Sogamoso:** 6.000 estudiantes\n',
            '- **Chiquinquirá:** 2.000 estudiantes\n',
            '\n',
            'El funcionamiento de estas sedes involucra sectores de: *Comedores, Salones, Laboratorios, Auditorios y Oficinas*.'
        ]
    },
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '## Configuración e Importación de Librerías'
        ]
    },
    {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [
            'import os\n',
            'import numpy as np\n',
            'import pandas as pd\n',
            'import matplotlib.pyplot as plt\n',
            'import seaborn as sns\n',
            '\n',
            '# Estilos visuales\n',
            'sns.set_theme(style="whitegrid", palette="muted")\n',
            'plt.rcParams["figure.figsize"] = (12, 6)\n',
            'pd.set_option("display.max_columns", None)\n',
            'print("Librerías importadas correctamente.")'
        ]
    },
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '---\n',
            '## Fase I. Carga y Exploración Inicial de Datos'
        ]
    },
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '### 1. Cargar los datos desde el archivo CSV (`consumos_uptc.csv`)'
        ]
    },
    {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [
            'csv_path = "consumos_uptc.csv" if os.path.exists("consumos_uptc.csv") else "../consumos_uptc.csv"\n',
            'df = pd.read_csv(csv_path)\n',
            'print(f"Dataset cargado correctamente desde: {csv_path}")\n',
            'df.head()'
        ]
    },
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '### 2. Identificar dimensiones del conjunto de datos'
        ]
    },
    {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [
            'filas, columnas = df.shape\n',
            'print("Dimensiones del dataset:")\n',
            'print(f"- Filas (registros):    {filas:,}")\n',
            'print(f"- Columnas (variables): {columnas}")'
        ]
    },
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '### 3. Analizar variables y tipos de datos'
        ]
    },
    {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [
            'df.info()'
        ]
    },
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '### 4. Explorar valores únicos por sede'
        ]
    },
    {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [
            'conteo_sedes = df["sede"].value_counts()\n',
            'print("Distribución de registros por sede:")\n',
            'display(conteo_sedes)\n',
            '\n',
            'plt.figure(figsize=(8, 4))\n',
            'sns.barplot(x=conteo_sedes.index, y=conteo_sedes.values, hue=conteo_sedes.index, legend=False)\n',
            'plt.title("Cantidad de Registros por Sede - UPTC", fontsize=13, fontweight="bold")\n',
            'plt.ylabel("Número de Registros")\n',
            'plt.xlabel("Sede")\n',
            'plt.show()'
        ]
    },
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '### 5. Obtener estadísticas descriptivas'
        ]
    },
    {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [
            'df.describe().T'
        ]
    },
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '### 6. Detectar posibles inconsistencias\n',
            'Revisamos variables categóricas como `periodo_academico` para detectar inconsistencias de formato, tipeo y mayúsculas/minúsculas.'
        ]
    },
    {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [
            'print("Valores únicos en \'periodo_academico\':")\n',
            'print(df["periodo_academico"].value_counts(dropna=False))\n',
            'print("\nDiagnóstico: Se observan variantes inconsistentes como \'semestre1\', \'Semestre_1\', \'SEMESTRE_1\', \'semestre_1\'.")'
        ]
    },
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '---\n',
            '## Fase II. Limpieza y Preparación Inicial'
        ]
    },
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '### 7. Identificar valores nulos'
        ]
    },
    {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [
            'nulos = df.isnull().sum()\n',
            'pct_nulos = (nulos / len(df)) * 100\n',
            'tabla_nulos = pd.DataFrame({"Valores Nulos": nulos, "Porcentaje (%)": pct_nulos})\n',
            'display(tabla_nulos[tabla_nulos["Valores Nulos"] > 0].sort_values(by="Valores Nulos", ascending=False))'
        ]
    },
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '### 8. Filtrar registros correspondientes a la sede DUITAMA'
        ]
    },
    {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [
            'df_duitama = df[df["sede"].str.strip().str.upper() == "DUITAMA"].copy()\n',
            'df_duitama.reset_index(drop=True, inplace=True)\n',
            'print("Primeros registros filtrados para Duitama:")\n',
            'df_duitama.head()'
        ]
    },
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '### 9. Comparar cantidad de registros antes y después del filtrado'
        ]
    },
    {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [
            'reg_antes = len(df)\n',
            'reg_despues = len(df_duitama)\n',
            'print(f"Registros antes del filtrado (General): {reg_antes:,}")\n',
            'print(f"Registros después del filtrado (Duitama): {reg_despues:,}")\n',
            'print(f"Porcentaje retenido: {(reg_despues / reg_antes) * 100:.2f}%")'
        ]
    },
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '### 10. Detectar valores negativos en variables de consumo y ambientales:\n',
            '- Energía comedor\n',
            '- Energía salones\n',
            '- Energía laboratorios\n',
            '- Energía auditorios\n',
            '- Energía oficinas\n',
            '- Agua (litros)\n',
            '- CO2 (kg)\n',
            '- Energía total (variable objetivo)\n'
        ]
    },
    {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [
            'vars_a_verificar = [\n',
            '    "energia_comedor_kwh",\n',
            '    "energia_salones_kwh",\n',
            '    "energia_laboratorios_kwh",\n',
            '    "energia_auditorios_kwh",\n',
            '    "energia_oficinas_kwh",\n',
            '    "agua_litros",\n',
            '    "co2_kg",\n',
            '    "energia_total_kwh"\n',
            ']\n',
            '\n',
            'conteo_negativos = {}\n',
            'for col in vars_a_verificar:\n',
            '    conteo_negativos[col] = (df_duitama[col] < 0).sum()\n',
            '\n',
            'df_neg = pd.DataFrame(list(conteo_negativos.items()), columns=["Variable", "Valores Negativos"])\n',
            'display(df_neg)'
        ]
    },
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '### 11. Eliminar registros inválidos\n',
            'Se eliminan los registros con valores negativos en las variables físicas ya que representan inconsistencias o fallas en sensores.'
        ]
    },
    {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [
            'mascara_validos = pd.Series(True, index=df_duitama.index)\n',
            'for col in vars_a_verificar:\n',
            '    mascara_validos &= ~(df_duitama[col] < 0)\n',
            '\n',
            'invalidos = (~mascara_validos).sum()\n',
            'df_duitama = df_duitama[mascara_validos].copy().reset_index(drop=True)\n',
            'print(f"Registros inválidos removidos: {invalidos}")\n',
            'print(f"Total registros válidos en Duitama: {len(df_duitama):,}")'
        ]
    },
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '### 12. Verificar registros duplicados'
        ]
    },
    {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [
            'cols_sin_id = [c for c in df_duitama.columns if c != "reading_id"]\n',
            'num_duplicados = df_duitama.duplicated(subset=cols_sin_id).sum()\n',
            'print(f"Cantidad de filas duplicadas (excluyendo reading_id): {num_duplicados}")'
        ]
    },
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '### 13. Eliminar duplicados'
        ]
    },
    {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [
            'if num_duplicados > 0:\n',
            '    df_duitama = df_duitama.drop_duplicates(subset=cols_sin_id).reset_index(drop=True)\n',
            '    print(f"Duplicados eliminados. Registros actuales: {len(df_duitama):,}")\n',
            'else:\n',
            '    print("No existen registros duplicados en el dataset de Duitama.")'
        ]
    },
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '---\n',
            '## Fase III. Análisis Exploratorio de Datos (EDA)'
        ]
    },
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '### 14. Estadísticas descriptivas de las variables energéticas (Sede Duitama)'
        ]
    },
    {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [
            'vars_energeticas = [\n',
            '    "energia_comedor_kwh",\n',
            '    "energia_salones_kwh",\n',
            '    "energia_laboratorios_kwh",\n',
            '    "energia_auditorios_kwh",\n',
            '    "energia_oficinas_kwh"\n',
            ']\n',
            'display(df_duitama[vars_energeticas].describe().T)'
        ]
    },
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '### 15. Visualizar histogramas para cada tipo de variable energética'
        ]
    },
    {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [
            'fig, axes = plt.subplots(3, 2, figsize=(14, 11))\n',
            'axes = axes.flatten()\n',
            '\n',
            'for i, col in enumerate(vars_energeticas):\n',
            '    sns.histplot(df_duitama[col].dropna(), kde=True, ax=axes[i], color="#1f77b4", bins=40)\n',
            '    axes[i].set_title(f"Distribución de {col}", fontsize=11, fontweight="bold")\n',
            '    axes[i].set_xlabel("Consumo (kWh)")\n',
            '    axes[i].set_ylabel("Frecuencia")\n',
            '\n',
            '# Gráfico para energía total de la sede\n',
            'sns.histplot(df_duitama["energia_total_kwh"].dropna(), kde=True, ax=axes[5], color="#ff7f0e", bins=40)\n',
            'axes[5].set_title("Distribución de energia_total_kwh (Consumo Total)", fontsize=11, fontweight="bold")\n',
            'axes[5].set_xlabel("Consumo Total (kWh)")\n',
            'axes[5].set_ylabel("Frecuencia")\n',
            '\n',
            'plt.tight_layout()\n',
            'plt.show()'
        ]
    },
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '### 16. Imputar valores nulos\n',
            'Estrategia:\n',
            '- **Variables numéricas:** Mediana (adecuada ante asimetrías y sesgos).\n',
            '- **Variables categóricas:** Moda.'
        ]
    },
    {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [
            'cols_num = df_duitama.select_dtypes(include=[np.number]).columns\n',
            'cols_cat = df_duitama.select_dtypes(exclude=[np.number]).columns\n',
            '\n',
            '# Imputar numéricas con la mediana\n',
            'for col in cols_num:\n',
            '    if df_duitama[col].isnull().sum() > 0:\n',
            '        med = df_duitama[col].median()\n',
            '        df_duitama[col] = df_duitama[col].fillna(med)\n',
            '        print(f"Columna numérica \'{col}\' imputada con mediana: {med:.4f}")\n',
            '\n',
            '# Imputar categóricas con la moda\n',
            'for col in cols_cat:\n',
            '    if df_duitama[col].isnull().sum() > 0:\n',
            '        mod = df_duitama[col].mode()[0]\n',
            '        df_duitama[col] = df_duitama[col].fillna(mod)\n',
            '        print(f"Columna categórica \'{col}\' imputada con moda: {mod}")\n',
            '\n',
            'print(f"Total de nulos tras imputación: {df_duitama.isnull().sum().sum()}")'
        ]
    },
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '### 17. Construir e interpretar la matriz de correlación'
        ]
    },
    {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [
            'cols_analisis = [\n',
            '    "energia_total_kwh",\n',
            '    "energia_comedor_kwh",\n',
            '    "energia_salones_kwh",\n',
            '    "energia_laboratorios_kwh",\n',
            '    "energia_auditorios_kwh",\n',
            '    "energia_oficinas_kwh",\n',
            '    "potencia_total_kw",\n',
            '    "agua_litros",\n',
            '    "temperatura_exterior_c",\n',
            '    "ocupacion_pct",\n',
            '    "co2_kg"\n',
            ']\n',
            '\n',
            'matriz_correlacion = df_duitama[cols_analisis].corr()\n',
            '\n',
            'plt.figure(figsize=(11, 9))\n',
            'sns.heatmap(matriz_correlacion, annot=True, fmt=".2f", cmap="coolwarm", cbar=True, square=True)\n',
            'plt.title("Matriz de Correlación de Pearson - Sede Duitama", fontsize=13, fontweight="bold")\n',
            'plt.tight_layout()\n',
            'plt.show()'
        ]
    },
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '---\n',
            '## Fase IV. Preparación para Modelado'
        ]
    },
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '### 18. Seleccionar las variables objetivo\n',
            'Para predicción institucional general de consumo eléctrico seleccionamos:\n',
            '- **Variable Objetivo:** `energia_total_kwh`'
        ]
    },
    {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [
            'target_col = "energia_total_kwh"\n',
            'y = df_duitama[target_col]\n',
            'print(f"Variable objetivo definida: {target_col}")\n',
            'print(y.describe())'
        ]
    },
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '### 19. Definir variables predictoras (features)'
        ]
    },
    {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [
            'features = [\n',
            '    "energia_comedor_kwh",\n',
            '    "energia_salones_kwh",\n',
            '    "energia_laboratorios_kwh",\n',
            '    "energia_auditorios_kwh",\n',
            '    "energia_oficinas_kwh",\n',
            '    "potencia_total_kw",\n',
            '    "agua_litros",\n',
            '    "temperatura_exterior_c",\n',
            '    "ocupacion_pct",\n',
            '    "hora",\n',
            '    "dia_semana",\n',
            '    "mes",\n',
            '    "trimestre",\n',
            '    "es_fin_semana",\n',
            '    "es_festivo",\n',
            '    "es_semana_parciales",\n',
            '    "es_semana_finales"\n',
            ']\n',
            'X = df_duitama[features]\n',
            'print(f"Total de características predictoras: {len(features)}")\n',
            'X.head()'
        ]
    },
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '### 20. Excluir variables no relevantes\n',
            'Se excluyen identificadores únicos, variables constantes post-filtrado y metadatos no informativos.'
        ]
    },
    {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [
            'excluidas = ["reading_id", "timestamp", "sede", "sede_id", "dia_nombre", "año", "periodo_academico", "co2_kg"]\n',
            'print("Variables excluidas del modelado predictivo directo:")\n',
            'for col in excluidas:\n',
            '    print(f"- {col}")'
        ]
    },
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '### 21. Construir el conjunto final para entrenamiento y exportar'
        ]
    },
    {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [
            'os.makedirs("data", exist_ok=True)\n',
            'dataset_final = pd.concat([X, y], axis=1)\n',
            'output_file = "data/consumos_duitama_preparado.csv"\n',
            'dataset_final.to_csv(output_file, index=False)\n',
            '\n',
            'print("=== Conjunto final de entrenamiento construido con éxito ===")\n',
            'print(f"- Dimensiones: {dataset_final.shape[0]:,} filas x {dataset_final.shape[1]} columnas")\n',
            'print(f"- Guardado en: {output_file}")\n',
            'dataset_final.head()'
        ]
    }
]

nb = {
    'cells': cells,
    'metadata': {
        'kernelspec': {
            'display_name': 'Python 3',
            'language': 'python',
            'name': 'python3'
        },
        'language_info': {
            'codemirror_mode': {'name': 'ipython', 'version': 3},
            'file_extension': '.py',
            'mimetype': 'text/x-python',
            'name': 'python',
            'nbconvert_exporter': 'python',
            'pygments_lexer': 'ipython3',
            'version': '3.13.2'
        }
    },
    'nbformat': 4,
    'nbformat_minor': 4
}

with open('notebooks/taller_preparacion_datos.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print('Notebook creado con éxito en notebooks/taller_preparacion_datos.ipynb')
