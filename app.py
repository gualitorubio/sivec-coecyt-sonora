import streamlit as st
from google import genai
import datetime
from supabase import create_client

# ==============================================================================
# CONFIGURACIÓN E IDENTIDAD CORPORATIVA
# ==============================================================================
st.set_page_config(page_title="SIVEC - Rubio Intelligence Systems", page_icon=" 🔬 ", layout="wide")

# Inicialización de clientes
# Asegúrate de que SUPABASE_URL en tus Secrets NO contenga "/rest/v1/"
try:
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
    # Inicialización del cliente de Gemini
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error(f"Error crítico de inicialización: {e}")
    st.stop()

# ==============================================================================
# LÓGICA DE SEGURIDAD Y LÍMITES
# ==============================================================================
def verificar_limite_y_sumar(user_id):
    hoy = str(datetime.date.today())
    try:
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
    " 🧬 Ciencias Médicas y de la Salud", " 🌱 Biología y Agrobiociencias",
    " 🔋 Ingeniería y Nanomateriales", " 🤖 Inteligencia Artificial",
    " 🌍 Ciencias de la Tierra y Astrofísica", " 📊 Ciencias Exactas"
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
        if verificar_limite_y_sumar(user_email):
            with st.status(" 🛸 Procesando en infraestructura de Rubio Intelligence Systems...", expanded=True) as status:
                try:
                    # Prueba simple para verificar si el cliente responde
                    prompt = f"Rama: {rama_cientifica}. Pregunta: {pregunta_usuario}. Palabras clave: {termino_busqueda}"
                    response = client.models.generate_content(
                        model='gemini-1.5-flash',
                        contents=prompt
                    )
                    st.markdown(response.text)
                    status.update(label=" ✅ Análisis finalizado", state="complete")
                except Exception as e:
                    status.update(label=" ❌ Error en IA", state="error")
                    st.error(f"Gemini API Error: {e}")
        else:
            st.error("⚠️ Límite de consultas diario alcanzado o error de sincronización.")
