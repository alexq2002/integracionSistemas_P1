import csv
import re
from pymongo import MongoClient, errors

# Configuración de la conexión a MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['finanzas']
coleccion = db['flujos_efectivo']

# Crear índice único en la colección para evitar duplicados
coleccion.create_index([("fecha", 1), ("tipoRegistro", 1), ("monto", 1)], unique=True)

# Expresiones regulares para validación
regex_fecha = re.compile(r'^\d{2}-\d{2}-\d{4}$')
tipos_validos = ['Ingreso', 'Egreso']

def validar_fila(fila):
    # Validar formato de la fecha
    if not regex_fecha.match(fila['fecha']):
        return False, "Fecha inválida"
    
    # Validar mes y año
    try:
        mes = int(fila['mesReporte'])
        año = int(fila['añoReporte'])
        if mes < 1 or mes > 12 or año < 2000:
            return False, "Mes o año inválido"
    except ValueError:
        return False, "Mes o año no numérico"
    
    # Validar tipo de registro
    if fila['tipoRegistro'] not in tipos_validos:
        return False, "Tipo de registro inválido"
    
    # Validar monto
    try:
        fila['monto'] = float(fila['monto'])
        if fila['monto'] < 0:
            return False, "Monto negativo"
    except ValueError:
        return False, "Monto no numérico"
    
    return True, ""

def importar_csv_a_mongodb(nombre_archivo):
    registros_importados = 0
    registros_ignorados = 0
    errores = []

    with open(nombre_archivo, mode='r', encoding='utf-8') as archivo_csv:
        lector = csv.DictReader(archivo_csv)
        
        for fila in lector:
            # Validar la fila antes de la importación
            es_valido, error = validar_fila(fila)
            if not es_valido:
                errores.append(f"Error en fila {fila}: {error}")
                registros_ignorados += 1
                continue
            
            # Intentar insertar el registro en MongoDB
            try:
                coleccion.insert_one(fila)
                registros_importados += 1
            except errors.DuplicateKeyError:
                registros_ignorados += 1
                errores.append(f"Registro duplicado ignorado: {fila}")
            except Exception as e:
                errores.append(f"Error al insertar {fila}: {str(e)}")
                registros_ignorados += 1

    # Mostrar resumen
    print(f"Importación completada: {registros_importados} registros importados.")
    print(f"Registros ignorados: {registros_ignorados}")
    
    # Registrar errores en un archivo log
    if errores:
        with open("errores_importacion.log", mode='w', encoding='utf-8') as log_file:
            for error in errores:
                log_file.write(error + "\n")
        print("Errores registrados en 'errores_importacion.log'.")

# Ejecutar la importación
nombre_archivo = 'flujo_efectivo.csv'
importar_csv_a_mongodb(nombre_archivo)
