import streamlit as st
import requests
import google.generativeai as genai # CORREGIDO: Usando SDK oficial
import io
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from supabase import create_client

# ==============================================================================
# CONFIGURACIÓN E IDENTIDAD CORPORATIVA - RUBIO INTELLIGENCE SYSTEMS
# ==============================================================================
st.set_page_config(page_title="SIVEC - Rubio Intelligence Systems", page_icon=" 🔬 ", layout="wide")

# Inicialización de Clientes (Gemini + Supabase)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# ==============================================================================
# LÓGICA DE SEGURIDAD SUPABASE
# ==============================================================================
def verificar_limite_y_sumar(user_id):
    hoy = str(datetime.date.today())
    res = supabase.table("uso_sivec").select("consultas").eq("user_id", user_id).eq("fecha", hoy).execute()
    
    if not res.data:
        supabase.table("uso_sivec").insert({"user_id": user_id, "fecha": hoy, "consultas": 1}).execute()
        return True
    
    contador = res.data[0]['consultas']
    if contador < 10:
        supabase.table("uso_sivec").update({"consultas": contador + 1}).eq("user_id", user_id).eq("fecha", hoy).execute()
        return True
    return False

# ==============================================================================
# INTERFAZ (Original restaurada)
# ==============================================================================
st.title(" 🔬  SIVEC")
st.subheader("Sistema de Inteligencia para la Vanguardia Experimental y Científica")
st.caption("Propiedad de Rubio Intelligence Systems.")
st.markdown("---")

st.sidebar.header(" ⚙️  Panel de Control")
user_email = st.sidebar.text_input("Correo Institucional (Acceso):")

# Taxonomía Científica Universal
rama_cientifica = st.sidebar.selectbox(
    "Rama del Conocimiento:",
    [
        " 🧬  Ciencias Médicas y de la Salud",
        " 🌱  Biología, Agrobiociencias y Química",
        " 🔋  Ingeniería, Tecnología y Nanomateriales",
        " 🤖  Inteligencia Artificial y Computación Cuántica",
        " 🌍  Ciencias de la Tierra, Astrofísica y Medio Ambiente",
        " 📊  Matemáticas, Física y Ciencias Exactas",
        " ⚖️  Derecho, Ética y Regulación Científica"
    ]
)

st.markdown(f"###  📑  Módulo Activo: {rama_cientifica}")
termino_busqueda = st.text_input("Palabras clave para la búsqueda científica:", placeholder="Ej. Autonomous weapons laws ethics regulations")
pregunta_usuario = st.text_area("Pregunta de investigación detallada:", placeholder="Ej. ¿Qué vacíos legales reportan frente al derecho internacional?")

# ==============================================================================
# EJECUCIÓN (Lógica original + Seguridad)
# ==============================================================================
if st.button(" 🚀  Lanzar Análisis de Vanguardia"):
    if not user_email:
        st.warning("⚠️ Por favor, ingrese su correo institucional en el panel lateral.")
    elif not termino_busqueda or not pregunta_usuario:
        st.warning(" ⚠️  Completa todos los campos para iniciar el escaneo.")
    else:
        # Validación
        if verificar_limite_y_sumar(user_email):
            with st.status(" 🛸  Procesando peticiones en la infraestructura de Rubio Intelligence Systems...", expanded=True) as status:
                # Aquí va tu motor original
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(pregunta_usuario)
                st.markdown(response.text)
                status.update(label=" ✅  Análisis finalizado", state="complete")
        else:
            st.error("⚠️ Límite de 10 consultas diarias alcanzado. Contacte a soporte.")
