#Integrantes: Di Niro Ismael, Domínguez Tomás, Ottaviano Jaime.

#En este archivo, a partir de esquemas, generamos reportes con consultas SQL y gráficos para luego analizarlos y sacar
#las conclusiones necesarias.

#Para correr el código deberás completar la variable "carpeta" con la dirección en donde tengas los esquemas.
#Se recomienda recorrer las celdas en orden.

import pandas as pd
import duckdb as dd
import matplotlib.pyplot as plt

carpeta = "Ruta de la carpeta donde estén tus archivos"

provincias = pd.read_csv(carpeta + r"\provincias.csv", sep = ";")
personas2010 = pd.read_csv(carpeta + r"\personas2010.csv", sep = ";")
personas2022 = pd.read_csv(carpeta + r"\personas2022.csv", sep = ";")
centros_medicos = pd.read_csv(carpeta + r"\centros_medicos.csv", sep = ";")
departamentos = pd.read_csv(carpeta + r"\departamentos.csv", sep = ";")
madres2010 = pd.read_csv(carpeta + r"\madres2010.csv", sep = ";")
madres2022 = pd.read_csv(carpeta + r"\madres2022.csv", sep = ";")
nacidos2010 = pd.read_csv(carpeta + r"\nacidos2010.csv", sep = ";")
nacidos2022 = pd.read_csv(carpeta + r"\nacidos2022.csv", sep = ";")

#%%
#Cobertura de salud

concobertura2010 = """
            SELECT provincia_id,
            CASE WHEN (edad >= 0 AND edad <= 9) THEN '0-9' 
                WHEN (edad >= 10 AND edad <= 18) THEN '10-18'
                WHEN (edad >= 19 AND edad <= 34) THEN '19-34'
                WHEN (edad >= 35 AND edad <= 50) THEN '35-50'
                WHEN (edad >= 51 AND edad <= 64) THEN '51-64'
                ELSE '65+'
            END AS rango_edad,
            SUM(cantidad) AS Cantidad
            FROM personas2010
            WHERE cobertura != 'No tiene obra social, prepaga o plan estatal'
            GROUP BY provincia_id, rango_edad
            """
concobertura2010 = dd.sql(concobertura2010).df()
sincobertura2010 = """
            SELECT provincia_id,
            CASE WHEN (edad >= 0 AND edad <= 9) THEN '0-9' 
                WHEN (edad >= 10 AND edad <= 18) THEN '10-18'
                WHEN (edad >= 19 AND edad <= 34) THEN '19-34'
                WHEN (edad >= 35 AND edad <= 50) THEN '35-50'
                WHEN (edad >= 51 AND edad <= 64) THEN '51-64'
                ELSE '65+'
            END AS rango_edad,
            SUM(cantidad) AS Cantidad
            FROM personas2010
            WHERE cobertura == 'No tiene obra social, prepaga o plan estatal'
            GROUP BY provincia_id, rango_edad
            """
sincobertura2010 = dd.sql(sincobertura2010).df()
concobertura2022 = """
            SELECT provincia_id,
            CASE WHEN (edad >= 0 AND edad <= 9) THEN '0-9' 
                WHEN (edad >= 10 AND edad <= 18) THEN '10-18'
                WHEN (edad >= 19 AND edad <= 34) THEN '19-34'
                WHEN (edad >= 35 AND edad <= 50) THEN '35-50'
                WHEN (edad >= 51 AND edad <= 64) THEN '51-64'
                ELSE '65+'
            END AS rango_edad,
            SUM(cantidad) AS Cantidad
            FROM personas2022
            WHERE cobertura != 'No tiene obra social, prepaga ni plan estatal'
            GROUP BY provincia_id, rango_edad
            """
concobertura2022 = dd.sql(concobertura2022).df()
sincobertura2022 = """
            SELECT provincia_id,
            CASE WHEN (edad >= 0 AND edad <= 9) THEN '0-9' 
                WHEN (edad >= 10 AND edad <= 18) THEN '10-18'
                WHEN (edad >= 19 AND edad <= 34) THEN '19-34'
                WHEN (edad >= 35 AND edad <= 50) THEN '35-50'
                WHEN (edad >= 51 AND edad <= 64) THEN '51-64'
                ELSE '65+'
            END AS rango_edad,
            SUM(cantidad) AS Cantidad
            FROM personas2022
            WHERE cobertura == 'No tiene obra social, prepaga ni plan estatal'
            GROUP BY provincia_id, rango_edad
            """
sincobertura2022 = dd.sql(sincobertura2022).df()
cobertura1 = """
            SELECT con2010.provincia_id, con2010.rango_edad, con2010.Cantidad AS cantidad_con_cobertura_2010,
            sin2010.Cantidad AS cantidad_sin_cobertura_2010, con2022.Cantidad AS cantidad_con_cobertura_2022,
            sin2022.Cantidad AS cantidad_sin_cobertura_2022
            FROM concobertura2010 AS con2010
            LEFT OUTER JOIN sincobertura2010 AS sin2010
            ON con2010.provincia_id = sin2010.provincia_id AND con2010.rango_edad = sin2010.rango_edad
            LEFT OUTER JOIN sincobertura2022 AS sin2022
            ON con2010.provincia_id = sin2022.provincia_id AND con2010.rango_edad = sin2022.rango_edad
            LEFT OUTER JOIN concobertura2022 AS con2022
            ON con2010.provincia_id = con2022.provincia_id AND con2010.rango_edad = con2022.rango_edad
            
"""
cobertura1 = dd.sql(cobertura1).df()
coberturaDeSalud = """
            SELECT p.nombre AS provincia, c.rango_edad, c.cantidad_con_cobertura_2010, c.cantidad_sin_cobertura_2010,
            c.cantidad_con_cobertura_2022, c.cantidad_sin_cobertura_2022
            FROM cobertura1 AS c
            LEFT OUTER JOIN provincias AS p
            ON p.id = c.provincia_id
            ORDER BY p.nombre, c.rango_edad
"""
coberturaDeSalud = dd.sql(coberturaDeSalud).df()
#%%
#Establecimientos de salud con terapia intensiva
consulta = """ 
     SELECT p.nombre AS Provincia,
            c.origen_financiamiento,
            COUNT(*) AS cantidad_total
    FROM centros_medicos AS c
    INNER JOIN provincias AS p
    ON p.id = c.provincia_id
    WHERE c.tipologia_id = 10 
    GROUP BY p.nombre,c.origen_financiamiento
    ORDER BY cantidad_total DESC
"""
Establecimientos_de_salud_con_terapia_intensiva = dd.sql(consulta).df()
#%%
#Características de los nacimientos
consulta = """ 
            SELECT m.provincia_id,
                   CASE WHEN m.rango_edad = 'Menor de 15' THEN '0 a 15'
                         ELSE m.rango_edad 
                         END AS rango_edad_madre,
                   SUM(n.cantidad) AS cantidad_total_nacidos,
                   SUM(CASE WHEN n.peso_al_nacer = 'Menos de 2500 gramos'
                             THEN n.cantidad
                             ELSE 0 
                       END) / SUM(n.cantidad) * 100 AS  porcentaje_bajo_peso_al_nacer
            FROM madres2010 AS m
            INNER JOIN nacidos2010 AS n
                    ON m.id = n.id_madre
            WHERE m.rango_edad <> 'Sin especificar'
            GROUP BY m.provincia_id, 
                     m.rango_edad 
            ORDER BY m.provincia_id ASC, 
                     m.rango_edad ASC
"""
Caracteristicas_de_los_nacimientos2010 = dd.sql(consulta).df() 

consulta = """ 
            SELECT m.provincia_id,
                   CASE WHEN m.rango_edad = 'Menor de 15' THEN '0 a 15'
                         ELSE m.rango_edad 
                         END AS rango_edad_madre,
                   SUM(n.cantidad) AS cantidad_total_nacidos,
                   SUM(CASE WHEN n.peso_al_nacer = 'Menos de 2500 gramos'
                             THEN n.cantidad
                             ELSE 0 
                       END) / SUM(n.cantidad) * 100 AS  porcentaje_bajo_peso_al_nacer
            FROM madres2022 AS m
            INNER JOIN nacidos2022 AS n
                    ON m.id = n.id_madre
             WHERE m.rango_edad <> 'Sin especificar'
            GROUP BY m.provincia_id, 
                     m.rango_edad 
            ORDER BY m.provincia_id ASC, 
                     m.rango_edad ASC
"""
Caracteristicas_de_los_nacimientos2022 = dd.sql(consulta).df() 


consulta = """
           SELECT c22.provincia_id,
                  c10.rango_edad_madre, 
                  c10.cantidad_total_nacidos AS cantidad_total_nacidos2010,
                  c22.cantidad_total_nacidos AS cantidad_total_nacidos2022,
                  c10.porcentaje_bajo_peso_al_nacer AS porcentaje_bajo_peso_al_nacer2010,
                  c22.porcentaje_bajo_peso_al_nacer AS porcentaje_bajo_peso_al_nacer2022
           FROM Caracteristicas_de_los_nacimientos2010 AS c10
           INNER JOIN Caracteristicas_de_los_nacimientos2022 AS c22
                       ON c22.provincia_id = c10.provincia_id
                       AND c22.rango_edad_madre = c10.rango_edad_madre
           ORDER BY provincia_id ASC, rango_edad_madre ASC
""" 

tabla_temp = dd.sql(consulta).df()

consulta = """ 
            SELECT p.nombre AS provincia,
                   t.rango_edad_madre,
                   t.cantidad_total_nacidos2010,
                   t.cantidad_total_nacidos2022,
                   t.porcentaje_bajo_peso_al_nacer2010,
                   t.porcentaje_bajo_peso_al_nacer2022
            FROM tabla_temp AS t
            INNER JOIN provincias AS p
                    ON t.provincia_id = p.id
            ORDER BY provincia ASC, rango_edad_madre ASC
"""
caracteristicas_de_los_nacimientos = dd.sql(consulta).df()
#%%
#Tasa de fecundidad por provincia (2022)
consulta = """ 
            SELECT m.provincia_id,
                   m.rango_edad,
                   SUM(n.cantidad) AS cantidad_nacidos
            FROM madres2022 AS m
            INNER JOIN nacidos2022 AS n
                    ON n.id_madre = m.id
            GROUP BY m.provincia_id, m.rango_edad
            ORDER BY m.provincia_id ASC, m.rango_edad ASC
"""
tabla_nacimientos_2022= dd.sql(consulta).df()
consulta = """ 
        SELECT provincia_id,
               CASE WHEN(edad < 15) THEN 'Menor de 15'
                    WHEN (edad >= 15 AND edad <= 19) THEN '15 a 19'
                    WHEN (edad >= 20 AND edad <= 24) THEN '20 a 24'
                    WHEN (edad >= 25 AND edad <= 29) THEN '25 a 29'
                    WHEN (edad >= 30 AND edad <= 34) THEN '30 a 34'
                    WHEN (edad >= 35 AND edad <= 39) THEN '35 a 39'
                    WHEN (edad >= 40 AND edad <= 44) THEN '40 a 44'
                    WHEN (edad >= 45) THEN 'De 45 y más' 
                END AS rango_edad,
                SUM(CAST(cantidad AS INTEGER)) AS cantidad_mujeres
        FROM personas2022
        WHERE sexo = 'mujer'
        GROUP BY provincia_id, 
                 rango_edad
        ORDER BY provincia_id ASC, rango_edad ASC     
"""

tabla_mujeres_total_2022 = dd.sql(consulta).df()
consulta = """ 
            SELECT n.provincia_id,
                   n.rango_edad AS rango_edad_madre,
                   n.cantidad_nacidos,
                   m.cantidad_mujeres,
                  (n.cantidad_nacidos / m.cantidad_mujeres) * 1000 AS tasa_fecundidad
            FROM tabla_nacimientos_2022 AS n
            INNER JOIN tabla_mujeres_total_2022 AS m
                    ON n.provincia_id = m.provincia_id AND n.rango_edad = m.rango_edad
"""
tabla_temp= dd.sql(consulta).df() 
tabla_temp.loc[tabla_temp["rango_edad_madre"] == "Menor de 15","rango_edad_madre"] = "0 a 15"
#Modificamos esto para poder tener un orden correcto de los rangos etarios
consulta = """ 
            SELECT p.nombre, t.rango_edad_madre, t.tasa_fecundidad 
            FROM tabla_temp AS t
            LEFT OUTER JOIN provincias AS p
            ON p.id = t.provincia_id
            ORDER BY t.tasa_fecundidad DESC
"""

tasa_de_fecundidad_por_provincia_2022 = dd.sql(consulta).df()
#%%
#Cambios en la edad de las madres
menores2010 = """
                SELECT provincia_id, COUNT(*) * 100 / (SELECT COUNT(*)
                                                       FROM madres2010) AS 'porcentaje'
                FROM madres2010
                WHERE rango_edad = '15 a 19' OR rango_edad = 'Menor de 15'
                GROUP BY provincia_id
            """ 
menores2010 = dd.sql(menores2010).df()

menores2022 = """
                SELECT provincia_id, COUNT(*) * 100 / (SELECT COUNT(*)
                                                       FROM madres2022) AS 'porcentaje'
                FROM madres2022
                WHERE rango_edad = '15 a 19' OR rango_edad = 'Menor de 15'
                GROUP BY provincia_id
            """
menores2022 = dd.sql(menores2022).df()            
diferencia = """
                SELECT d10.provincia_id, d22.porcentaje - d10.porcentaje AS 'Diferencia porc. madres menores a 20 entre 2010-2022'
                FROM menores2010 AS d10
                LEFT OUTER JOIN menores2022 AS d22
                ON d10.provincia_id = d22.provincia_id
                ORDER BY "Diferencia porc. madres menores a 20 entre 2010-2022" DESC
            """
diferencia = dd.sql(diferencia).df()
cambios_edad_madres = """
                        SELECT p.nombre AS Provincia, d."Diferencia porc. madres menores a 20 entre 2010-2022"
                        FROM diferencia AS d
                        LEFT OUTER JOIN provincias AS p
                        ON p.id = d.provincia_id
                        ORDER BY d."Diferencia porc. madres menores a 20 entre 2010-2022" DESC
                    """
cambios_edad_madres = dd.sql(cambios_edad_madres).df()
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#INFORMACIÓN UTILIZANDO HERRAMIENTAS DE VISUALIZACIÓN

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#Cantidad de habitantes por provincia
habitantes2010 = """
            SELECT provincia_id, SUM(cantidad) AS habitantes_2010
            FROM personas2010
            GROUP BY provincia_id
            ORDER BY habitantes_2010 DESC
            """
habitantes2010 = dd.sql(habitantes2010).df()
habitantes2022 = """
                SELECT provincia_id, SUM(cantidad) AS habitantes_2022
                FROM personas2022
                GROUP BY provincia_id
                ORDER BY habitantes_2022 DESC
"""
habitantes2022 = dd.sql(habitantes2022).df()
grafico_habitantes = """
            SELECT p.nombre AS provincia, h10.habitantes_2010, h22.habitantes_2022
            FROM habitantes2010 AS h10
            LEFT OUTER JOIN habitantes2022 AS h22
            ON h10.provincia_id = h22.provincia_id
            LEFT OUTER JOIN provincias AS p
            ON h10.provincia_id = p.id
            GROUP BY provincia, h10.habitantes_2010, h22.habitantes_2022
            ORDER BY h10.habitantes_2010 ASC, h22.habitantes_2022 ASC
"""
grafico_habitantes = dd.sql(grafico_habitantes).df()

fig, ax = plt.subplots()
grafico_habitantes.plot(x="provincia", y= ["habitantes_2010", "habitantes_2022"],
                        kind = "barh", label = ["2010", "2022"], ax=ax, grid= True, figsize = (10,8), width=0.8)
plt.xlabel("Cantidad de habitantes")
plt.ylabel("Provincia")
plt.title("Cantidad de habitantes por provincia por año")
#%%
#Nacimientos prematuros según provincia
consulta = """ 
            SELECT m.provincia_id,
                   SUM (CASE WHEN n.tiempo_gestacion = 'Menos de 22'
                             OR n.tiempo_gestacion = '22 a 23'
                             OR n.tiempo_gestacion = '24 a 27'
                             OR n.tiempo_gestacion = '28 a 31'
                             OR n.tiempo_gestacion = '32 a 36'
                             THEN n.cantidad
                             ELSE 0 
                             END) / SUM (CASE WHEN n.tiempo_gestacion <> 'Sin especificar' 
                                               THEN n.cantidad
                                               ELSE 0
                                            END) * 100 AS porcentaje_prematuros
            FROM madres2010 AS m
            INNER JOIN nacidos2010 AS n
                    ON m.id = n.id_madre
            GROUP BY m.provincia_id
            ORDER BY m.provincia_id ASC 
"""

porcentaje_prematuros2010 = dd.sql(consulta).df() 


consulta = """ 
            SELECT m.provincia_id,
                   SUM (CASE WHEN n.tiempo_gestacion = 'Menos de 22'
                             OR n.tiempo_gestacion = '22 a 23'
                             OR n.tiempo_gestacion = '24 a 27'
                             OR n.tiempo_gestacion = '28 a 31'
                             OR n.tiempo_gestacion = '32 a 36'
                             THEN n.cantidad
                             ELSE 0 
                             END) / SUM (CASE WHEN n.tiempo_gestacion <> 'Sin especificar' 
                                               THEN n.cantidad
                                               ELSE 0
                                            END) * 100 AS porcentaje_prematuros
            FROM madres2022 AS m
            INNER JOIN nacidos2022 AS n
                    ON m.id = n.id_madre
            GROUP BY m.provincia_id
            ORDER BY m.provincia_id ASC 
"""

porcentaje_prematuros2022 = dd.sql(consulta).df() 


consulta = """ 
            SELECT p10.provincia_id, 
                   p10.porcentaje_prematuros AS porcentaje_prematuros_2010,
                   p22.porcentaje_prematuros AS porcentaje_prematuros_2022
            FROM porcentaje_prematuros2010 AS p10
            INNER JOIN porcentaje_prematuros2022 AS p22
                        ON p10.provincia_id = p22.provincia_id
            ORDER BY p10.provincia_id ASC
"""

porcentaje_prematuros_2010_2022 = dd.sql(consulta).df() 

consulta = """ 
            SELECT p.nombre AS nombre_provincia,
                   p1022.porcentaje_prematuros_2010,
                   p1022.porcentaje_prematuros_2022
            FROM provincias AS p
            INNER JOIN porcentaje_prematuros_2010_2022 AS p1022
                        ON p.id = p1022.provincia_id
            ORDER BY porcentaje_prematuros_2022, porcentaje_prematuros_2010
"""
porcentaje_prematuros_provincias_2010_2022 = dd.sql(consulta).df()



fig, ax = plt.subplots()
x = range((len(porcentaje_prematuros_provincias_2010_2022)))
ancho = 0.4

ax.barh ([i+ancho/2 for i in x], 
         porcentaje_prematuros_provincias_2010_2022["porcentaje_prematuros_2010"],
         height=ancho,
         label="2010")

ax.barh ([i-ancho/2 for i in x], 
         porcentaje_prematuros_provincias_2010_2022["porcentaje_prematuros_2022"],
         height=ancho,
         label="2022")

ax.set_yticks (x,
               porcentaje_prematuros_provincias_2010_2022["nombre_provincia"])
ax.tick_params(axis="y", labelsize=6)


ax.set_ylabel ("Provincias")
ax.set_xlabel ("Porcentajes de nacimientos prematuros ")
ax.set_title ("Porcentajes de nacimientos prematuros por provincia años 2010-2022")
ax.legend ()
ax.grid(axis="x")
#%%
#Tasa de fecundidad por provincia en 2022
consulta = """ 
            SELECT m.provincia_id,
                   SUM(n.cantidad) AS cantidad_nacidos
            FROM madres2022 AS m
            INNER JOIN nacidos2022 AS n
                    ON n.id_madre = m.id
            WHERE m.rango_edad = '15 a 19'
               OR m.rango_edad = '20 a 24'
               OR m.rango_edad = '25 a 29'
               OR m.rango_edad = '30 a 34'
               OR m.rango_edad = '35 a 39'
               OR m.rango_edad = '40 a 44'
               OR m.rango_edad = 'De 45 y más'
            GROUP BY m.provincia_id,
            ORDER BY m.provincia_id ASC
"""
tabla_rango_edad_15_49= dd.sql(consulta).df()
 
consulta = """ 
        SELECT provincia_id,
               SUM(CAST(cantidad AS INTEGER)) AS cantidad_mujeres
        FROM personas2022
        WHERE sexo = 'mujer'
            AND edad >= 15
            AND edad <= 49
        GROUP BY provincia_id 
        ORDER BY provincia_id ASC
"""

tabla_mujeres_total_rango_edad_15_49 = dd.sql(consulta).df() 


consulta = """ 
            SELECT n.provincia_id,
                   n.cantidad_nacidos,
                   m.cantidad_mujeres,
                  (n.cantidad_nacidos / m.cantidad_mujeres) * 1000 AS tasa_fecundidad
            FROM tabla_rango_edad_15_49 AS n
            INNER JOIN tabla_mujeres_total_rango_edad_15_49 AS m
                    ON n.provincia_id = m.provincia_id 
"""
tabla_temp= dd.sql(consulta).df() 

consulta = """ 
            SELECT p.nombre AS nombre_provincia,
                   t.tasa_fecundidad
            FROM tabla_temp AS t
            INNER JOIN provincias AS p
                        ON p.id = t.provincia_id
            ORDER BY t.tasa_fecundidad
"""

tasa_de_fecundidad_por_provincia_2022 = dd.sql(consulta).df()

fig, ax = plt.subplots() 

x = range(len(tasa_de_fecundidad_por_provincia_2022))
 

ax.barh(x,
         tasa_de_fecundidad_por_provincia_2022["tasa_fecundidad"])
         
         
ax.set_yticks(x,
              tasa_de_fecundidad_por_provincia_2022["nombre_provincia"])

ax.tick_params(axis='y',labelsize = 6)

ax.set_xlabel("Tasas de fecundidad")
ax.set_ylabel("Provincias") 
ax.set_title("Tasa de Fecundidad por Provincia año 2022")
ax.grid(axis="x")

consulta = """ 
            SELECT m.provincia_id,
                    n.tipo_parto,
                   SUM(n.cantidad) AS cantidad_nacidos
            FROM madres2022 AS m
            INNER JOIN nacidos2022 AS n
                    ON n.id_madre = m.id
            WHERE (m.rango_edad = '15 a 19'
               OR m.rango_edad = '20 a 24'
               OR m.rango_edad = '25 a 29'
               OR m.rango_edad = '30 a 34'
               OR m.rango_edad = '35 a 39'
               OR m.rango_edad = '40 a 44'
               OR m.rango_edad = 'De 45 y más')
               AND n.tipo_parto <> 9 
            GROUP BY m.provincia_id,
                     n.tipo_parto
            ORDER BY  n.tipo_parto ASC
"""
tabla_rango_edad_tipo_parto= dd.sql(consulta).df()
 
consulta = """ 
        SELECT provincia_id,
               SUM(CAST(cantidad AS INTEGER)) AS cantidad_mujeres
        FROM personas2022
        WHERE sexo = 'mujer'
            AND edad >= 15
            AND edad <= 49
        GROUP BY provincia_id 
        
"""

tabla_mujeres_total_rango_edad_15_49 = dd.sql(consulta).df() 


consulta = """ 
            SELECT n.provincia_id,
                   n.tipo_parto,
                   n.cantidad_nacidos,
                   m.cantidad_mujeres,
                  (n.cantidad_nacidos / m.cantidad_mujeres) * 1000 AS tasa_fecundidad
            FROM tabla_rango_edad_tipo_parto AS n
            INNER JOIN tabla_mujeres_total_rango_edad_15_49 AS m
                    ON n.provincia_id = m.provincia_id 
"""
tabla_temp= dd.sql(consulta).df() 

consulta = """ 
            SELECT p.nombre AS nombre_provincia,
                   t.tasa_fecundidad,
                   t.tipo_parto
            FROM tabla_temp AS t
            INNER JOIN provincias AS p
                        ON p.id = t.provincia_id
            ORDER BY t.tasa_fecundidad, 
                     t.tipo_parto ASC
"""

tasa_de_fecundidad_tipo_parto = dd.sql(consulta).df()

fig, ax = plt.subplots()
x = range((len(tasa_de_fecundidad_tipo_parto["nombre_provincia"].unique())))
ancho = 0.4 


ax.barh ([i+ancho/2 for i in x], 
         tasa_de_fecundidad_tipo_parto[tasa_de_fecundidad_tipo_parto["tipo_parto"] == 1]["tasa_fecundidad"],
         height=ancho,
         label="Simple")

ax.barh ([i-ancho/2 for i in x], 
         tasa_de_fecundidad_tipo_parto[tasa_de_fecundidad_tipo_parto["tipo_parto"] == 2]["tasa_fecundidad"],
         height=ancho,
         label="Multiple") 


ax.set_yticks(
    x,
    tasa_de_fecundidad_tipo_parto[
        tasa_de_fecundidad_tipo_parto["tipo_parto"] == 1]["nombre_provincia"])
ax.tick_params(axis="y", labelsize=6)


ax.set_ylabel ("Provincias")
ax.set_xlabel ("Tasa de fecundidad ")
ax.set_title ("Tasas de fecundidad dependiendo el tipo de parto año 2022")
ax.legend ()
ax.grid(axis="x")
#%%
#Peso al nacer según el nivel de instrucción de la madre
nacimientosporprov = """
                    SELECT m.provincia_id, SUM(n.cantidad) AS cantidad
                    FROM madres2022 AS m
                    LEFT OUTER JOIN nacidos2022 AS n
                    ON m.id = n.id_madre
                    WHERE m.nivel_educacion != 'Sin especificar'
                    GROUP BY m.provincia_id
"""
nacimientosporprov = dd.sql(nacimientosporprov).df()
primaria_completa = """
                    SELECT m.provincia_id, m.nivel_educacion, 
                    SUM(CASE WHEN n.peso_al_nacer = 'Menos de 2500 gramos' 
                    THEN n.cantidad ELSE 0 END) * 100 / 
                    c.cantidad AS "porcentaje"
                    FROM madres2022 AS m
                    LEFT OUTER JOIN nacidos2022 AS n
                    ON m.id = n.id_madre
                    LEFT OUTER JOIN nacimientosporprov AS c
                    ON m.provincia_id = c.provincia_id
                    WHERE m.nivel_educacion = 'Hasta Primaria/C.EGB Completa'
                    GROUP BY m.provincia_id, m.nivel_educacion, c.cantidad
                    """
primaria_completa = dd.sql(primaria_completa).df()
secundaria_incompleta = """
                    SELECT m.provincia_id, m.nivel_educacion, 
                    SUM(CASE WHEN n.peso_al_nacer = 'Menos de 2500 gramos' 
                    THEN n.cantidad ELSE 0 END) * 100 / 
                    c.cantidad AS "porcentaje"
                    FROM madres2022 AS m
                    LEFT OUTER JOIN nacidos2022 AS n
                    ON m.id = n.id_madre
                    LEFT OUTER JOIN nacimientosporprov AS c
                    ON m.provincia_id = c.provincia_id
                    WHERE m.nivel_educacion = 'Secundaria/Polimodal Incompleta'
                    GROUP BY m.provincia_id, m.nivel_educacion, c.cantidad
                    """
secundaria_incompleta = dd.sql(secundaria_incompleta).df()
secundaria_completa = """
                    SELECT m.provincia_id, m.nivel_educacion, 
                    SUM(CASE WHEN n.peso_al_nacer = 'Menos de 2500 gramos' 
                    THEN n.cantidad ELSE 0 END) * 100 / 
                    c.cantidad AS "porcentaje"
                    FROM madres2022 AS m
                    LEFT OUTER JOIN nacidos2022 AS n
                    ON m.id = n.id_madre
                    LEFT OUTER JOIN nacimientosporprov AS c
                    ON m.provincia_id = c.provincia_id
                    WHERE m.nivel_educacion = 'Secundario/Polimodal Completa y más'
                    GROUP BY m.provincia_id, m.nivel_educacion, c.cantidad
                    """
secundaria_completa = dd.sql(secundaria_completa).df()
grafico_pesos_bajos = """
            SELECT p.nombre AS provincia, pc.porcentaje AS 'Primaria completa', si.porcentaje AS 'Secundaria incompleta',
            sc.porcentaje AS 'Secundaria completa'
            FROM provincias AS p
            LEFT OUTER JOIN primaria_completa AS pc
            ON p.id = pc.provincia_id
            LEFT OUTER JOIN secundaria_incompleta AS si
            ON p.id = si.provincia_id
            LEFT OUTER JOIN secundaria_completa AS sc
            ON p.id = sc.provincia_id
            GROUP BY p.nombre, pc.porcentaje, si.porcentaje, sc.porcentaje
            ORDER BY sc.porcentaje, si.porcentaje, pc.porcentaje
"""
grafico_pesos_bajos = dd.sql(grafico_pesos_bajos).df()


grafico_pesos_bajos.plot(x = "provincia", y = ["Primaria completa", "Secundaria incompleta", "Secundaria completa"], 
                         kind = "barh", grid=True, figsize = (15,8), width=0.8)
plt.xlabel("Porcentaje de nacimientos con bajo peso")
plt.ylabel("Provincia")
plt.title("Porcentaje de nacimientos según nivel de instrucción de la madre (2022)")

#%%
#Distribución de establecimientos de salud
consulta = """ 
            SELECT d.provincia_id,
                   d.id AS id_departamento,
                  COUNT(c.id) AS cantidad_centros_medicos
            FROM departamentos AS d
            INNER JOIN centros_medicos AS c
                    ON d.id = c.departamento_id
            GROUP BY d.provincia_id,
                     d.id,
            ORDER BY d.provincia_id ASC, cantidad_centros_medicos ASC
                                            
"""

cantidad_establecimientos_por_depto = dd.sql(consulta).df()

consulta = """ 
            SELECT p.nombre AS nombre_provincia,
                   c.id_departamento,
                   c.cantidad_centros_medicos
            FROM cantidad_establecimientos_por_depto AS c
            INNER JOIN provincias AS p
                    ON p.id = c.provincia_id
            ORDER BY p.id ASC
"""
distribucion_de_establecimientos_de_salud = dd.sql(consulta).df() 

fig,ax = plt.subplots()


cant_por_provincia = [] 
nombre_provincias = provincias["nombre"]
for provincia in nombre_provincias: 
    cant_por_provincia.append(distribucion_de_establecimientos_de_salud[distribucion_de_establecimientos_de_salud["nombre_provincia"] == provincia]["cantidad_centros_medicos"])

ax.boxplot(cant_por_provincia)

ax.set_xticks(range(1,len(nombre_provincias)+1),nombre_provincias)

ax.tick_params(axis= "x", labelsize= 6,rotation= 90)


ax.set_xlabel("Provincias")
ax.set_ylabel("Cantidad de establecimientos")
ax.set_title("Distribución de establecimientos de salud por departamento")
ax.grid(axis="x")
#%%
#Gráfico a elección: Diferencia entre la tasa de fecundidad entre los años 2010-2022
consulta = """ 
            SELECT m.provincia_id,
                   SUM(n.cantidad) AS cantidad_nacidos
            FROM madres2010 AS m
            INNER JOIN nacidos2010 AS n
                    ON n.id_madre = m.id
            WHERE m.rango_edad = '15 a 19'
               OR m.rango_edad = '20 a 24'
               OR m.rango_edad = '25 a 29'
               OR m.rango_edad = '30 a 34'
               OR m.rango_edad = '35 a 39'
               OR m.rango_edad = '40 a 44'
               OR m.rango_edad = 'De 45 y más'
            GROUP BY m.provincia_id,
            ORDER BY m.provincia_id ASC
"""
tabla_rango_edad_15_49_2010= dd.sql(consulta).df()
 


consulta = """ 
        SELECT provincia_id,
               SUM(CAST(cantidad AS INTEGER)) AS cantidad_mujeres
        FROM personas2010
        WHERE sexo = 'mujer'
            AND edad >= 15
            AND edad <= 49
        GROUP BY provincia_id 
        ORDER BY provincia_id ASC
"""
tabla_mujeres_total_rango_edad_15_49_2010 = dd.sql(consulta).df() 




consulta = """ 
            SELECT n.provincia_id,
                  (n.cantidad_nacidos / m.cantidad_mujeres) * 1000 AS tasa_fecundidad
            FROM tabla_rango_edad_15_49_2010 AS n
            INNER JOIN tabla_mujeres_total_rango_edad_15_49 AS m
                    ON n.provincia_id = m.provincia_id 
"""
tasa_2010= dd.sql(consulta).df() 



consulta = """ 
            SELECT p.nombre AS provincia,
                   t10.tasa_fecundidad
            FROM tasa_2010 AS t10
            INNER JOIN provincias AS p
                        ON p.id = t10.provincia_id
"""
tasa_2010 = dd.sql(consulta).df()

diferencia_tasas = """
                    SELECT t10.provincia, t10.tasa_fecundidad - t22.tasa_fecundidad AS "Diferencia tasa fecundidad"
                    FROM tasa_2010 AS t10
                    LEFT OUTER JOIN tasa_de_fecundidad_por_provincia_2022 AS t22
                    ON t10.provincia = t22.nombre_provincia
                    ORDER BY "Diferencia tasa fecundidad"
                    """
diferencia_tasas = dd.sql(diferencia_tasas).df()

diferencia_tasas.plot(x = "provincia", y = "Diferencia tasa fecundidad", 
                         kind = "barh", grid=True, figsize = (15,8), width=0.6, color="orange")
plt.xlabel("Diferencia en la tasa de fecundidad")
plt.ylabel("Provincia")
plt.title("Diferencia en la tasa de fecundidad por provincia 2010-2022")
#%%
#Como datos extras, decidimos calcular la cantidad de centros de acceso público y general que hay para cada provincia.
cant_centros_publicos = """
                    SELECT p.nombre, COUNT(*) AS cantidad
                    FROM centros_medicos AS c
                    LEFT OUTER JOIN provincias AS p
                    ON p.id = c.provincia_id
                    WHERE (c.origen_financiamiento = 'Universitario público' OR c.origen_financiamiento = 'Municipal'
                    OR c.origen_financiamiento = 'Provincial')
                    GROUP BY p.nombre
                    ORDER BY cantidad
"""
cant_centros_publicos = dd.sql(cant_centros_publicos).df()
#%%
#Cantidad de centros de salud por provincia
centros_por_provincia = """
                    SELECT p.nombre, COUNT(*) AS cantidad
                    FROM centros_medicos AS c
                    LEFT OUTER JOIN provincias AS p
                    ON p.id = c.provincia_id
                    GROUP BY p.nombre
                    ORDER BY cantidad
"""
centros_por_provincia = dd.sql(centros_por_provincia).df()