#archivo para diagnosticar problemas de importación de langchain_google_genai 
import sys # importar sys para acceder a información del sistema
import importlib # importar importlib para importar módulos dinámicamente 

# Función para imprimir encabezados
def print_header(title):
    print('\n' + '='*10 + ' ' + title + ' ' + '='*10) 

# Imprimir información del entorno
print_header('Python executable')
print(sys.executable)

# imprimir sys.path para ver rutas de búsqueda de módulos
print_header('sys.path')
for p in sys.path:
    print(p)

# imprimir prefijo de instalación de Python para ver dónde está instalado
print_header('where python (from sys)')
print(sys.prefix)

# Intentar importar langchain_google_genai para ver si está disponible
print_header('trying import langchain_google_genai')
try:
    mod = importlib.import_module('langchain_google_genai')
    print('OK import: ', mod.__file__)
except Exception as e:
    print('IMPORT ERROR:', type(e), e)
# Intentar importar ChatGoogleGenerativeAI desde langchain_google_genai
print_header('trying import langchain_google_genai.ChatGoogleGenerativeAI')
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    print('OK class found')
except Exception as e:
    print('IMPORT ERROR:', type(e), e)
# Finalizar diagnóstico
print_header('done')
