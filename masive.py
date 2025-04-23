import psycopg2
import csv

def cargar_datos_csv_a_postgres(nombre_archivo_csv, nombre_tabla, host, nombre_base_datos, usuario, contraseña):
    """
    Carga datos desde un archivo CSV a una tabla de PostgreSQL.

    Args:
        nombre_archivo_csv (str): Ruta al archivo CSV.
        nombre_tabla (str): Nombre de la tabla en PostgreSQL.
        host (str): Host de la base de datos.
        nombre_base_datos (str): Nombre de la base de datos.
        usuario (str): Nombre de usuario de la base de datos.
        contraseña (str): Contraseña de la base de datos.
    """
    try:
        # Conexión a la base de datos PostgreSQL
        conexion = psycopg2.connect(
            host=host,
            database=nombre_base_datos,
            user=usuario,
            password=contraseña
        )
        cursor = conexion.cursor()

        # Abrir el archivo CSV y leer los datos
        with open(nombre_archivo_csv, 'r') as archivo_csv:
            lector_csv = csv.reader(archivo_csv, delimiter=';')
            encabezados = next(lector_csv)  # Leer la primera fila (encabezados)

            # Construir la consulta SQL para la inserción masiva
            consulta_sql = f"COPY {nombre_tabla} FROM stdin WITH (FORMAT CSV, HEADER TRUE)"

            # Usar COPY para insertar los datos de manera eficiente
            cursor.copy_expert(consulta_sql, archivo_csv)

        # Confirmar la transacción
        conexion.commit()
        print("Datos cargados correctamente.")

    except (Exception, psycopg2.Error) as error:
        print("Error al cargar datos:", error)
    finally:
        # Cerrar el cursor y la conexión
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

# Ejemplo de uso
cargar_datos_csv_a_postgres(
    nombre_archivo_csv='materiales.csv',
    nombre_tabla='app_material',
    host='localhost',
    nombre_base_datos='forum',
    usuario='leander',
    contraseña='Forum.2024'
)