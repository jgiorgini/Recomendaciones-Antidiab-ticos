"""
BASE DE DATOS DE FÁRMACOS (VADEMÉCUM)
[cite_start]Fuente: Guía Nacional Argentina 2019 [cite: 1] [cite_start]y Actualización SEMI 2025[cite: 2].
"""

# Lista de fármacos con sus propiedades clínicas y reglas de seguridad
FARMACOS = [
    {
        "id": "metformina",
        "nombre": "Metformina",
        "familia": "Biguanida",
        "nombres_comerciales_arg": "DBI, Metforal, Glucophage, Islotin, Baligluc",
        "mecanismo": "Disminuye producción hepática de glucosa (Insulino-sensibilizador).",
        "hba1c_reduccion": "1.5% - 2.0%",
        "dosis_habitual": "500-2550 mg/día (Generalmente 1000-2000 mg)",
        "admin_comidas": "Con las comidas (para reducir efectos GI)",
        "efectos_adversos": "Diarrea, náuseas, dolor abdominal, déficit Vit B12.",
        "ajuste_renal": [
            {"min": 60, "max": 200, "accion": "VERDE", "msg": "Dosis plena permitida."},
            {"min": 45, "max": 59, "accion": "VERDE", "msg": "Precaución: Monitorizar c/ 3-6 meses."}, 
            {"min": 30, "max": 44, "accion": "AMARILLO", "msg": "ALERTA: Reducir dosis al 50% (Máx 1000 mg)."}, 
            {"min": 0, "max": 29, "accion": "ROJO", "msg": "CONTRAINDICADO: Riesgo acidosis láctica."} 
        ]
    },
    {
        "id": "empagliflozina",
        "nombre": "Empagliflozina",
        "familia": "iSGLT2",
        "nombres_comerciales_arg": "Jardiance, Glafornil",
        "mecanismo": "Glucosúrico (elimina glucosa por orina). Cardioprotector.",
        "hba1c_reduccion": "0.4% - 0.7%",
        "dosis_habitual": "10-25 mg una vez al día",
        "admin_comidas": "Con o sin alimentos",
        "efectos_adversos": "Infecciones genitales (micosis), ITU, hipotensión.",
        "ajuste_renal": [
            {"min": 20, "max": 200, "accion": "VERDE", "msg": "Dosis plena (10 mg)."}, 
            {"min": 0, "max": 19, "accion": "ROJO", "msg": "No iniciar (Mantener si ya estaba en tto hasta diálisis)."} 
        ]
    },
    {
        "id": "dapagliflozina",
        "nombre": "Dapagliflozina",
        "familia": "iSGLT2",
        "nombres_comerciales_arg": "Forxiga, Edistride",
        "mecanismo": "Glucosúrico. Cardioprotector (IC).",
        "hba1c_reduccion": "0.4% - 0.7%",
        "dosis_habitual": "10 mg una vez al día",
        "admin_comidas": "Con o sin alimentos",
        "efectos_adversos": "Infecciones genitales, riesgo cetoacidosis euglucémica.",
        "ajuste_renal": [
            {"min": 25, "max": 200, "accion": "VERDE", "msg": "Dosis plena (10 mg)."}, 
            {"min": 0, "max": 24, "accion": "ROJO", "msg": "No iniciar (Mantener si ya estaba en tto hasta diálisis)."} 
        ]
    },
    {
        "id": "canagliflozina",
        "nombre": "Canagliflozina",
        "familia": "iSGLT2",
        "nombres_comerciales_arg": "Invokana",
        "mecanismo": "Glucosúrico.",
        "hba1c_reduccion": "0.4% - 0.7%",
        "dosis_habitual": "100-300 mg una vez al día",
        "admin_comidas": "Preferentemente antes de la primera comida",
        "efectos_adversos": "Infecciones genitales, riesgo amputación (bajo), fracturas.",
        "ajuste_renal": [
            {"min": 30, "max": 200, "accion": "VERDE", "msg": "Dosis plena permitida."}, 
            {"min": 0, "max": 29, "accion": "AMARILLO", "msg": "Usar dosis baja (100 mg) hasta diálisis."} 
        ]
    },
    {
        "id": "sitagliptina",
        "nombre": "Sitagliptina",
        "familia": "iDPP4",
        "nombres_comerciales_arg": "Januvia, Xelevia",
        "mecanismo": "Potencia incretinas (dependiente de glucosa). Neutro en peso.",
        "hba1c_reduccion": "0.6% - 0.8%",
        "dosis_habitual": "100 mg una vez al día",
        "admin_comidas": "Con o sin alimentos",
        "efectos_adversos": "Bien tolerado. Raro: artralgias, pancreatitis.",
        "ajuste_renal": [
            {"min": 45, "max": 200, "accion": "VERDE", "msg": "Dosis plena (100 mg)."}, 
            {"min": 30, "max": 44, "accion": "AMARILLO", "msg": "Ajustar dosis a 50 mg."}, 
            {"min": 0, "max": 29, "accion": "AMARILLO", "msg": "Ajustar dosis a 25 mg."}  
        ]
    },
    {
        "id": "linagliptina",
        "nombre": "Linagliptina",
        "familia": "iDPP4",
        "nombres_comerciales_arg": "Trayenta",
        "mecanismo": "Potencia incretinas. Excreción biliar (seguro en renal).",
        "hba1c_reduccion": "0.6% - 0.8%",
        "dosis_habitual": "5 mg una vez al día",
        "admin_comidas": "Con o sin alimentos",
        "efectos_adversos": "Bien tolerado.",
        "ajuste_renal": [
            {"min": 0, "max": 200, "accion": "VERDE", "msg": "NO REQUIERE AJUSTE (Dosis 5 mg)."} 
        ]
    },
    {
        "id": "vildagliptina",
        "nombre": "Vildagliptina",
        "familia": "iDPP4",
        "nombres_comerciales_arg": "Galvus, Jalra",
        "mecanismo": "Potencia incretinas.",
        "hba1c_reduccion": "0.6% - 0.8%",
        "dosis_habitual": "50 mg dos veces al día (100 mg/día)",
        "admin_comidas": "Con o sin alimentos",
        "efectos_adversos": "Raro: elevación enzimas hepáticas (controlar).",
        "ajuste_renal": [
            {"min": 50, "max": 200, "accion": "VERDE", "msg": "Dosis plena (50 mg c/12hs)."}, 
            {"min": 0, "max": 49, "accion": "AMARILLO", "msg": "Ajustar: 50 mg una vez al día."} 
        ]
    },
    {
        "id": "semaglutida_sc",
        "nombre": "Semaglutida (SC)",
        "familia": "arGLP1",
        "nombres_comerciales_arg": "Ozempic, Wegovy",
        "mecanismo": "Incretina potente. Pérdida de peso y protección CV.",
        "hba1c_reduccion": "1.5% - 1.8%",
        "dosis_habitual": "0.25 a 1.0 mg semanal (Inyectable)",
        "admin_comidas": "Independiente de comidas",
        "efectos_adversos": "GI: Náuseas, vómitos (titular dosis).",
        "ajuste_renal": [
            {"min": 15, "max": 200, "accion": "VERDE", "msg": "Sin ajuste de dosis."}, 
            {"min": 0, "max": 14, "accion": "AMARILLO", "msg": "No recomendado (falta evidencia)."} 
        ]
    },
    {
        "id": "liraglutida",
        "nombre": "Liraglutida",
        "familia": "arGLP1",
        "nombres_comerciales_arg": "Victoza, Saxenda",
        "mecanismo": "Incretina diaria. Protección CV.",
        "hba1c_reduccion": "1.0% - 1.5%",
        "dosis_habitual": "0.6 a 1.8 mg diarios (Inyectable)",
        "admin_comidas": "Independiente de comidas",
        "efectos_adversos": "GI: Náuseas, vómitos.",
        "ajuste_renal": [
            {"min": 15, "max": 200, "accion": "VERDE", "msg": "Sin ajuste de dosis."}, 
            {"min": 0, "max": 14, "accion": "ROJO", "msg": "No recomendado."} 
        ]
    },
    {
        "id": "gliclazida",
        "nombre": "Gliclazida",
        "familia": "Sulfonilurea",
        "nombres_comerciales_arg": "Diamicron, Uniglic",
        "mecanismo": "Secretagogo (estimula páncreas).",
        "hba1c_reduccion": "1.5%",
        "dosis_habitual": "30-120 mg (liberación modificada) en desayuno",
        "admin_comidas": "ANTES del desayuno",
        "efectos_adversos": "Hipoglucemia, aumento de peso.",
        "ajuste_renal": [
            {"min": 45, "max": 200, "accion": "VERDE", "msg": "Precaución por hipoglucemias."},
            {"min": 0, "max": 44, "accion": "ROJO", "msg": "No recomendada (Riesgo hipoglucemia severa)."} 
        ]
    },
    {
        "id": "glimepirida",
        "nombre": "Glimepirida",
        "familia": "Sulfonilurea",
        "nombres_comerciales_arg": "Amaryl, Endial",
        "mecanismo": "Secretagogo.",
        "hba1c_reduccion": "1.5%",
        "dosis_habitual": "1-4 mg diarios",
        "admin_comidas": "ANTES de la primera comida",
        "efectos_adversos": "Hipoglucemia severa, peso.",
        "ajuste_renal": [
            {"min": 50, "max": 200, "accion": "VERDE", "msg": "Iniciar con dosis baja."},
            {"min": 0, "max": 49, "accion": "ROJO", "msg": "CONTRAINDICADO en insuficiencia renal."} 
        ]
    }
]

def obtener_ajuste_renal(farmaco_id, fge_paciente):
    """
    Busca el fármaco y devuelve el estado (VERDE/AMARILLO/ROJO)
    y el mensaje correspondiente según el FGe del paciente.
    """
    farmaco = next((f for f in FARMACOS if f["id"] == farmaco_id), None)
    if not farmaco:
        return "DESCONOCIDO", "Fármaco no encontrado"
    
    for regla in farmaco["ajuste_renal"]:
        if regla["min"] <= fge_paciente <= regla["max"]:
            return regla["accion"], regla["msg"]
            
    return "DESCONOCIDO", "Fuera de rango"
