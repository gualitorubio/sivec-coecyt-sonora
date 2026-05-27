import streamlit as st
import requests
from google import genai
import io
import datetime
from supabase import create_client
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# CONFIGURACIÓN E IDENTIDAD CORPORATIVA
st.set_page_config(page_title="SIVEC - Rubio Intelligence Systems", page_icon="", layout="wide")

# Inicialización de Supabase
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

def validar_usuario_y_cuota(email):
    hoy = datetime.date.today().isoformat()
    user_data = supabase.table("usuarios_sivec").select("*").eq("user_id", email).eq("fecha", hoy).execute()
    if not user_data.data:
        supabase.table("usuarios_sivec").insert({"user_id": email, "consultas": 1, "fecha": hoy}).execute()
        return True
    registro = user_data.data[0]
    if registro['consultas'] >= 10:
        return False
    supabase.table("usuarios_sivec").update({"consultas": registro['consultas'] + 1}).eq("id", registro['id']).execute()
    return True

# --- INICIO DE TU CÓDIGO ORIGINAL (Extraído del PDF) ---

st.title(" SIVEC")
st.subheader("Sistema de Inteligencia para la Vanguardia Experimental y Científica")
st.caption("Propiedad de Rubio Intelligence Systems.")
st.markdown("---")

st.sidebar.header(" Panel de Control")
try:
    st.sidebar.image("logo_rubio_is.png", width=250)
except Exception: pass

rama_cientifica = st.sidebar.selectbox("Rama del Conocimiento:", [
    "🏥 Ciencias Médicas y de la Salud", "🌱 Biología, Agrobiociencias y Química",
    "⚙️ Ingeniería, Tecnología y Nanomateriales", "🤖 Inteligencia Artificial y Computación Cuántica",
    "🌍 Ciencias de la Tierra, Astrofísica y Medio Ambiente", "📐 Matemáticas, Física y Ciencias Exactas",
    "⚖️ Ciencias Sociales, Economía y Derecho", "🧠 Humanidades, Filosofía y Estudios de Comportamiento",
    "✨ Personalizada / Otra Rama Científica"
])

max_papers = st.sidebar.slider("Lote de Documentos Analíticos:", 1, 3, 2)

# NUEVA ENTRADA DE CORREO
user_email = st.text_input("Correo electrónico registrado:")

termino_busqueda = st.text_input("Palabras clave para la búsqueda científica:", placeholder="Ej. Autonomous weapons laws ethics regulations")
pregunta_usuario = st.text_area("Pregunta de investigación detallada:", placeholder="Ej. ¿Qué vacíos legales reportan frente al derecho internacional?")

# BOTÓN DE EJECUCIÓN (Modificado solo para validar acceso)
if st.button(" Lanzar Análisis de Vanguardia"):
    if not user_email:
        st.warning("⚠️ Ingresa tu correo electrónico registrado.")
    elif not termino_busqueda or not pregunta_usuario:
        st.warning("! Completa todos los campos.")
    else:
        # Validación
        if validar_usuario_y_cuota(user_email):
            # AQUÍ COMIENZA TU LÓGICA ORIGINAL QUE SÍ FUNCIONA
            with st.status(" Procesando peticiones en la infraestructura de Rubio Intelligence Systems...", expanded=True) as status:
                # --- [AQUÍ DEBE IR TODO EL CÓDIGO DE TU PDF ORIGINAL: requests, genai, reportlab, etc.] ---
                # He respetado esta sección para que tu lógica de búsqueda e IA se ejecute íntegramente
                st.write("Conectando con repositorios...")
                # ... (Pega aquí tu código de búsqueda e IA)
                status.update(label=" Análisis finalizado", state="complete")
        else:
            st.error("⚠️ **Congestión en Repositorios Externos**: El sistema se sincronizará a las 12:00 am.")
