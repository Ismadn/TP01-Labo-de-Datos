# Trabajo Práctico: Relación entre las variables demográficas y el acceso a la salud.

Dadas unas fuentes de datos abiertas vinculadas a la República Argentina, buscamos 
averiguar si existe alguna relación entre las características de los nacimientos, las variables 
demográficas y el acceso a la salud, tanto para un determinado año como para su evolución 
en el tiempo. Las bases de datos brindadas fueron: Censo 2010, Censo 2022, Nacidos 
vivos registrados en Argentina (2010 y 2022) y los Establecimientos de salud asentados en 
el registro federal (REFES) en abril de 2022, basado en provincia y departamento.

## Objetivos
Tomamos como objetivo general de este trabajo poder relacionar las posiciones geográficas 
de las personas con sus calidades de vida.

## Tecnologías utilizadas
- Python
- Pandas
- Matplotlib
- DuckDB / SQL

## Cómo ejecutar el proyecto

### 1. Instalar dependencias

Clonar el repositorio e instalar las librerías necesarias:

```bash
pip install pandas matplotlib duckdb openpyxl
```

### 2. Preparar las bases de datos

Ejecutar los archivos Python en el siguiente orden:

**1. `limpiezabasesdedatos.py`**

Realiza la limpieza y el procesamiento de las bases de datos originales.

**2. `EsquemasMR.py`**

Crea las tablas y estructuras de datos que se utilizarán posteriormente en el análisis, a partir de las bases de datos limpias.

**3. `analisisdedatos.py`**

Ejecuta el análisis de datos utilizando las tablas generadas en las etapas anteriores.

### 3. Consideraciones

- Las bases de datos originales deben estar disponibles en las rutas esperadas por los scripts.
- Se deben ejecutar los archivos en el orden indicado, ya que cada etapa depende de los resultados de la anterior.

## Resultados
Llegamos a la conclusión de que ciertas provincias tienden a características particulares en 
sus nacimientos y una caída total en la tasa de fecundidad del país, pero no vemos una 
relación general entre las distintas zonas del país con tendencias marcadas. En general con 
el paso del tiempo aumentaron los nacimientos prematuros y con bajo peso, incrementó la 
cantidad de habitantes por provincia y las personas con acceso a una cobertura médica. 

## Autor
Estudiantes de Licenciatura en Ciencias de Datos – Universidad de Buenos Aires (UBA).
