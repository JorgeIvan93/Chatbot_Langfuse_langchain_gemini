import os
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

def try_google_generativeai_sdk():
    try:
        import google.generativeai as genai
        print("Using google.generativeai SDK")
        try:
            genai.configure(api_key=API_KEY)
        except Exception:
            # older/newer variants
            try:
                genai.init(api_key=API_KEY)
            except Exception:
                pass
        try:
            models = genai.list_models()
            # list_models may return a generator; handle ambos casos
            if hasattr(models, "__iter__") and not isinstance(models, (list, tuple, dict, str)):
                print("Models (generator):")
                count = 0
                for m in models:
                    try:
                        print(json.dumps(m, indent=2, default=str))
                    except Exception:
                        print(m)
                    count += 1
                print(f"Total models listed: {count}")
            else:
                try:
                    print(json.dumps(models, indent=2, default=str))
                except Exception:
                    print(models)
            return True
        except Exception as e:
            print("SDK call failed:", e)
            return False
    except Exception as e:
        print("google.generativeai import failed:", e)
        return False

def try_requests_rest():
    try:
        import requests
    except Exception as e:
        print("requests not installed:", e)
        return False

    url = "https://generativelanguage.googleapis.com/v1beta/models"
    params = {"key": API_KEY} if API_KEY else {}
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
