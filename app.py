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
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
except Exception as e:
    st.error(f"Error de inicialización: {e}")
    st.stop()

# ==============================================================================
# LÓGICA DE SEGURIDAD Y LÍMITES
# ==============================================================================
def verificar_limite_y_sumar(user_id):
    hoy = str(datetime.date.today())
    try:
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
    except Exception as e:
        st.error(f"Error de sincronización con base de datos: {e}")
        return False

# ==============================================================================
# INTERFAZ Y MOTOR SIVEC
# ==============================================================================
st.title(" 🔬 SIVEC")
st.subheader("Sistema de Inteligencia para la Vanguardia Experimental y Científica")
st.markdown("---")

st.sidebar.header(" ⚙️ Panel de Control")
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

st.markdown(f"### 📑 Módulo Activo: {rama_cientifica}")
termino_busqueda = st.text_input("Palabras clave:")
pregunta_usuario = st.text_area("Pregunta de investigación:")

if st.button(" 🚀 Lanzar Análisis de Vanguardia"):
    if not user_email:
        st.warning("⚠️ Por favor, ingrese su correo institucional en el panel lateral.")
    elif not termino_busqueda or not pregunta_usuario:
        st.warning(" ⚠️ Completa todos los campos.")
    else:
        # Validación de seguridad
        if verificar_limite_y_sumar(user_email):
            with st.status(" 🛸 Procesando en infraestructura de Rubio Intelligence Systems...", expanded=True) as status:
                try:
                    # Motor de Gemini
                    response = client.models.generate_content(
                        model='gemini-1.5-flash',
                        contents=f"Rama: {rama_cientifica}. Pregunta: {pregunta_usuario}. Palabras clave: {termino_busqueda}"
                    )
                    st.markdown(response.text)
                    status.update(label=" ✅ Análisis finalizado", state="complete")
                except Exception as e:
                    status.update(label=" ❌ Error en el procesamiento de IA", state="error")
                    st.error(f"Detalles del error técnico: {e}")
        else:
            st.error("""
            ⚠️ **Congestión en Repositorios Externos**
            
            Debido a una alta demanda simultánea en los servidores globales de literatura científica, no es posible establecer una conexión de datos en este momento. 
            
            El sistema de inteligencia SIVEC se sincronizará automáticamente para nuevos procesamientos a partir de las 12:00 am. Agradecemos su comprensión.
            """)
