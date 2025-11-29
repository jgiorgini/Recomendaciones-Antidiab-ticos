import streamlit as st
import sys
import os
import pandas as pd

# --- BLOQUE DE IMPORTACIÓN ROBUSTO ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
sys.path.append(parent_dir)

try:
    from src.data.vademecum import obtener_ajuste_renal, FARMACOS
except ImportError:
    try:
        from data.vademecum import obtener_ajuste_renal, FARMACOS
    except ImportError:
        FARMACOS = []
        def obtener_ajuste_renal(id, fge):
            return "DESCONOCIDO", "Error de carga"
        st.error("⚠️ Error crítico: No se encuentra el archivo 'vademecum.py'.")

# Configuración de la página
st.set_page_config(
    page_title="Recomendaciones DBT2",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- FUNCIÓN PARA RESETEAR DATOS (Valores actualizados) ---
def resetear_datos():
    st.session_state["sintomas"] = "No"
    st.session_state["imc"] = 25.0        # Default actualizado
    st.session_state["hba1c_actual"] = 7.0 # Default actualizado
    st.session_state["hba1c_meta"] = 7.0   # Default actualizado
    st.session_state["fge"] = 60
    st.session_state["ic"] = False
    st.session_state["ascvd"] = False
    st.session_state["erd"] = False

# --- TEXTOS Y DATA ---
DISCLAIMER = """
**AVISO IMPORTANTE: HERRAMIENTA DE APOYO CLÍNICO**
1. **Naturaleza:** Esta aplicación es una herramienta de ayuda basada en las Guías Nacionales (2019) y Actualización SEMI (2025). **No sustituye el juicio clínico.**
2. **Responsabilidad:** La prescripción final es responsabilidad exclusiva del profesional médico.
3. **Seguridad:** Verifique siempre alergias, dosis y contraindicaciones.
"""

# --- BARRA LATERAL (INPUTS) ---
with st.sidebar:
    st.title("Perfil del Paciente")
    
    # Botón de Reset
    st.button("🗑️ Limpiar / Resetear", on_click=resetear_datos, type="secondary")
    st.markdown("---")

    st.subheader("1. Clínica y Biometría")
    
    sintomas = st.radio("¿Síntomas de hiperglucemia?", ["No", "Sí (Poliuria, Polidipsia, Pérdida peso)"], index=0, key="sintomas")
    
    # IMC Default: 25.0
    imc = st.number_input("IMC (kg/m²)", min_value=15.0, max_value=60.0, value=25.0, step=0.1, key="imc")
    
    st.subheader("2. Laboratorio")
    
    # HbA1c Default: 7.0
    hba1c_actual = st.number_input("HbA1c Actual (%)", min_value=4.0, max_value=20.0, value=7.0, step=0.1, key="hba1c_actual")
    hba1c_meta = st.number_input("HbA1c Meta (%)", min_value=5.0, max_value=10.0, value=7.0, step=0.1, key="hba1c_meta")
    
    # FGe Default: 60
    fge = st.number_input("Filtrado Glomerular (ml/min)", min_value=0, max_value=150, value=60, step=1, key="fge")
    
    if fge > 60:
        st.success(f"Función Renal Conservada (>60)")
    elif fge >= 30:
        st.warning(f"Insuficiencia Renal Moderada ({fge})")
    else:
        st.error(f"Insuficiencia Renal Severa/Falla ({fge})")

    st.subheader("3. Comorbilidades")
    col1, col2 = st.columns(2)
    with col1:
        tiene_ic = st.checkbox("Insuf. Cardíaca", key="ic")
        tiene_ascvd = st.checkbox("Enf. CV (Infarto/ACV)", key="ascvd")
    with col2:
        tiene_erd = st.checkbox("Enf. Renal Diabética", key="erd")
        tiene_obesidad = True if imc >= 30 else False
        if tiene_obesidad:
            st.caption("✅ Obesidad")

# --- PANTALLA PRINCIPAL CON PESTAÑAS ---

st.title("Recomendaciones de Tratamiento en DBT2")

# Creamos dos pestañas
tab1, tab2 = st.tabs(["🧮 Calculadora Terapéutica", "📖 Vademécum Completo"])

# --- PESTAÑA 1: LA CALCULADORA ---
with tab1:
    st.markdown("---")
    
    recomendaciones = []

    # 1. Regla de Emergencia
    if sintomas.startswith("Sí"):
        st.error("🚨 **ALERTA CLÍNICA:** Paciente sintomático/catabólico.")
        st.info("💉 **INSULINIZACIÓN**
