import streamlit as st
import sys
import os
import pandas as pd # Necesitamos pandas para la tabla linda

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
            st.caption("✅ Obesidad")

# --- PANTALLA PRINCIPAL CON PESTAÑAS ---

st.title("Día-D: Recomendación Terapéutica")

# Creamos dos pestañas
tab1, tab2 = st.tabs(["🧮 Calculadora Terapéutica", "📖 Vademécum Completo"])

# --- PESTAÑA 1: LA CALCULADORA (Lógica anterior) ---
with tab1:
    st.markdown("---")
    
    # LÓGICA RÁPIDA
    recomendaciones = []

    # 1. Regla de Emergencia
    if sintomas.startswith("Sí"):
        st.error("🚨 **ALERTA CLÍNICA:** Paciente sintomático/catabólico.")
        st.info("💉 **INSULINIZACIÓN** (Basal o Esquema intensivo según criterio) +/- Metformina.")
    
    else:
        # 2. Regla de Comorbilidades
        col_izq, col_der = st.columns([2, 1])

        with col_izq:
            st.subheader("💊 Esquema Sugerido")
            
            # Driver Cardiorrenal
            if tiene_ic:
                st.success("💙 **Prioridad Insuficiencia Cardíaca:** iSGLT2")
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
                recomendaciones.append("metformina") 
                if gap < 1.5:
                    st.info("💊 **Monoterapia:** Metformina + Estilo de vida")
                else:
                    st.info("💊 **Terapia Dual:** Metformina + iSGLT2 / iDPP4")
                    recomendaciones.append("sitagliptina") 

            # 3. DETALLE DE DROGAS (Tarjetas)
            st.markdown("---")
            st.subheader("🛡️ Seguridad y Ajuste de Dosis")
            
            if recomendaciones:
                st.write("Detalle de fármacos sugeridos para este perfil:")
                for farmaco_id in recomendaciones:
                    datos = next((f for f in FARMACOS if f["id"] == farmaco_id), None)
                    if datos:
                        accion, mensaje_renal = obtener_ajuste_renal(farmaco_id, fge)
                        
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
            # Corrección de decimales aplicada aquí (.1f)
            st.metric("HbA1c Meta", f"{hba1c_meta:.1f}%", delta=f"{hba1c_actual - hba1c_meta:.1f}%", delta_color="inverse")
            st.metric("Función Renal", f"{fge} ml/min")
            
            if tiene_ic or tiene_ascvd or tiene_erd:
                st.warning("Perfil: **Alto Riesgo**")
            else:
                st.success("Perfil: **Metabólico**")

# --- PESTAÑA 2: VADEMECUM (TABLA) ---
with tab2:
    st.header("📖 Tabla Comparativa de Fármacos")
    st.markdown("Referencia rápida de familias, mecanismos y ajustes.")
    
    # Procesamos los datos para que se vean bien en una tabla plana
    tabla_datos = []
    for f in FARMACOS:
        tabla_datos.append({
            "Fármaco": f["nombre"],
            "Familia": f["familia"],
            "Mecanismo": f["mecanismo"],
            "Reducción HbA1c": f["hba1c_reduccion"],
            "Dosis Habitual": f["dosis_habitual"],
            "Efectos Adversos": f["efectos_adversos"],
            "Nombres Comerciales": f["nombres_comerciales_arg"]
        })
    
    # Creamos un DataFrame de Pandas
    df = pd.DataFrame(tabla_datos)
    
    # Mostramos la tabla interactiva
    st.dataframe(
        df, 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "Fármaco": st.column_config.TextColumn(width="medium"),
            "Mecanismo": st.column_config.TextColumn(width="large"),
            "Nombres Comerciales": st.column_config.TextColumn(width="medium"),
        }
    )

# --- FOOTER ---
st.markdown("---")
with st.expander("⚖️ AVISO LEGAL Y FUENTES", expanded=False):
    st.markdown(DISCLAIMER)
