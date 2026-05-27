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

# Lógica de Validación de Cuotas (Ajustada a: user_id, consultas, fecha)
def validar_cuota(user_id):
    hoy = datetime.now().strftime("%Y-%m-%d")
    # Buscamos por el ID del usuario
    res = supabase.table("usuarios_sivec").select("*").eq("user_id", user_id).execute()
    
    if not res.data:
        # Insertamos usando tus nombres de columna reales
        supabase.table("usuarios_sivec").insert({"user_id": user_id, "consultas": 1, "fecha": hoy}).execute()
        return True
    
    usuario = res.data[0]
    
    if usuario['fecha'] != hoy:
        # Reseteamos el contador en la columna 'consultas'
        supabase.table("usuarios_sivec").update({"consultas": 1, "fecha": hoy}).eq("user_id", user_id).execute()
        return True
    
    if usuario['consultas'] < 10:
        # Incrementamos el contador en 'consultas'
        supabase.table("usuarios_sivec").update({"consultas": usuario['consultas'] + 1}).eq("user_id", user_id).execute()
        return True
        
    return False

# --- AQUÍ VAN TUS FUNCIONES ORIGINALES (generar_pdf_dictamen, ejecutar_sivec, etc.) ---
# ... [MANTÉN AQUÍ TU CÓDIGO ORIGINAL SIN CAMBIOS] ...

# ==============================================================================
# INTERFAZ DE USUARIO
# ==============================================================================
st.title(" 🔬  SIVEC")
st.subheader("Sistema de Inteligencia para la Vanguardia Experimental y Científica")
st.caption("Propiedad de Rubio Intelligence Systems.")
st.markdown("---")

st.sidebar.header(" ⚙️  Panel de Control")

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

st.markdown(f"###  📑  Módulo Activo: {area_estrategica}")

# Campo para identificar al usuario por su ID
user_id = st.sidebar.text_input("ID de Usuario COECyT:")
termino_busqueda = st.text_input("Palabras clave:")
pregunta_usuario = st.text_area("Pregunta de investigación:")

if st.button(" 🚀  Lanzar Análisis de Vanguardia"):
    if not user_id:
        st.warning("⚠️ Ingresa tu ID de usuario para continuar.")
    elif not termino_busqueda or not pregunta_usuario:
        st.warning(" ⚠️  Completa los campos.")
    elif validar_cuota(user_id):
        with st.status(" 🛸  Procesando...", expanded=True) as status:
            ejecutar_sivec(termino_busqueda, pregunta_usuario)
            status.update(label=" ✅  Análisis finalizado", state="complete")
    else:
        st.error("""⚠️ **Congestión en Repositorios Externos**
        
        Debido a una alta demanda simultánea, el sistema de inteligencia SIVEC se sincronizará automáticamente para nuevos procesamientos a partir de las 12:00 am. Agradecemos su comprensión.""")
