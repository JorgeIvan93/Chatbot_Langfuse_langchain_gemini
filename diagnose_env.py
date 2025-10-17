import sys
import importlib

def print_header(title):
    print('\n' + '='*10 + ' ' + title + ' ' + '='*10)

print_header('Python executable')
print(sys.executable)

print_header('sys.path')
for p in sys.path:
    print(p)

print_header('where python (from sys)')
print(sys.prefix)

print_header('trying import langchain_google_genai')
try:
    mod = importlib.import_module('langchain_google_genai')
    print('OK import: ', mod.__file__)
except Exception as e:
    print('IMPORT ERROR:', type(e), e)

print_header('trying import langchain_google_genai.ChatGoogleGenerativeAI')
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    print('OK class found')
except Exception as e:
    print('IMPORT ERROR:', type(e), e)

print_header('done')
