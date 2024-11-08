import csv
import random
from datetime import datetime, timedelta

# generar dato
def generar_datos_csv(nombre_archivo, num_items=20):
    tipos_registro = ['Ingreso', 'Egreso']
    fecha_actual = datetime.now()
    
    with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo_csv:
        escritor = csv.writer(archivo_csv)
        escritor.writerow(['fecha', 'mesReporte', 'añoReporte', 'tipoRegistro', 'monto'])
        
        for _ in range(num_items):
            # Generar fecha aleatoria
            fecha_aleatoria = fecha_actual - timedelta(days=random.randint(0, 30))
            fecha_formato = fecha_aleatoria.strftime('%d-%m-%Y')
            
            # Generar el resto de datos
            mes_reporte = fecha_aleatoria.month
            año_reporte = fecha_aleatoria.year
            tipo_registro = random.choice(tipos_registro)
            monto = round(random.uniform(100, 5000), 2)
            
            # Insertar fila en el csv
            escritor.writerow([fecha_formato, mes_reporte, año_reporte, tipo_registro, monto])
    
    print(f"Archivo CSV '{nombre_archivo}' generado con éxito.")

# Generar el archivo CSV
nombre_archivo = 'flujo_efectivo.csv'
generar_datos_csv(nombre_archivo)
