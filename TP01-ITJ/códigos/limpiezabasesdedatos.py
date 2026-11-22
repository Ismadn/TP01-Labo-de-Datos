#Integrantes: Di Niro Ismael, Domínguez Tomás, Ottaviano Jaime.

#En este archivo se desarrolla la limpieza de las bases de datos: censos, nacidos vivos y establecimientos de salud.
#Recordar que las bases que contengan datos para dos años diferentes siguen el mismo algoritmo de limpieza.

#Para correr el código deberás completar la variable "carpeta" con la dirección en donde tengas las bases de datos.
#En caso de querer descargar las bases limpias, quitar el "#" en las filas con código del tipo .to_csv

import pandas as pd
import duckdb as dd

carpeta = "Ruta de la carpeta donde estén tus archivos"

codigos_prov = {
    "BUENOS AIRES": 6,
    "CABA": 2,
    "CIUDAD AUTÓNOMA DE BUENOS AIRES": 2,
    "CATAMARCA": 10,
    "CHACO": 22,
    "CHUBUT": 26,
    "CORRIENTES": 18,
    "CÓRDOBA": 14,
    "ENTRE RÍOS": 30,
    "FORMOSA": 34,
    "JUJUY": 38,
    "LA PAMPA": 42,
    "LA RIOJA": 46,
    "MENDOZA": 50,
    "MISIONES": 54,
    "NEUQUÉN": 58,
    "RÍO NEGRO": 62,
    "SALTA": 66,
    "SAN JUAN": 70,
    "SAN LUIS": 74,
    "SANTA CRUZ": 78,
    "SANTA FE": 82,
    "SANTIAGO DEL ESTERO": 86,
    "TUCUMÁN": 90,
    "TIERRA DEL FUEGO": 94
}
#%%%%%%%%
#LIMPIEZA BASE DE DATOS CENSO 2010
censo2010 = pd.read_excel(carpeta + r"/censo2010.xlsx")
#El problema de esta base es que se abre "rara" y hay muchos nan. Debemos hacer una buena limpieza.
censo2010 = censo2010.iloc[13:,] #Elimino filas innecesarias
censo2010.columns = ["provincia","cobertura", "edad", "varon", "mujer", "total"]
censo2010 = censo2010.reset_index(drop=True)
provincia_actual = None
eliminar = []
for i in range(len(censo2010)):    #Algoritmo para detectar en qué provincia estoy y completar las filas necesarias
    if "AREA #" in str(censo2010.iloc[i, 1]):
        provincia_actual = censo2010.iloc[i, 2]
        eliminar.extend([i-1, i, i+1])
    if "Cobertura de salud" in str(censo2010.iloc[i,1]):
        eliminar.append(i)
    censo2010.iloc[i, 0] = provincia_actual
censo2010 = censo2010.drop(eliminar) #Elimino filas innecesarias
censo2010["cobertura"] = censo2010["cobertura"].ffill() #Le doy el último valor a todas las filas nan
censo2010 = censo2010.reset_index(drop=True) #Reseteo índices
resumen = censo2010[censo2010["cobertura"] == "RESUMEN"].index
censo2010 = censo2010.drop(censo2010.index[resumen[0]:]) #Elimino las filas de resumen
censo2010 = censo2010.drop(censo2010[(censo2010["cobertura"] == "Total")].index) #Elimino filas innecesarias
censo2010 = censo2010.drop(censo2010[(censo2010["edad"] == " Total")].index) 
censo2010 = censo2010.dropna(subset=["edad"]) 
censo2010.loc[censo2010["varon"] == "-", "varon"] = 0 #Los valores '-' los tomamos como que no hay personas con esa edad,
censo2010.loc[censo2010["mujer"] == "-", "mujer"] = 0 #por lo que decidimos reemplazar con 0
censo2010 = censo2010.melt(id_vars = ["provincia", "cobertura", "edad", "total"], #Ahora yo quiero juntar mis dos columnas
                           value_vars = ["varon", "mujer"], #en una sola llamada "sexo". Con melt le doy las columnas que
                           var_name = "sexo", #dejo fijas, las columnas a juntar, el nuevo nombre y el valor que debe tener.
                           value_name = "cantidad")
censo2010 = censo2010.sort_values(["provincia","cobertura", "edad"])
censo2010 = censo2010.drop(columns=["total"]) #La columna total no nos aporta info. necesaria
censo2010 = censo2010.reset_index(drop=True)
censo2010["provincia"] = censo2010["provincia"].astype(object) #Le cambio el tipo para poder reemplazar por un número
for i in censo2010.index: #Reemplazo los nombres de las provincias por sus id's
    provincia_nombre = censo2010.loc[i, "provincia"].upper()
    censo2010.loc[i, "provincia"] = codigos_prov[provincia_nombre]
    
#censo2010.to_csv(carpeta+"\censo2010limpio.csv", sep=";", index = False) Guardo mi base limpia para después exportar los esquemas
#%%%%%%%%
#LIMPIEZA BASE DE DATOS CENSO2022
censo2022 = pd.read_excel(carpeta + r"/censo2022.xlsx")

censo2022 = censo2022.iloc[13:,]    #Idem. censo2010
censo2022.columns = ["provincia","cobertura", "edad", "varon", "mujer", "total"]
censo2022 = censo2022.reset_index(drop=True)
provincia_actual = None
eliminar = []
for i in range(len(censo2022)):
    if "AREA #" in str(censo2022.iloc[i, 1]):
        provincia_actual = censo2022.iloc[i, 2]
        eliminar.extend([i-1, i, i+1])
    if "Cobertura de salud" in str(censo2022.iloc[i,1]):
        eliminar.append(i)
    censo2022.iloc[i, 0] = provincia_actual
censo2022 = censo2022.drop(eliminar)
censo2022["cobertura"] = censo2022["cobertura"].ffill()
censo2022 = censo2022.reset_index(drop=True) 
resumen = censo2022[censo2022["cobertura"] == "RESUMEN"].index
censo2022 = censo2022.drop(censo2022.index[resumen[0]:]) 
censo2022 = censo2022.drop(censo2022[(censo2022["cobertura"] == "Total")].index)
censo2022 = censo2022.drop(censo2022[(censo2022["edad"] == " Total")].index)
censo2022 = censo2022.dropna(subset=["edad"])
censo2022.loc[censo2022["varon"] == "-", "varon"] = 0
censo2022.loc[censo2022["mujer"] == "-", "mujer"] = 0
censo2022 = censo2022.melt(id_vars = ["provincia", "cobertura", "edad", "total"],
                           value_vars = ["varon", "mujer"],
                           var_name = "sexo",
                           value_name = "cantidad")
censo2022 = censo2022.sort_values(["provincia","cobertura", "edad"])
censo2022 = censo2022.drop(columns=["total"])
censo2022 = censo2022.reset_index(drop=True)
censo2022["provincia"] = censo2022["provincia"].astype(object)
for i in censo2022.index:
    provincia_nombre = censo2022.loc[i, "provincia"].upper()
    censo2022.loc[i, "provincia"] = codigos_prov[provincia_nombre]
#censo2022.to_csv(carpeta+"\censo2022limpio.csv", sep=";", index = False)
#%%%%%%%
centros = pd.read_excel(carpeta + r"\centros.xlsx")
# Acá notamos que algunas provincias repetían los id o tenían más de uno,
# así que lo que hicimos es corregir los id poniendo los que correspondían (según el INDEC)
for i in centros.index:
    provincia_nombre = centros.loc[i, "provincia_nombre"]
    centros.loc[i, "provincia_id"] = codigos_prov[provincia_nombre]
#centros.to_csv(carpeta+"\centroslimpio.csv", sep=";", index = False)
#%%%%%%%
nacweb10 = pd.read_csv(carpeta + r"\\nacweb10.csv", encoding="latin1")
nacweb22_0 = pd.read_csv(carpeta + r"\\nacweb22_0.csv", sep = ";")

#Acá lo primero que hacemos es limpiar las tablas nacweb10 y nacweb22 en las siguientes columnas:  
#       IMEDAD,ITIEMGES, IMINSTRUC, IPESONAC
# Lo que limpiamos es que antes de cada dato hay algo de este estilo '1.', 
# lo que hacemos es sacar eso para que sea más cómodo visualmente.
# También eliminamos los valores Sin especificar ya que no nos sirven para el análisis
# Nos armamos las tablas "limpias" y luego transformamos las originales        
consulta = """ 
            SELECT PROVRES,
                   TIPPARTO,
                   SEXO,
                   SUBSTRING(IMEDAD,3) AS IMEDAD, 
                   SUBSTRING(ITIEMGEST,3) AS ITIEMGES ,
                   SUBSTRING(IMINSTRUC,3) AS IMINSTRUC, 
                   SUBSTRING(IPESONAC,3) AS IPESONAC,
                   CUENTA
            FROM nacweb10
"""

nacweb10limpio= dd.sql(consulta).df() 
nacweb10limpio = nacweb10limpio.drop(nacweb10limpio[(nacweb10limpio["PROVRES"] == 98) | (nacweb10limpio["PROVRES"] == 99)].index)
nacweb10limpio = nacweb10limpio.drop(nacweb10limpio[(nacweb10limpio["IMEDAD"] == 'Sin especificar')].index)
#nacweb10limpio.to_csv(carpeta+r"\nacweb10limpio.csv", sep=";", index = False)

consulta = """ 
            SELECT PROVRES,
                   TIPPARTO,
                   SEXO,
                   SUBSTRING(IMEDAD,3) AS IMEDAD, 
                   SUBSTRING(ITIEMGEST,3) AS ITIEMGES ,
                   SUBSTRING(IMINSTRUC,3) AS IMINSTRUC, 
                   SUBSTRING(IPESONAC,3) AS IPESONAC,
                   CUENTA
            FROM nacweb22_0
"""

nacweb22limpio = dd.sql(consulta).df() 
nacweb22limpio = nacweb22limpio.drop(nacweb22limpio[(nacweb22limpio["PROVRES"] == 98) | (nacweb22limpio["PROVRES"] == 99)].index)
nacweb22limpio = nacweb22limpio.drop(nacweb22limpio[(nacweb22limpio["IMEDAD"] == 'Sin especificar')].index)
#nacweb22limpio.to_csv(carpeta+r"\nacweb22limpio.csv", sep=";", index = False)
#%%%%%%