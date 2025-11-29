import streamlit as st
from datetime import datetime

# Configuración de la página (Debe ser la primera línea de Streamlit)
st.set_page_config(
    page_title="Día-D: Asistente Diabetes",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- TEXTOS Y DATA ---
DISCLAIMER = """
**AVISO IMPORTANTE: HERRAMIENTA DE APOYO CLÍNICO**
1. **Naturaleza:** Esta aplicación es una herramienta de ayuda basada en las Guías Nacionales (2019) y Actualización SEMI (2025). **No sustituye el juicio clínico.**
2. **Responsabilidad:** La prescripción final es responsabilidad exclusiva del profesional médico.
3. **Seguridad:** Verifique siempre alergias, dosis y contraindicaciones.
"""

# --- BARRA LATERAL (INPUTS) ---
with st.sidebar:
    # Puedes cambiar la URL por un logo local si prefieres
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063176.png", width=50) 
    st.title("Perfil del Paciente")
    
    st.subheader("1. Clínica y Biometría")
    sintomas = st.radio("¿Síntomas de hiperglucemia?", ["No", "Sí (Poliuria, Polidipsia, Pérdida peso)"], index=0)
    imc = st.number_input("IMC (kg/m²)", min_value=15.0, max_value=60.0, value=28.0, step=0.1)
    
    st.subheader("2. Laboratorio")
    hba1c_actual = st.number_input("HbA1c Actual (%)", min_value=4.0, max_value=20.0, value=8.5, step=0.1)
    hba1c_meta = st.number_input("HbA1c Meta (%)", min_value=5.0, max_value=10.0, value=7.0, step=0.1)
    
    # Input de FGe con cambio de color dinámico
    fge = st.number_input("Filtrado Glomerular (ml/min)", min_value=0, max_value=150, value=60)
    if fge > 60:
        st.success(f"Función Renal Conservada (>60)")
    elif fge >= 30:
        st.warning(f"Insuficiencia Renal Moderada ({fge})")
    else:
        st.error(f"Insuficiencia Renal Severa/Falla ({fge})")

    st.subheader("3. Comorbilidades (Drivers)")
    col1, col2 = st.columns(2)
    with col1:
        tiene_ic = st.checkbox("Insuf. Cardíaca")
        tiene_ascvd = st.checkbox("Enf. CV (Infarto/ACV)")
    with col2:
        tiene_erd = st.checkbox("Enf. Renal Diabética")
        tiene_obesidad = True if imc >= 30 else False
        st.write(f"Obesidad: {'Sí' if tiene_obesidad else 'No'}")

# --- PANTALLA PRINCIPAL ---

st.title("Día-D: Recomendación Terapéutica")
st.markdown("---")

# LÓGICA RÁPIDA (PROTOTIPO)
recomendaciones = []
alertas = []

# 1. Regla de Emergencia
if sintomas.startswith("Sí"):
    st.error("🚨 **ALERTA CLÍNICA:** Paciente sintomático/catabólico.")
    st.markdown("### Recomendación Prioritaria:")
    st.info("💉 **INSULINIZACIÓN** (Basal o Esquema intensivo según criterio) +/- Metformina.")
    st.stop() # Detiene el resto del algoritmo

# 2. Regla de Comorbilidades
col_izq, col_der = st.columns([2, 1])

with col_izq:
    st.subheader("💊 Esquema Sugerido")
    
    # Driver Cardiorrenal
    if tiene_ic:
        st.success("💙 **Prioridad Insuficiencia Cardíaca:** iSGLT2 (Empagliflozina / Dapagliflozina)")
        recomendaciones.append("iSGLT2")
        st.caption("Evitar: Pioglitazona, Saxagliptina.")
        
    elif tiene_erd:
        st.success("🧡 **Prioridad Renal:** iSGLT2 (Nefroprotección)")
        recomendaciones.append("iSGLT2")
        if fge < 30:
            st.warning("⚠️ Si FGe < 30, considerar iDPP4 o aGLP1 según tolerancia.")

    elif tiene_ascvd:
        st.success("❤️ **Prioridad Cardiovascular:** aGLP1 o iSGLT2")
        recomendaciones.append("aGLP1")
        
    elif tiene_obesidad:
        st.info("⚖️ **Prioridad Peso:** aGLP1 (Semaglutida/Tirzepatida)")
        recomendaciones.append("aGLP1")

    # Driver Glucémico (Si no hay recomendaciones previas fuertes o falta potencia)
    gap = hba1c_actual - hba1c_meta
    if not recomendaciones:
        if gap < 1.5:
            st.primary("💊 **Monoterapia:** Metformina + Estilo de vida")
        else:
            st.primary("💊 **Terapia Dual:** Metformina + iSGLT2 / iDPP4")

    # 3. Filtros de Seguridad Renal
    st.markdown("---")
    st.subheader("🛡️ Seguridad Renal y Ajustes")
    
    if fge < 30:
        st.error(f"⛔ **FGe {fge}:** Metformina CONTRAINDICADA. Evitar Glibenclamida.")
    elif fge < 45:
        st.warning(f"⚠️ **FGe {fge}:** Reducir dosis de Metformina al 50%.")
    elif fge < 60:
        st.info(f"ℹ️ **FGe {fge}:** Monitorizar función renal cada 3-6 meses.")
    else:
        st.success("✅ Función renal permite dosis plenas de Metformina y mayoría de orales.")

with col_der:
    st.markdown("### 📝 Resumen Clínico")
    st.write(f"**Paciente:** {hba1c_actual}% HbA1c (Meta: {hba1c_meta}%)")
    st.write(f"**Renal:** {fge} ml/min")
    if tiene_ic or tiene_ascvd or tiene_erd:
        st.write("**Perfil:** Alto Riesgo Cardiorrenal")
    else:
        st.write("**Perfil:** Control Glucémico")

# --- FOOTER / DISCLAIMER ---
st.markdown("---")
with st.expander("⚖️ AVISO LEGAL Y FUENTES (Clic para desplegar)", expanded=False):
    st.markdown(DISCLAIMER)
    st.markdown("**Fuentes:**")
    st.markdown("- *Guía de Práctica Clínica Nacional DM2 (Argentina, 2019)*")
    st.markdown("- *Actualización Tratamiento DM2 (SEMI, 2025)*")
