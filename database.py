import sqlite3 as sql
import pandas as pd


conn = sql.connect("base_de_datos.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Residentes(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_completo TEXT,
        edad INTEGER,
        fecha_inscripcion TEXT
    )
""")

def anadir_residente_db(nombre_completo, edad, fecha_inscripcion):
    cursor.execute("INSERT INTO Residentes VALUES (null, ?, ?, ?)", (nombre_completo, edad, fecha_inscripcion,))
    conn.commit()

def busqueda_residente_db(query):
    cursor.execute("SELECT nombre_completo FROM Residentes WHERE nombre_completo LIKE ?", (f'%{query}%',))
    resultados = cursor.fetchall()
    return resultados

def obtener_residentes():
    cursor.execute("SELECT nombre_completo FROM Residentes")
    resultados = cursor.fetchall()
    return resultados

def eliminar_residente(nombre_completo):
    cursor.execute("DELETE FROM Residentes WHERE nombre_completo = ?", (nombre_completo,))
    conn.commit()

def obtener_datos(nombre_completo):
    cursor.execute("SELECT * FROM Residentes WHERE nombre_completo = ?", (nombre_completo,))
    datos = cursor.fetchall()
    return datos[0]

def actualizar_datos_db(nombre_completo_nuevo, edad_nueva, fecha_nueva, nombre_completo_anterior):
    cursor.execute("UPDATE Residentes SET nombre_completo = ?, edad = ?, fecha_inscripcion = ? WHERE nombre_completo = ?", (nombre_completo_nuevo, edad_nueva, fecha_nueva, nombre_completo_anterior))
    conn.commit()

def importar_excel_db(ruta_archivo):
    # Leer el archivo Excel y almacenar los datos en un DataFrame
    df = pd.read_excel(ruta_archivo)

    # Ignorar primeras filas
    df = df.iloc[0:]

    # Iterar sobre las filas del DataFrame y ejecutar las consultas INSERT
    for fila in df.itertuples(index=False):
        cursor.execute('INSERT INTO Residentes VALUES (null, ?, ?, ?)', fila)


def exportar_excel_db(ruta_archivo):
    cursor.execute("SELECT nombre_completo, edad, fecha_inscripcion FROM Residentes")
    resultados = cursor.fetchall()
    
    # Crear un DataFrame con los resultados de la consulta
    df = pd.DataFrame(resultados, columns=['Nombre', 'Edad', 'Fecha de Inscripción'])
    
    # Exportar el DataFrame a un archivo de Excel
    df.to_excel(ruta_archivo, index=False)
    
    
def borrar_todo_db():
    cursor.execute("DELETE FROM Residentes;")
    conn.commit()

def cerrar_db():
    conn.close()   



