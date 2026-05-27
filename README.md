# 📊 Simulador de Distribuciones de Probabilidad

[cite_start]Este proyecto es una herramienta computacional interactiva desarrollada en Python utilizando **Streamlit** para simular, analizar y visualizar el comportamiento de diferentes variables aleatorias, tanto discretas como continuas[cite: 11, 30]. [cite_start]El sistema calcula de forma automática los estadísticos empíricos y los compara directamente contra sus correspondientes valores teóricos esperados[cite: 23, 26].

[cite_start]Desarrollado para la asignatura de **Probabilidad y Estadística** de la **Ingeniería en Sistemas Computacionales** en **ESCOM - IPN**[cite: 3, 4, 7, 8].

## 🚀 Características del Simulador
- [cite_start]**6 Distribuciones de Probabilidad Implementadas:** [cite: 49]
  - [cite_start]*Variables Discretas:* Binomial, Poisson y Geométrica[cite: 31, 53].
  - [cite_start]*Variables Continuas:* Normal, Uniforme Continua y Exponencial[cite: 32, 53].
- [cite_start]**Validación de Parámetros:** Candados en tiempo real para evitar ingresos de datos inválidos (como probabilidades fuera del rango $[0, 1]$ o desviaciones estándar negativas)[cite: 56, 57].
- [cite_start]**Resultados Numéricos:** Tabulación automática de Media, Varianza y Desviación Estándar (Teórica vs. Simulada) calculando su diferencia[cite: 69, 70, 71, 72, 121, 122].
- [cite_start]**Exportación de Datos (Puntos Extra):** Botones integrables para descargar los reportes tabulados en formato CSV y las gráficas generadas en formato PNG de alta calidad[cite: 131, 132].

## 🛠️ Requisitos e Instalación

Para ejecutar este simulador de forma local en su computadora, asegúrese de contar con Python instalado y ejecute el siguiente comando en su terminal para instalar las dependencias necesarias:

```bash
pip install streamlit numpy scipy matplotlib seaborn pandas