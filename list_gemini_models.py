from config import config  # Importación de configuración centralizada
import json  # importar json para formatear la salida


API_KEY = config.clave_api_gemini  # Reemplazado por configuración centralizada

# Intentar listar modelos usando el SDK oficial de google.generativeai
def try_google_generativeai_sdk():
    try:
        import google.generativeai as genai
        print("Usando SDK google.generativeai")
        try:
            genai.configure(api_key=config.clave_api_gemini)
        except Exception:
            # excepciones en variantes antiguas/nuevas
            try:
                genai.init(api_key=config.clave_api_gemini)
            except Exception:
                pass
        # Intentamos listar modelos
        try:
            models = genai.list_models()
            # lista modelos regresando generador o lista
            if hasattr(models, "__iter__") and not isinstance(models, (list, tuple, dict, str)):
                print("Modelos (generador):")
                count = 0
                for m in models:
                    try:
                        print(json.dumps(m, indent=2, default=str))
                    except Exception:
                        print(m)
                    count += 1
                print(f"Total de modelos listados: {count}")
            else:
                try:
                    print(json.dumps(models, indent=2, default=str))
                except Exception:
                    print(models)
            return True
        except Exception as e:
            print("Falló el llamado del SDK:", e)
            return False
    except Exception as e:
        print("Falló la importación de google.generativeai:", e)
        return False

# Intentar listar modelos usando REST con requests
def try_requests_rest():
    try:
        import requests
    except Exception as e:
        print("requests no está instalado:", e)
        return False

    url = "https://generativelanguage.googleapis.com/v1beta/models"
    params = {"key": API_KEY} if API_KEY else {}

    try:
        r = requests.get(url, params=params, timeout=15)
        print(f"Estado REST: {r.status_code}")
        try:
            print(json.dumps(r.json(), indent=2))
        except Exception:
            print(r.text)
        return r.status_code == 200
    except Exception as e:
        print("Excepción en llamada REST:", e)
        return False

# Función principal para ejecutar los intentos de listado de modelos
def main():
    if not config.clave_api_gemini:
        print("GEMINI_API_KEY no está configurada. Añade tu clave en el archivo .env o como variable de entorno.")
        return

    print("Intentando SDK google.generativeai...")
    ok = try_google_generativeai_sdk()
    if ok:
        return

    print("Intentando REST como alternativa...")
    ok = try_requests_rest()
    if ok:
        return

    print("No se pudo listar modelos. Verifica que la clave de API sea válida y tenga permisos para acceder a la API de Generative AI.")

if __name__ == '__main__':
    main()
