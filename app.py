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

# Inicialización de Supabase
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# Lógica de Validación de Cuotas
def validar_cuota(user_id):
    hoy = datetime.now().strftime("%Y-%m-%d")
    # Consulta a tu tabla 'usuarios_sivec' con tus columnas 'user_id', 'consultas', 'fecha'
    res = supabase.table("usuarios_sivec").select("*").eq("user_id", user_id).execute()
    
    if not res.data:
        supabase.table("usuarios_sivec").insert({"user_id": user_id, "consultas": 1, "fecha": hoy}).execute()
        return True
    
    usuario = res.data[0]
    
    if usuario['fecha'] != hoy:
        supabase.table("usuarios_sivec").update({"consultas": 1, "fecha": hoy}).eq("user_id", user_id).execute()
        return True
    
    if usuario['consultas'] < 10:
        supabase.table("usuarios_sivec").update({"consultas": usuario['consultas'] + 1}).eq("user_id", user_id).execute()
        return True
        
    return False

# ==============================================================================
# AQUÍ VA TU INTERFAZ ORIGINAL (MANTENIDA COMPLETAMENTE)
# ==============================================================================
st.title(" 🔬  SIVEC")
st.subheader("Sistema de Inteligencia para la Vanguardia Experimental y Científica")
st.caption("Propiedad de Rubio Intelligence Systems.")
st.markdown("---")

st.sidebar.header(" ⚙️  Panel de Control")
try:
    st.sidebar.image("logo_rubio_is.png", width=250)
except Exception:
    pass

# Taxonomía Científica Universal
rama_cientifica = st.sidebar.selectbox(
    "Rama del Conocimiento:",
    [
        " 🧬  Ciencias Médicas y de la Salud", " 🌱  Biología, Agrobiociencias y Química",
        " 🔋  Ingeniería, Tecnología y Nanomateriales", " 🤖  Inteligencia Artificial y Computación Cuántica",
        " 🌍  Ciencias de la Tierra, Astrofísica y Medio Ambiente", " 📊  Matemáticas, Física y Ciencias Exactas",
        " ⚖️  Ciencias Sociales, Economía y Derecho", " 🎨  Humanidades, Filosofía y Estudios de Comportamiento",
        " ✨  Personalizada / Otra Rama Científica"
    ]
)

if rama_cientifica == " ✨  Personalizada / Otra Rama Científica":
    rama_personalizada = st.sidebar.text_input("Especifica la disciplina:")
    area_estrategica = rama_personalizada if rama_personalizada else "Disciplina Personalizada"
else:
    area_estrategica = rama_cientifica

# --- INTEGRACIÓN DE ID PARA SUPABASE ---
user_id = st.sidebar.text_input("ID de Usuario COECyT:")

st.markdown(f"###  📑  Módulo Activo: {area_estrategica}")
termino_busqueda = st.text_input("Palabras clave para la búsqueda científica:", placeholder="Ej. Autonomous weapons laws ethics regulations")
pregunta_usuario = st.text_area("Pregunta de investigación detallada:", placeholder="Ej. ¿Qué vacíos legales reportan frente al derecho internacional?")

# --- LÓGICA DEL BOTÓN (MANTENIENDO TU ESTRUCTURA ORIGINAL) ---
if st.button(" 🚀  Lanzar Análisis de Vanguardia"):
    if not user_id:
        st.warning("⚠️ Por favor, ingresa tu ID de usuario.")
    elif not termino_busqueda or not pregunta_usuario:
        st.warning(" ⚠️  Completa ambos campos para iniciar el escaneo.")
    elif validar_cuota(user_id):
        with st.status(" 🛸  Procesando peticiones en la infraestructura de Rubio Intelligence Systems...", expanded=True) as status:
            # Aquí va tu función original de ejecución
            ejecutar_sivec(termino_busqueda, pregunta_usuario)
            status.update(label=" ✅  Análisis finalizado", state="complete")
    else:
        st.error("""
            ⚠️ **Congestión en Repositorios Externos**
            
            Debido a una alta demanda simultánea en los servidores globales de literatura científica, no es posible establecer una conexión de datos en este momento. 
            
            El sistema de inteligencia SIVEC se sincronizará automáticamente para nuevos procesamientos a partir de las 12:00 am. Agradecemos su comprensión.
            """)
