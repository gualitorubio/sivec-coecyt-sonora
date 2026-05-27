import streamlit as st
import requests
from google import genai
import io
import json
import os
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# --- LÓGICA DE CONTROL (Persistente) ---
def verificar_acceso(email):
    if not os.path.exists("usuarios_autorizados.txt"):
        with open("usuarios_autorizados.txt", "w") as f: f.write("admin@rubio.com")
    with open("usuarios_autorizados.txt", "r") as f:
        autorizados = [line.strip() for line in f.readlines()]
    if email not in autorizados: return False, "Usuario no autorizado."

    archivo_cuotas = "cuotas_sivec.json"
    hoy = datetime.date.today().isoformat()
    if os.path.exists(archivo_cuotas):
        with open(archivo_cuotas, "r") as f: datos = json.load(f)
    else: datos = {}
    if email not in datos or datos[email]["fecha"] != hoy:
        datos[email] = {"fecha": hoy, "consultas": 0}
    if datos[email]["consultas"] >= 10: return False, "Límite alcanzado."
    datos[email]["consultas"] += 1
    with open(archivo_cuotas, "w") as f: json.dump(datos, f)
    return True, "Ok"

# --- TU CÓDIGO ORIGINAL (CONFIGURACIÓN) ---
st.set_page_config(page_title="SIVEC - Rubio Intelligence Systems", page_icon="🔬", layout="wide")
st.title("🔬 SIVEC")
st.subheader("Sistema de Inteligencia para la Vanguardia Experimental y Científica")
st.sidebar.header("⚙️ Panel de Control")
user_email = st.text_input("Correo electrónico registrado:")

# --- TU LÓGICA DE INTERFAZ ORIGINAL ---
rama_cientifica = st.sidebar.selectbox("Rama del Conocimiento:", ["Ciencias Médicas y de la Salud", "IA", "Otras"])
max_papers = st.sidebar.slider("Lote de Documentos:", 1, 3, 2)
termino_busqueda = st.text_input("Palabras clave:")
pregunta_usuario = st.text_area("Pregunta de investigación:")

# --- EL BOTÓN ORIGINAL (Aquí ejecutamos tu lógica tal cual) ---
if st.button("🚀 Lanzar Análisis de Vanguardia"):
    autorizado, msg = verificar_acceso(user_email)
    if not autorizado:
        st.error(f"⚠️ {msg}")
    elif not termino_busqueda or not pregunta_usuario:
        st.warning("⚠️ Completa los campos.")
    else:
        # AQUÍ ESTÁ EL BLOQUE QUE HACE EL TRABAJO DURO
        with st.status("🛸 Procesando...", expanded=True):
            # PEGA AQUÍ TODO TU BLOQUE ORIGINAL DE REQUESTS.GET A OPENALEX
            # Y LA LLAMADA A GENAI QUE ESTABA EN TU PDF
            st.write("Conectando con repositorios...")
            # ... (Toda tu lógica original va aquí exactamente igual)
            st.success("Dictamen finalizado")
