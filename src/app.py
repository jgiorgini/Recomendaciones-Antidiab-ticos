import streamlit as st
import sys
import os

# Agregamos el directorio raíz al path para poder importar módulos propios
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Intentamos importar la base de datos (Vademecum)
try:
    from src.data.vademecum import obtener_ajuste_renal, FARMACOS
except ImportError:
    # Fallback por si la estructura de carpetas varía en local/nube
    try:
        from data.vademecum import obtener_ajuste_renal, FARMACOS
    except:
        st.error("No se pudo cargar el Vademécum. Verifique la estructura de carpetas.")
        FARMACOS = []

# Configuración de la página
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

    st.subheader("3. Comorbilidades")
    col1, col2 = st.columns(2)
    with col1:
        tiene_ic = st.checkbox("Insuf. Cardíaca")
        tiene_ascvd = st.checkbox("Enf. CV (Infarto/ACV)")
    with col2:
        tiene_erd = st.checkbox("Enf. Renal Diabética")
        tiene_obesidad = True if imc >= 30 else False
        if tiene_obesidad:
            st.caption("✅ Obesidad detectada")

# --- PANTALLA PRINCIPAL ---

st.title("Día-D: Recomendación Terapéutica")
st.markdown("---")

# LÓGICA RÁPIDA (PROTOTIPO)
recomendaciones = []

# 1. Regla de Emergencia
if sintomas.startswith("Sí"):
    st.error("🚨 **ALERTA CLÍNICA:** Paciente sintomático/catabólico.")
    st.markdown("### Recomendación Prioritaria:")
    st.info("💉 **INSULINIZACIÓN** (Basal o Esquema intensivo según criterio) +/- Metformina.")
    st.stop() 

# 2. Regla de Comorbilidades
col_izq, col_der = st.columns([2, 1])

with col_izq:
    st.subheader("💊 Esquema Sugerido")
    
    # Driver Cardiorrenal
    if tiene_ic:
        st.success("💙 **Prioridad Insuficiencia Cardíaca:** iSGLT2 (Empagliflozina / Dapagliflozina)")
        recomendaciones.append("empagliflozina")
        recomendaciones.append("dapagliflozina")
        st.caption("Evitar: Pioglitazona, Saxagliptina.")
        
    elif tiene_erd:
        st.success("🧡 **Prioridad Renal:** iSGLT2 (Nefroprotección)")
        recomendaciones.append("empagliflozina")
        recomendaciones.append("dapagliflozina")
        recomendaciones.append("canagliflozina")
        if fge < 30:
            st.warning("⚠️ Si FGe < 30, considerar iDPP4 o aGLP1 según tolerancia.")

    elif tiene_ascvd:
        st.success("❤️ **Prioridad Cardiovascular:** aGLP1 o iSGLT2")
        recomendaciones.append("liraglutida")
        recomendaciones.append("empagliflozina")
        
    elif tiene_obesidad:
        st.info("⚖️ **Prioridad Peso:** aGLP1 (Semaglutida/Tirzepatida)")
        recomendaciones.append("semaglutida_sc")

    # Driver Glucémico
    gap = hba1c_actual - hba1c_meta
    if not recomendaciones:
        recomendaciones.append("metformina") # Base siempre
        if gap < 1.5:
            st.info("💊 **Monoterapia:** Metformina + Estilo de vida") # CORREGIDO AQUÍ
        else:
            st.info("💊 **Terapia Dual:** Metformina + iSGLT2 / iDPP4") # CORREGIDO AQUÍ
            recomendaciones.append("sitagliptina") # Ejemplo

    # 3. DETALLE DE DROGAS Y AJUSTE RENAL (CONECTADO A VADEMECUM)
    st.markdown("---")
    st.subheader("🛡️ Seguridad y Ajuste de Dosis")
    
    if recomendaciones:
        st.write("Detalle de fármacos sugeridos para este perfil:")
        for farmaco_id in recomendaciones:
            # Buscamos los datos en el vademecum
            datos = next((f for f in FARMACOS if f["id"] == farmaco_id), None)
            
            if datos:
                # Calculamos seguridad renal en vivo
                accion, mensaje_renal = obtener_ajuste_renal(farmaco_id, fge)
                
                # Renderizamos tarjeta
                with st.expander(f"**{datos['nombre']}** ({datos['familia']})", expanded=True):
                    col_a, col_b = st.columns([1, 2])
                    with col_a:
                        if accion == "VERDE":
                            st.success(f"Renal: {mensaje_renal}")
                        elif accion == "AMARILLO":
                            st.warning(f"Renal: {mensaje_renal}")
                        else:
                            st.error(f"Renal: {mensaje_renal}")
                    with col_b:
                        st.write(f"**Dosis:** {datos['dosis_habitual']}")
                        st.caption(f"**Comercial (Arg):** {datos['nombres_comerciales_arg']}")

with col_der:
    st.markdown("### 📝 Resumen")
    st.metric("HbA1c Meta", f"{hba1c_meta:.1f}%", delta=f"{hba1c_actual - hba1c_meta:.1f}%", delta_color="inverse")
    st.metric("Función Renal", f"{fge} ml/min")
    
    if tiene_ic or tiene_ascvd or tiene_erd:
        st.warning("Perfil: **Alto Riesgo**")
    else:
        st.success("Perfil: **Metabólico**")

# --- FOOTER ---
st.markdown("---")
with st.expander("⚖️ AVISO LEGAL Y FUENTES", expanded=False):
    st.markdown(DISCLAIMER)
