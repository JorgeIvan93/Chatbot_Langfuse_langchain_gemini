import os 
import json #importar json para formatear la salida
from dotenv import load_dotenv 

#cargar variables de entorno desde el archivo .env
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Intentar listar modelos usando el SDK oficial de google.generativeai
def try_google_generativeai_sdk():
    try:
        import google.generativeai as genai
        print("Using google.generativeai SDK")
        try:
            genai.configure(api_key=API_KEY)
        except Exception:
            # exepciones en variantes antiguas/nuevas
            try:
                genai.init(api_key=API_KEY)
            except Exception:
                pass
        #inentamos listar modelos 
        try:
            models = genai.list_models()
            # lista modelos regresando generador o lista 
            if hasattr(models, "__iter__") and not isinstance(models, (list, tuple, dict, str)):
                print("Models (generator):")
                # ciclo para imprimir cada modelo en formato json
                count = 0
                for m in models:
                    try:
                        print(json.dumps(m, indent=2, default=str))
                    except Exception:
                        print(m)
                    count += 1
                print(f"Total models listed: {count}")
            # si es lista o dict, imprimimos directamente
            else:
                try:
                    print(json.dumps(models, indent=2, default=str))
                except Exception:
                    print(models)
            return True
        except Exception as e:
            print("fallo el llamado de SDK:", e)
            return False
    # importar el SDK muestra error de importación
    except Exception as e:
        print("google.generativeai fallo importacion:", e)
        return False

def try_requests_rest():
    try:
        import requests
    except Exception as e:
        print("requerimiento no instalado:", e)
        return False
    # hacer llamada REST para listar modelos
    url = "https://generativelanguage.googleapis.com/v1beta/models"
    params = {"key": API_KEY} if API_KEY else {}
    # intentamos la llamada REST verificando la respuesta y desplegando el resultado
    try:
        r = requests.get(url, params=params, timeout=15)
        print(f"REST status: {r.status_code}")
        try:
            print(json.dumps(r.json(), indent=2))
        except Exception:
            print(r.text)
        return r.status_code == 200
    except Exception as e:
        print("REST call exception:", e)
        return False
# función principal para ejecutar los intentos de listado de modelos
def main():
    if not API_KEY:
        print("GEMINI_API_KEY no está configurada en el entorno. Añade tu API key en .env o en la variable de entorno GEMINI_API_KEY.")
        return

    print("Intentando SDK google.generativeai...")
    ok = try_google_generativeai_sdk()
    if ok:
        return

    print("Intentando REST fallback con requests...")
    ok = try_requests_rest()
    if ok:
        return

    print("No se pudo listar modelos con los métodos probados. Asegúrate de que la clave clave de API es válida y tiene permisos para acceder a la API de Generative AI.")

if __name__ == '__main__':
    main()
