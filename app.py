import streamlit as st
import google.generativeai as genai
from supabase import create_client
import datetime

# 1. Configuración de clientes
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# 2. Función de control (Supabase)
def verificar_limite_y_sumar(user_id):
    hoy = str(datetime.date.today())
    # Consultar uso actual
    res = supabase.table("uso_sivec").select("consultas").eq("user_id", user_id).eq("fecha", hoy).execute()
    
    if not res.data:
        # Crear usuario nuevo en tabla hoy
        supabase.table("uso_sivec").insert({"user_id": user_id, "fecha": hoy, "consultas": 1}).execute()
        return True
    
    contador = res.data[0]['consultas']
    if contador < 10:
        # Sumar +1
        supabase.table("uso_sivec").update({"consultas": contador + 1}).eq("user_id", user_id).eq("fecha", hoy).execute()
        return True
    return False

# 3. Interfaz y flujo (Aquí pegas tu lógica de SIVEC)
st.title(" 🔬 SIVEC - COECyT Sonora")
user_email = st.text_input("Ingrese su Correo Institucional:")

if st.button("🚀 Lanzar Análisis"):
    if not user_email:
        st.warning("Por favor ingrese su correo.")
    elif verificar_limite_y_sumar(user_email):
        # AQUÍ LLAMAS A TU LÓGICA DE EJECUCIÓN (ejecutar_sivec)
        st.success("Acceso autorizado. Ejecutando análisis...")
        # ... resto de tu código original ...
    else:
        st.error("⚠️ Límite de 10 consultas diarias alcanzado. El sistema se reiniciará a las 12:00 am.")
