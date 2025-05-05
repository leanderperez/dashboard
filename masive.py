import psycopg2
import csv
import os

def cargar_datos_linea_por_linea(nombre_archivo_csv, nombre_tabla, host, nombre_base_datos, usuario, contraseña, codificacion='utf-8'):
    try:
        conexion = psycopg2.connect(
            host=host,
            database=nombre_base_datos,
            user=usuario,
            password=contraseña
        )
        cursor = conexion.cursor()

        with open(nombre_archivo_csv, 'r', encoding=codificacion) as archivo_csv:
            lector_csv = csv.reader(archivo_csv, delimiter=';')
            encabezados = next(lector_csv)  # Leer los encabezados
            for fila in lector_csv:
                nombre, descripcion, unidad_medida = fila
                consulta_insert = f"INSERT INTO {nombre_tabla} (nombre, descripcion, unidad_medida) VALUES (%s, %s, %s)"
                cursor.execute(consulta_insert, (nombre, descripcion, unidad_medida))

        conexion.commit()
        print("Datos cargados correctamente (línea por línea).")

    except (Exception, psycopg2.Error) as error:
        print("Error al cargar datos:", error)
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

# Llama a esta nueva función para probar
cargar_datos_linea_por_linea(
    nombre_archivo_csv='materiales.csv',
    nombre_tabla='app_material',
    host='localhost',
    nombre_base_datos= os.getenv('FORUM_DB_NAME'),
    usuario= os.getenv('FORUM_DB_USER'),
    contraseña= os.getenv('FORUM_DB_PASSWORD')
)