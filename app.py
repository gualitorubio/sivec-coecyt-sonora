import streamlit as st
import requests
from google import genai
import io
import datetime  # Agregado para Supabase
from supabase import create_client  # Agregado para Supabase
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# ==============================================================================
# CONFIGURACIÓN E IDENTIDAD CORPORATIVA - RUBIO INTELLIGENCE SYSTEMS
# ==============================================================================
st.set_page_config(page_title="SIVEC - Rubio Intelligence Systems", page_icon=" 🔬 ", layout="wide")

# Inicialización de Clientes
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# --- LÓGICA DE SEGURIDAD SUPABASE (INTEGRADA) ---
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
# INTERFAZ Y LÓGICA ORIGINAL (MANTENIDA)
# ==============================================================================
st.title(" 🔬  SIVEC")
st.subheader("Sistema de Inteligencia para la Vanguardia Experimental y Científica")
st.caption("Propiedad de Rubio Intelligence Systems.")
st.markdown("---")
st.sidebar.header(" ⚙️  Panel de Control")

# Tu sidebar original
user_email = st.sidebar.text_input("Correo Institucional (Acceso):")
area_estrategica = st.sidebar.selectbox("Rama del Conocimiento:", [...]) # Manten tu lista original

# ... (Todo tu código original de UI va aquí) ...

termino_busqueda = st.text_input("Palabras clave para la búsqueda científica...")
pregunta_usuario = st.text_area("Pregunta de investigación detallada...")

if st.button(" 🚀  Lanzar Análisis de Vanguardia"):
    if not user_email:
        st.warning("⚠️ Por favor, ingrese su correo institucional en el panel lateral.")
    elif not termino_busqueda or not pregunta_usuario:
        st.warning(" ⚠️  Completa ambos campos para iniciar el escaneo.")
    else:
        # VALIDACIÓN: Si es válido, ejecuta. Si no, muestra tu mensaje exacto.
        if verificar_limite_y_sumar(user_email):
            with st.status(" 🛸  Procesando peticiones en la infraestructura de Rubio Intelligence Systems...", expanded=True) as status:
                ejecutar_sivec(termino_busqueda, pregunta_usuario)
                status.update(label=" ✅  Análisis finalizado", state="complete")
        else:
            st.error("""
            ⚠️ **Congestión en Repositorios Externos**
            
            Debido a una alta demanda simultánea en los servidores globales de literatura científica, no es posible establecer una conexión de datos en este momento. 
            
            El sistema de inteligencia SIVEC se sincronizará automáticamente para nuevos procesamientos a partir de las 12:00 am. Agradecemos su comprensión.
            """)
