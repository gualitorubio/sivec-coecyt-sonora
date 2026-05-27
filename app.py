import streamlit as st
import requests
from google import genai
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from supabase import create_client
from datetime import datetime

# ==============================================================================
# CONFIGURACIÓN E IDENTIDAD CORPORATIVA - RUBIO INTELLIGENCE SYSTEMS
# ==============================================================================
st.set_page_config(page_title="SIVEC - Rubio Intelligence Systems", page_icon=" 🔬 ", layout="wide")

# Inicialización de Supabase (usando tus Secrets actuales)
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# Lógica de Validación de Cuotas
def validar_cuota(email):
    hoy = datetime.now().strftime("%Y-%m-%d")
    res = supabase.table("usuarios_sivec").select("*").eq("email", email).execute()
    if not res.data:
        supabase.table("usuarios_sivec").insert({"email": email, "peticiones_hoy": 1, "ultima_fecha": hoy}).execute()
        return True
    usuario = res.data[0]
    if usuario['ultima_fecha'] != hoy:
        supabase.table("usuarios_sivec").update({"peticiones_hoy": 1, "ultima_fecha": hoy}).eq("email", email).execute()
        return True
    if usuario['peticiones_hoy'] < 10:
        supabase.table("usuarios_sivec").update({"peticiones_hoy": usuario['peticiones_hoy'] + 1}).eq("email", email).execute()
        return True
    return False

# --- AQUÍ IRÍAN TUS FUNCIONES ORIGINALES (generar_pdf_dictamen, ejecutar_sivec) ---
# ... (Mantén aquí exactamente el código de tus funciones originales) ...

# ==============================================================================
# INTERFAZ DE USUARIO (Orden Corregido para evitar NameError)
# ==============================================================================
st.title(" 🔬  SIVEC")
st.subheader("Sistema de Inteligencia para la Vanguardia Experimental y Científica")
st.caption("Propiedad de Rubio Intelligence Systems.")
st.markdown("---")

st.sidebar.header(" ⚙️  Panel de Control")
# Selección de rama (esto define area_estrategica)
rama_cientifica = st.sidebar.selectbox("Rama del Conocimiento:", [
    " 🧬  Ciencias Médicas y de la Salud", " 🌱  Biología, Agrobiociencias y Química",
    " 🔋  Ingeniería, Tecnología y Nanomateriales", " 🤖  Inteligencia Artificial y Computación Cuántica",
    " 🌍  Ciencias de la Tierra, Astrofísica y Medio Ambiente", " 📊  Matemáticas, Física y Ciencias Exactas",
    " ⚖️  Ciencias Sociales, Economía y Derecho", " 🎨  Humanidades, Filosofía y Estudios de Comportamiento",
    " ✨  Personalizada / Otra Rama Científica"
])

if rama_cientifica == " ✨  Personalizada / Otra Rama Científica":
    rama_personalizada = st.sidebar.text_input("Especifica la disciplina:")
    area_estrategica = rama_personalizada if rama_personalizada else "Disciplina Personalizada"
else:
    area_estrategica = rama_cientifica

# AHORA que area_estrategica existe, podemos renderizar el título
st.markdown(f"###  📑  Módulo Activo: {area_estrategica}")

email_usuario = st.sidebar.text_input("Correo Institucional COECyT:")
termino_busqueda = st.text_input("Palabras clave:")
pregunta_usuario = st.text_area("Pregunta de investigación:")

if st.button(" 🚀  Lanzar Análisis de Vanguardia"):
    if not email_usuario:
        st.warning("⚠️ Ingresa tu correo institucional.")
    elif not termino_busqueda or not pregunta_usuario:
        st.warning(" ⚠️  Completa los campos.")
    elif validar_cuota(email_usuario):
        with st.status(" 🛸  Procesando...", expanded=True) as status:
            ejecutar_sivec(termino_busqueda, pregunta_usuario) # Tu función original
            status.update(label=" ✅  Análisis finalizado", state="complete")
    else:
        st.error("""⚠️ **Congestión en Repositorios Externos**
        Debido a una alta demanda simultánea, el sistema se sincronizará a las 12:00 am.""")
