import streamlit as st
import google.generativeai as genai
import io
import datetime
from supabase import create_client
from reportlab.pdfgen import canvas
#
======================================================================
========
# CONFIGURACIÓN E IDENTIDAD CORPORATIVA
#
======================================================================
========
st.set_page_config(page_title="SIVEC - Rubio Intelligence Systems",
page_icon=" 🔬 ", layout="wide")
# Inicialización
try:
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')
supabase = create_client(st.secrets["SUPABASE_URL"],
st.secrets["SUPABASE_KEY"])
except Exception as e:

st.error(f"Error de inicialización: {e}")
st.stop()
# Lógica de Seguridad
def verificar_limite_y_sumar(user_id):
hoy = str(datetime.date.today())
try:
res =

supabase.table("uso_sivec").select("consultas").eq("user_id",
user_id).eq("fecha", hoy).execute()

if not res.data:
supabase.table("uso_sivec").insert({"user_id": user_id,

"fecha": hoy, "consultas": 1}).execute()

return True
contador = res.data[0]['consultas']
if contador < 10:
supabase.table("uso_sivec").update({"consultas": contador

+ 1}).eq("user_id", user_id).eq("fecha", hoy).execute()

return True
return False
except Exception as e:
st.error(f"Error de base de datos: {e}")
return False

# Interfaz
st.title(" 🔬 SIVEC")
st.subheader("Sistema de Inteligencia para la Vanguardia Experimental
y Científica")
st.markdown("---")
st.sidebar.header(" ⚙️ Panel de Control")
user_email = st.sidebar.text_input("Correo Institucional (Acceso):")
rama_cientifica = st.sidebar.selectbox("Rama del Conocimiento:", [
"🧬 Ciencias Médicas y de la Salud", "🌱 Biología, Agrobiociencias
y Química",
"🔋 Ingeniería, Tecnología y Nanomateriales", "🤖 Inteligencia
Artificial y Computación Cuántica",
"🌍 Ciencias de la Tierra, Astrofísica y Medio Ambiente", "📊
Matemáticas, Física y Ciencias Exactas"
])
termino_busqueda = st.text_input("Palabras clave:")
pregunta_usuario = st.text_area("Pregunta de investigación:")
if st.button(" 🚀 Lanzar Análisis de Vanguardia"):
if verificar_limite_y_sumar(user_email):
with st.status(" 🛸 Procesando...", expanded=True) as status:

try:
response = model.generate_content(f"Rama:

{rama_cientifica}. Pregunta: {pregunta_usuario}")
st.markdown(response.text)
status.update(label=" ✅ Análisis finalizado",

state="complete")

except Exception as e:
status.update(label=" ❌ Error de IA", state="error")
st.error(f"Detalle técnico: {e}")

else:
st.error("⚠️ Límite diario alcanzado o error de

autenticación.")
