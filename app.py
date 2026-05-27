import streamlit as st
import requests
from google import genai
import io
import datetime
from supabase import create_client
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="SIVEC - Rubio Intelligence Systems", page_icon="", layout="wide")

# Inicialización de Supabase
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# --- FUNCIONES DE LÓGICA (Definidas antes de su uso) ---

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

def generar_pdf_dictamen(texto_dictamen, referencias_texto, area_estrategica):
    # (Mantiene tu lógica original de PDF)
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    # ... resto de la construcción del PDF igual a tu PDF original ...
    return buffer.getvalue()

def ejecutar_sivec(termino, pregunta, max_papers, area_estrategica):
    # Aquí va tu lógica original de extracción y IA intacta
    URL_API = "https://api.openalex.org/works"
    config_busqueda = {'search': termino, 'filter': 'is_oa:true', 'per_page': 10, 'sort': 'cited_by_count:desc'}
    st.write(" Escaneando literatura global y bases de datos indexadas...")
    # ... (Asegúrate de copiar aquí el bloque de requests y Gemini tal cual estaba en tu PDF original)
    st.success(" Análisis finalizado")

# --- INTERFAZ (Ejecutada al final) ---

st.title(" SIVEC")
st.subheader("Sistema de Inteligencia para la Vanguardia Experimental y Científica")
st.caption("Propiedad de Rubio Intelligence Systems.")
st.sidebar.header(" Panel de Control")
try:
    st.sidebar.image("logo_rubio_is.png", width=250)
except: pass

rama_cientifica = st.sidebar.selectbox("Rama del Conocimiento:", [
    "🏥 Ciencias Médicas y de la Salud", "🌱 Biología, Agrobiociencias y Química",
    "⚙️ Ingeniería, Tecnología y Nanomateriales", "🤖 Inteligencia Artificial y Computación Cuántica",
    "🌍 Ciencias de la Tierra, Astrofísica y Medio Ambiente", "📐 Matemáticas, Física y Ciencias Exactas",
    "⚖️ Ciencias Sociales, Economía y Derecho", "🧠 Humanidades, Filosofía y Estudios de Comportamiento",
    "✨ Personalizada / Otra Rama Científica"
])
max_papers = st.sidebar.slider("Lote de Documentos Analíticos:", min_value=1, max_value=3, value=2)

user_email = st.text_input("Correo electrónico registrado:")
termino_busqueda = st.text_input("Palabras clave para la búsqueda científica:")
pregunta_usuario = st.text_area("Pregunta de investigación detallada:")

if st.button(" Lanzar Análisis de Vanguardia"):
    if not user_email:
        st.warning("⚠️ Por favor, ingresa tu correo electrónico registrado.")
    elif not termino_busqueda or not pregunta_usuario:
        st.warning("! Completa todos los campos.")
    else:
        if validar_usuario_y_cuota(user_email):
            with st.status(" Procesando...", expanded=True) as status:
                ejecutar_sivec(termino_busqueda, pregunta_usuario, max_papers, rama_cientifica)
                status.update(label=" Análisis finalizado", state="complete")
        else:
            st.error("⚠️ **Congestión en Repositorios Externos**: El sistema de inteligencia SIVEC se sincronizará automáticamente para nuevos procesamientos a partir de las 12:00 am.")
