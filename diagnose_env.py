# archivo para diagnosticar problemas de importación de langchain_google_genai 
import sys  # importar sys para acceder a información del sistema
import importlib  # importar importlib para importar módulos dinámicamente 

# Función para imprimir encabezados
def imprimir_encabezado(titulo):
    print('' + '='*10 + ' ' + titulo + ' ' + '='*10)

# Imprimir información del entorno
imprimir_encabezado('Ejecutable de Python')
print(sys.executable)

# imprimir sys.path para ver rutas de búsqueda de módulos
imprimir_encabezado('sys.path')
for ruta in sys.path:
    print(ruta)

# imprimir prefijo de instalación de Python para ver dónde está instalado
imprimir_encabezado('Ubicación de instalación de Python')
print(sys.prefix)

# Intentar importar langchain_google_genai para ver si está disponible
imprimir_encabezado('Intentando importar langchain_google_genai')
try:
    modulo = importlib.import_module('langchain_google_genai')
    print('Importación exitosa: ', modulo.__file__)
except Exception as error:
    print('ERROR DE IMPORTACIÓN:', type(error), error)

# Intentar importar ChatGoogleGenerativeAI desde langchain_google_genai
imprimir_encabezado('Intentando importar ChatGoogleGenerativeAI')
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    print('Clase encontrada exitosamente')
except Exception as error:
    print('ERROR DE IMPORTACIÓN:', type(error), error)

# Finalizar diagnóstico
imprimir_encabezado('Diagnóstico finalizado')
