import streamlit as st
import requests
from google import genai
import io
import datetime
from supabase import create_client

# ==============================================================================
# CONFIGURACIÓN E IDENTIDAD CORPORATIVA - RUBIO INTELLIGENCE SYSTEMS
# ==============================================================================
st.set_page_config(page_title="SIVEC - Rubio Intelligence Systems", page_icon=" 🔬 ", layout="wide")

# Inicialización de Clientes
# Nota: Asegúrate de tener los secretos GEMINI_API_KEY, SUPABASE_URL y SUPABASE_KEY configurados en Streamlit
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# ==============================================================================
# LÓGICA DE SEGURIDAD Y LÍMITES
# ==============================================================================
def verificar_limite_y_sumar(user_id):
    hoy = str(datetime.date.today())
    # Consulta a Supabase
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
    " 🧬  Ciencias Médicas y de la Salud", " 🌱  Biología y Agrobiociencias",
    " 🔋  Ingeniería y Nanomateriales", " 🤖  Inteligencia Artificial",
    " 🌍  Ciencias de la Tierra y Astrofísica", " 📊  Ciencias Exactas"
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
        # Validación de seguridad
        if verificar_limite_y_sumar(user_email):
            with st.status(" 🛸  Procesando en infraestructura de Rubio Intelligence Systems...", expanded=True) as status:
                # Motor de Gemini (google-genai)
                response = client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=pregunta_usuario
                )
                st.markdown(response.text)
                status.update(label=" ✅  Análisis finalizado", state="complete")
        else:
            # MENSAJE DE BLOQUEO SOLICITADO
            st.error("""
            ⚠️ **Congestión en Repositorios Externos**
            
            Debido a una alta demanda simultánea en los servidores globales de literatura científica, no es posible establecer una conexión de datos en este momento. 
            
            El sistema de inteligencia SIVEC se sincronizará automáticamente para nuevos procesamientos a partir de las 12:00 am. Agradecemos su comprensión.
            """)
