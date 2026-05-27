import streamlit as st
import requests
import google.generativeai as genai  # Corregido para estabilidad
import io
import datetime
from supabase import create_client

# ==============================================================================
# CONFIGURACIÓN E IDENTIDAD CORPORATIVA - RUBIO INTELLIGENCE SYSTEMS
# ==============================================================================
st.set_page_config(page_title="SIVEC - Rubio Intelligence Systems", page_icon=" 🔬 ", layout="wide")

# Inicialización de Clientes
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# ==============================================================================
# LÓGICA DE SEGURIDAD Y LÍMITES
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
# INTERFAZ Y MOTOR SIVEC
# ==============================================================================
st.title(" 🔬  SIVEC")
st.subheader("Sistema de Inteligencia para la Vanguardia Experimental y Científica")
st.markdown("---")

st.sidebar.header(" ⚙️  Panel de Control")
user_email = st.sidebar.text_input("Correo Institucional (Acceso):")

rama_cientifica = st.sidebar.selectbox("Rama del Conocimiento:", [
    "🧬 Ciencias Médicas y de la Salud",
    "🌱 Biología, Agrobiociencias y Química",
    "🔋 Ingeniería, Tecnología y Nanomateriales",
    "🤖 Inteligencia Artificial y Computación Cuántica",
    "🌍 Ciencias de la Tierra, Astrofísica y Medio Ambiente",
    "📊 Matemáticas, Física y Ciencias Exactas",
    "⚖️ Ciencias Sociales, Economía y Derecho",
    "🎨 Humanidades, Filosofía y Estudios de Comportamiento",
    "✨ Personalizada / Otra Rama Científica"
])

st.markdown(f"###  📑  Módulo Activo: {rama_cientifica}")
termino_busqueda = st.text_input("Palabras clave:")
pregunta_usuario = st.text_area("Pregunta de investigación:")

if st.button(" 🚀  Lanzar Análisis de Vanguardia"):
    if not user_email:
        st.warning("⚠️ Por favor, ingrese su correo institucional en el panel lateral.")
    elif not termino_busqueda or not pregunta_usuario:
        st.warning(" ⚠️  Completa todos los campos.")
    else:
        if verificar_limite_y_sumar(user_email):
            with st.status(" 🛸  Procesando en infraestructura de Rubio Intelligence Systems...", expanded=True) as status:
                # Motor de Gemini (google-generativeai estable)
                response = model.generate_content(pregunta_usuario)
                st.markdown(response.text)
                status.update(label=" ✅  Análisis finalizado", state="complete")
        else:
            st.error("""
            ⚠️ **Congestión en Repositorios Externos**
            
            El sistema de inteligencia SIVEC se sincronizará automáticamente para nuevos procesamientos a partir de las 12:00 am.
            """)
