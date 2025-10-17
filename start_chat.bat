@echo off
REM =================================================================
REM Script de inicio del Chatbot Inteligente
REM
REM Este script configura el entorno y ejecuta el chatbot de forma
REM silenciosa, ocultando mensajes técnicos para una mejor experiencia.
REM =================================================================

REM Configurar variables de entorno para suprimir mensajes de depuración
set PYTHONWARNINGS=ignore
set TF_CPP_MIN_LOG_LEVEL=3

REM Ejecutar el chatbot redirigiendo la salida de error a nul
python main.py 2>nul