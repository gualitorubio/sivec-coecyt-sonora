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

# --- CAPA DE SEGURIDAD (No toca tu lógica, solo la protege) ---
def verificar_cuota(email):
    archivo_cuotas = "cuotas_sivec.json"
    hoy = datetime.date.today().isoformat()
    if os.path.exists(archivo_cuotas):
        with open(archivo_cuotas, "r") as f: datos = json.load(f)
    else: datos = {}
    if email not in datos or datos[email]["fecha"] != hoy:
        datos[email] = {"fecha": hoy, "consultas": 0}
    if datos[email]["consultas"] >= 10: return False
    datos[email]["consultas"] += 1
    with open(archivo_cuotas, "w") as f: json.dump(datos, f)
    return True

# --- TU CÓDIGO ORIGINAL SIN MODIFICAR ---
st.set_page_config(page_title="SIVEC - Rubio Intelligence Systems", page_icon="🔬", layout="wide")

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

# NUEVA ENTRADA (Obligatoria para el conteo)
user_email = st.text_input("Correo electrónico para control de acceso:")

st.markdown(f"### 📑 Módulo Activo: {rama_cientifica}")
termino_busqueda = st.text_input("Palabras clave:", placeholder="Ej. Autonomous weapons laws")
pregunta_usuario = st.text_area("Pregunta de investigación detallada:", placeholder="Ej. ¿Qué vacíos legales existen?")

# --- AQUÍ PROTEGEMOS EL BOTÓN ---
if st.button("🚀 Lanzar Análisis de Vanguardia"):
    if not user_email:
        st.warning("⚠️ Debes ingresar un correo para iniciar.")
    elif not termino_busqueda or not pregunta_usuario:
        st.warning("⚠️ Completa todos los campos.")
    elif verificar_cuota(user_email):
        # A PARTIR DE AQUÍ VA TODO TU CÓDIGO ORIGINAL DEL PDF
        # Pega aquí exactamente tu código (requests, genai, reportlab...)
        with st.status("🛸 Procesando peticiones en la infraestructura de Rubio Intelligence Systems...", expanded=True):
            st.write("Conectando con repositorios...")
            # TU LÓGICA ORIGINAL AQUÍ
            st.success("✅ Análisis finalizado")
    else:
        st.error("⚠️ Límite de 10 consultas diarias alcanzado. Intenta mañana.")
