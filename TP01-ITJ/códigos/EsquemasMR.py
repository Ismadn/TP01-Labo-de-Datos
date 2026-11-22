#Integrantes: Di Niro Ismael, Domínguez Tomás, Ottaviano Jaime.

#En este archivo, a partir de bases de datos limpias, generamos los esquemas que necesitaremos para el análisis de los datos

#Para correr el código deberás completar la variable "carpeta" con la dirección en donde tengas las bases de datos limpias.
#En caso de querer descargar los esquemas, quitar el "#" en las filas con código del tipo .to_csv()
#Se recomienda recorrer las celdas en orden.

import pandas as pd
import duckdb as dd
carpeta = "Ruta de la carpeta donde estén tus archivos"

centroslimpio = pd.read_csv(carpeta + r"\centroslimpio.csv", sep = ";")
nacweb10limpio = pd.read_csv(carpeta + r"\\nacweb10limpio.csv", sep = ";")
nacweb22limpio = pd.read_csv(carpeta + r"\\nacweb22limpio.csv", sep = ";")
censo2010limpio = pd.read_csv(carpeta + r"\\censo2010limpio.csv", sep = ";")
censo2022limpio = pd.read_csv(carpeta + r"\\censo2022limpio.csv", sep = ";")
#%%%
#Creamos centros_medicos desde el df de centros de salud
consulta = """ 
            SELECT establecimiento_id AS id,
                   departamento_id,
                   provincia_id,
                   origen_financiamiento,
                   tipologia_id,
            FROM centroslimpio
""" 

centros_medicos = dd.sql(consulta).df()
#centros_medicos.to_csv(carpeta+"\centros_medicos.csv", sep=";", index = False)
#%%%
# Nos armamos la tabla provincias que sale del df de centros de salud
consulta = """ 
            SELECT DISTINCT provincia_id AS id,
                            provincia_nombre AS nombre
            FROM centroslimpio
"""

provincias = dd.sql(consulta).df()
#provincias.to_csv(carpeta+"\provincias.csv", sep=";", index = False)
#%%%
# Nos armamos la tabla departamentos que sale del df de centros de salud

consulta = """ 
        SELECT DISTINCT  departamento_id AS id, 
                        departamento_nombre AS nombre,
                        provincia_id
        FROM centroslimpio
"""

departamentos = dd.sql(consulta).df() 
#departamentos.to_csv(carpeta+"\departamentos.csv", sep=";", index = False)
#%%%
# Acá nos armamos las tablas de las madres por año desde el df de nacweb

consulta = """ 
            SELECT PROVRES AS provincia_id,
                   IMINSTRUC AS nivel_educacion,
                   IMEDAD AS rango_edad
            FROM nacweb10limpio

"""
madres2010 = dd.sql(consulta).df() 
madres2010["id"] = madres2010.index+1 #Creo la clave id de madres a partir del valor del index de la base de datos limpia
madres2010 = madres2010[["id","provincia_id","nivel_educacion","rango_edad"]] #Ordeno las columnas
#madres2010.to_csv(carpeta+"\madres2010.csv", sep=";", index = False)

consulta = """ 
            SELECT PROVRES AS provincia_id,
                   IMINSTRUC AS nivel_educacion,
                   IMEDAD AS rango_edad
            FROM nacweb22limpio

"""
madres2022 = dd.sql(consulta).df() 
madres2022["id"] = madres2022.index+1
madres2022 = madres2022[["id","provincia_id","nivel_educacion","rango_edad"]]
#madres2022.to_csv(carpeta+"\madres2022.csv", sep=";", index = False)
#%%%
#Acá nos cremos las tablas de los nacidos vivos por año desde el df de nacweb

consulta = """ 
            SELECT TIPPARTO AS tipo_parto, 
                   SEXO AS sexo,
                   ITIEMGES AS tiempo_gestacion,
                   IPESONAC AS peso_al_nacer,
                   CUENTA AS cantidad
            FROM nacweb10limpio
"""

nacidos2010 = dd.sql(consulta).df() 
nacidos2010["id_madre"] = madres2010["id"] #Creo la clave id_madre cuyo valor es el mismo que tiene la clave de madres
nacidos2010 = nacidos2010[["id_madre","tipo_parto","sexo","tiempo_gestacion","peso_al_nacer","cantidad"]] #Ordeno las columnas
#nacidos2010.to_csv(carpeta+r"\nacidos2010.csv", sep=";", index = False)

consulta = """ 
            SELECT TIPPARTO AS tipo_parto, 
                   SEXO AS sexo,
                   ITIEMGES AS tiempo_gestacion,
                   IPESONAC AS peso_al_nacer,
                   CUENTA AS cantidad
            FROM nacweb22limpio
"""

nacidos2022 = dd.sql(consulta).df() 
nacidos2022["id_madre"] = madres2022["id"]
nacidos2022 = nacidos2022[["id_madre","tipo_parto","sexo","tiempo_gestacion","peso_al_nacer","cantidad"]]
#nacidos2022.to_csv(carpeta+r"\nacidos2022.csv", sep=";", index = False)
#%%%
# Creamos las tablas personas divididas por año desde los df de los censos (2010-2022)
consulta = """
            SELECT DISTINCT edad, sexo, cobertura, provincia AS provincia_id, cantidad
            FROM censo2010limpio
"""
personas2010 = dd.sql(consulta).df()
#personas2010.to_csv(carpeta+"\personas2010.csv", sep=";", index = False)

consulta = """
            SELECT DISTINCT edad, sexo, cobertura, provincia AS provincia_id, cantidad
            FROM censo2022limpio
"""
personas2022 = dd.sql(consulta).df()
#personas2022.to_csv(carpeta+"\personas2022.csv", sep=";", index = False)
#%%%