import streamlit as st
import google.generativeai as genai
from supabase import create_client
import datetime

# ==============================================================================
# CONFIGURACIÓN
# ==============================================================================
st.set_page_config(page_title="SIVEC - COECyT Sonora", page_icon=" 🔬 ", layout="wide")

# Inicialización
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# ==============================================================================
# LÓGICA DE CONTROL
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
# MOTOR SIVEC
# ==============================================================================
def ejecutar_sivec(termino, pregunta):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(pregunta)
    st.markdown(response.text)

# ==============================================================================
# INTERFAZ
# ==============================================================================
st.title(" 🔬  SIVEC - COECyT Sonora")
st.sidebar.header(" ⚙️  Acceso Institucional")
user_email = st.sidebar.text_input("Correo Institucional (COECyT):")
termino_busqueda = st.text_input("Palabras clave:")
pregunta_usuario = st.text_area("Pregunta de investigación:")

if st.button(" 🚀  Lanzar Análisis de Vanguardia"):
    if not user_email:
        st.warning("⚠️ Ingrese su correo.")
    elif not termino_busqueda or not pregunta_usuario:
        st.warning("⚠️ Complete todos los campos.")
    else:
        if verificar_limite_y_sumar(user_email):
            with st.status(" 🛸  Procesando...", expanded=True) as status:
                ejecutar_sivec(termino_busqueda, pregunta_usuario)
                status.update(label=" ✅  Análisis finalizado", state="complete")
        else:
            st.error("⚠️ Límite de 10 consultas diarias alcanzado.")
