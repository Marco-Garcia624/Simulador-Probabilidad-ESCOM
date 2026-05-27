import streamlit as st
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import io

# Configuración de la página
st.set_page_config(page_title="Simulador de Distribuciones ESCOM", layout="wide")
st.title("📊 Simulador de Distribuciones de Probabilidad")
st.write("Proyecto Segundo Parcial - Probabilidad y Estadística")

# ==========================================
# BARRA LATERAL: Selección y Configuración
# ==========================================
st.sidebar.header("Configuración de la Simulación")

# Selector de tipo y distribución
tipo_dist = st.sidebar.radio("Tipo de Variable", ["Discreta", "Continua"])

if tipo_dist == "Discreta":
    dist_name = st.sidebar.selectbox("Distribución", ["Binomial", "Poisson", "Geométrica"])
else:
    dist_name = st.sidebar.selectbox("Distribución", ["Normal", "Uniforme Continua", "Exponencial"])

# Tamaño de la muestra con validación inmediata
n_muestra = st.sidebar.number_input("Tamaño de muestra (N)", min_value=1, value=1000, step=100)

# Inicialización de variables para cálculos
valores_simulados = []
mu_teorica, var_teorica = 0.0, 0.0
es_valido = True
mensaje_error = ""

# ==========================================
# VALIDACIÓN DE PARÁMETROS Y SIMULACIÓN
# ==========================================
if dist_name == "Binomial":
    st.sidebar.subheader("Parámetros")
    n_ensayos = st.sidebar.number_input("Número de ensayos (n)", min_value=1, value=10)
    p_exito = st.sidebar.number_input("Probabilidad de éxito (p)", min_value=0.0, max_value=1.0, value=0.5, step=0.05)
    
    if p_exito < 0.0 or p_exito > 1.0:
        es_valido = False
        mensaje_error = "La probabilidad 'p' debe estar estrictamente entre 0 y 1."
    else:
        valores_simulados = np.random.binomial(n_ensayos, p_exito, n_muestra)
        mu_teorica = n_ensayos * p_exito
        var_teorica = n_ensayos * p_exito * (1 - p_exito)

elif dist_name == "Poisson":
    st.sidebar.subheader("Parámetros")
    lam = st.sidebar.number_input("Parámetro Lambda (λ)", value=4.0, step=0.5)
    
    if lam <= 0:
        es_valido = False
        mensaje_error = "El parámetro Lambda (λ) debe ser mayor que cero."
    else:
        valores_simulados = np.random.poisson(lam, n_muestra)
        mu_teorica = lam
        var_teorica = lam

elif dist_name == "Geométrica":
    st.sidebar.subheader("Parámetros")
    p_geom = st.sidebar.number_input("Probabilidad de éxito (p)", min_value=0.0, max_value=1.0, value=0.3, step=0.05)
    
    if p_geom <= 0.0 or p_geom > 1.0:
        es_valido = False
        mensaje_error = "Para la distribución Geométrica, 'p' debe estar en el intervalo (0, 1]."
    else:
        valores_simulados = np.random.geometric(p_geom, n_muestra)
        mu_teorica = 1 / p_geom
        var_teorica = (1 - p_geom) / (p_geom ** 2)

elif dist_name == "Normal":
    st.sidebar.subheader("Parámetros")
    media = st.sidebar.number_input("Media (μ)", value=0.0)
    sigma = st.sidebar.number_input("Desviación estándar (σ)", value=1.0, step=0.1)
    
    if sigma <= 0:
        es_valido = False
        mensaje_error = "La desviación estándar (σ) debe ser un valor positivo."
    else:
        valores_simulados = np.random.normal(media, sigma, n_muestra)
        mu_teorica = media
        var_teorica = sigma ** 2

elif dist_name == "Uniforme Continua":
    st.sidebar.subheader("Parámetros")
    lim_inf = st.sidebar.number_input("Límite inferior (a)", value=0.0)
    lim_sup = st.sidebar.number_input("Límite superior (b)", value=10.0)
    
    if lim_inf >= lim_sup:
        es_valido = False
        mensaje_error = "El límite inferior (a) debe ser estrictamente menor que el límite superior (b)."
    else:
        valores_simulados = np.random.uniform(lim_inf, lim_sup, n_muestra)
        mu_teorica = (lim_inf + lim_sup) / 2
        var_teorica = ((lim_sup - lim_inf) ** 2) / 12

elif dist_name == "Exponencial":
    st.sidebar.subheader("Parámetros")
    beta = st.sidebar.number_input("Escala (β = 1/λ)", value=2.0, step=0.5)
    
    if beta <= 0:
        es_valido = False
        mensaje_error = "El parámetro de escala (β) debe ser mayor que cero."
    else:
        valores_simulados = np.random.exponential(beta, n_muestra)
        mu_teorica = beta
        var_teorica = beta ** 2

# ==========================================
# DESPLIEGUE DE RESULTADOS Y EXPORTACIONES
# ==========================================
if not es_valido:
    st.error(f"❌ Error de validación: {mensaje_error}")
else:
    # Estadísticos empíricos
    mu_simulada = float(np.mean(valores_simulados))
    var_simulada = float(np.var(valores_simulados))
    sigma_teorica = float(np.sqrt(var_teorica))
    sigma_simulada = float(np.sqrt(var_simulada))
    
    # Renderizar la tabla de resultados
    st.header(f"Resultados Numéricos: Distribución {dist_name}")
    
    data_tabla = {
        "Concepto": ["Media", "Varianza", "Desviación estándar", "Tamaño de muestra"],
        "Valor teórico": [round(mu_teorica, 4), round(var_teorica, 4), round(sigma_teorica, 4), n_muestra],
        "Valor simulado": [round(mu_simulada, 4), round(var_simulada, 4), round(sigma_simulada, 4), n_muestra],
        "Diferencia": [round(abs(mu_teorica - mu_simulada), 4), round(abs(var_teorica - var_simulada), 4), round(abs(sigma_teorica - sigma_simulada), 4), 0]
    }
    
    df_resultados = pd.DataFrame(data_tabla)
    st.table(df_resultados)
    
    # 💾 BOTÓN DE EXPORTACIÓN 1: Descargar tabla en CSV
    csv_buffer = io.StringIO()
    df_resultados.to_csv(csv_buffer, index=False)
    st.download_button(
        label="📥 Descargar Tabla Comparativa (CSV)",
        data=csv_buffer.getvalue(),
        file_name=f"resultados_{dist_name.lower().replace(' ', '_')}.csv",
        mime="text/csv"
    )
    
    # Generar la sección gráfica
    st.header("Visualización Gráfica")
    fig, ax = plt.subplots(figsize=(10, 5))
    
    if tipo_dist == "Discreta":
        valores, conteos = np.unique(valores_simulados, return_counts=True)
        frec_relativas = conteos / n_muestra
        ax.bar(valores, frec_relativas, alpha=0.6, color="royalblue", label="Simulado (Frec. Relativa)", edgecolor="black")
        
        x_teorico = np.arange(int(min(valores_simulados)), int(max(valores_simulados)) + 1)
        if dist_name == "Binomial":
            y_teorico = stats.binom.pmf(x_teorico, n_ensayos, p_exito)
        elif dist_name == "Poisson":
            y_teorico = stats.poisson.pmf(x_teorico, lam)
        elif dist_name == "Geométrica":
            y_teorico = stats.geom.pmf(x_teorico, p_geom)
            
        ax.scatter(x_teorico, y_teorico, color="red", zorder=3, label="Teórico (PMF)")
        ax.vlines(x_teorico, 0, y_teorico, colors="red", linestyles="dashed", alpha=0.5)

    else:
        sns.histplot(valores_simulados, stat="density", kde=False, alpha=0.5, color="seagreen", label="Simulado (Densidad)", ax=ax, edgecolor="black")
        
        x_teorico = np.linspace(float(min(valores_simulados)), float(max(valores_simulados)), 500)
        if dist_name == "Normal":
            y_teorico = stats.norm.pdf(x_teorico, media, sigma)
        elif dist_name == "Uniforme Continua":
            y_teorico = stats.uniform.pdf(x_teorico, lim_inf, lim_sup - lim_inf)
        elif dist_name == "Exponencial":
            y_teorico = stats.expon.pdf(x_teorico, scale=beta)
            
        ax.plot(x_teorico, y_teorico, color="darkorange", linewidth=2, label="Teórico (PDF)")

    ax.set_title(f"Comparación Teórica vs. Simulación: {dist_name}")
    ax.set_xlabel("Variable Aleatoria (X)")
    ax.set_ylabel("Probabilidad / Densidad")
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    st.pyplot(fig)
    
    # 💾 BOTÓN DE EXPORTACIÓN 2: Descargar gráfica en PNG
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format="png", bbox_inches="tight")
    img_buffer.seek(0)
    st.download_button(
        label="🖼️ Descargar Gráfica (PNG)",
        data=img_buffer,
        file_name=f"grafica_{dist_name.lower().replace(' ', '_')}.png",
        mime="image/png"
    )