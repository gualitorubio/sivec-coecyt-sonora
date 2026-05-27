import streamlit as st
import requests
import json
import os
import datetime
from google import genai
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# --- CONFIGURACIÓN E IDENTIDAD ---
st.set_page_config(page_title="SIVEC - Rubio Intelligence Systems", page_icon="🔬", layout="wide")

# --- LÓGICA DE CONTROL (Integrada) ---
def verificar_acceso(email):
    # Autorizados (Crear archivo local si no existe)
    if not os.path.exists("usuarios_autorizados.txt"):
        with open("usuarios_autorizados.txt", "w") as f: f.write("admin@rubio.com")
    with open("usuarios_autorizados.txt", "r") as f:
        autorizados = [line.strip() for line in f.readlines()]
    if email not in autorizados: return False, "Usuario no autorizado."

    # Cuota diaria persistente
    archivo_cuotas = "cuotas_sivec.json"
    hoy = datetime.date.today().isoformat()
    if os.path.exists(archivo_cuotas):
        with open(archivo_cuotas, "r") as f: datos = json.load(f)
    else: datos = {}
    if email not in datos or datos[email]["fecha"] != hoy:
        datos[email] = {"fecha": hoy, "consultas": 0}
    if datos[email]["consultas"] >= 10: return False, "Límite de 10 consultas alcanzado."
    
    datos[email]["consultas"] += 1
    with open(archivo_cuotas, "w") as f: json.dump(datos, f)
    return True, "Acceso concedido"

# --- INTERFAZ ---
st.title("🔬 SIVEC")
st.subheader("Sistema de Inteligencia para la Vanguardia Experimental y Científica")
st.caption("Propiedad de Rubio Intelligence Systems.")
st.markdown("---")

st.sidebar.header("⚙️ Panel de Control")
try:
    st.sidebar.image("logo_rubio_is.png", width=250)
except: pass

rama_cientifica = st.sidebar.selectbox("Rama del Conocimiento:", [
    "🧬 Ciencias Médicas y de la Salud", "🌱 Biología, Agrobiociencias y Química",
    "🔋 Ingeniería, Tecnología y Nanomateriales", "🤖 Inteligencia Artificial y Computación Cuántica",
    "🌍 Ciencias de la Tierra, Astrofísica y Medio Ambiente", "📊 Matemáticas, Física y Ciencias Exactas",
    "⚖️ Ciencias Sociales, Economía y Derecho", "🎨 Humanidades, Filosofía y Estudios de Comportamiento",
    "✨ Personalizada / Otra Rama Científica"
])

max_papers = st.sidebar.slider("Lote de Documentos Analíticos:", 1, 3, 2)
user_email = st.text_input("Correo electrónico registrado:")

# --- ENTRADAS ---
termino_busqueda = st.text_input("Palabras clave para la búsqueda científica:")
pregunta_usuario = st.text_area("Pregunta de investigación detallada:")

# --- EJECUCIÓN (SOLO UN BOTÓN) ---
if st.button("🚀 Lanzar Análisis de Vanguardia"):
    if not user_email or not termino_busqueda or not pregunta_usuario:
        st.warning("⚠️ Completa todos los campos.")
    else:
        autorizado, mensaje = verificar_acceso(user_email)
        if not autorizado:
            st.error(f"⚠️ {mensaje}")
        else:
            with st.status("🛸 Procesando peticiones en la infraestructura de Rubio Intelligence Systems...", expanded=True) as status:
                # --- AQUÍ VA TU LÓGICA ORIGINAL EXACTA ---
                # Pega todo el bloque de tu PDF que realiza el 'requests.get' a OpenAlex
                # y la llamada a Gemini, justo aquí.
                st.write("Conectando con repositorios...")
                # ... (Tu código original aquí) ...
                status.update(label="✅ Análisis finalizado", state="complete")
