# ⚽ Predicción Probabilística de Resultados en la Liga MX
Modelado estadístico para cuantificación de incertidumbre en football analytics

**dashboard link:** **https://ligamx-match-prediction-vlpu.onrender.com/**

## 🎯 Objetivo 

Desarrollar un modelo de machine learning que permita estimar probabilidades de resultado (Victoria Local, Empate, Victoria Visitante) en partidos de la Liga MX, con el objetivo de apoyar la toma de decisiones analíticas y el análisis estratégico, superando enfoques deterministas basados únicamente en predicciones puntuales.

## 💡 Resumen y Solución Analítica

El proyecto se centró en la construcción de un pipeline completo de análisis y modelado predictivo aplicado a fútbol profesional. A partir de datos históricos de partidos, se realizó feature engineering orientado al contexto deportivo, incorporando métricas de forma reciente mediante ventanas temporales (rolling windows) y jerarquía competitiva (tiers) para capturar diferencias estructurales entre equipos.

Se implementó un esquema de validación temporal estricta por año, respetando la naturaleza secuencial de las temporadas (Apertura/Clausura) y evitando data leakage. Como modelos principales se evaluaron Regresión Logística Multiclase y XGBoost, priorizando métricas probabilísticas sobre métricas de clasificación tradicionales.

---

## 📊 Impacto y Conclusiones

Calidad Probabilística sobre Precisión: El desempeño se evaluó mediante Log Loss, permitiendo medir no solo si el modelo “acierta”, sino qué tan bien calibra la incertidumbre asociada a cada resultado posible.

Simplicidad vs Complejidad: La Regresión Logística obtuvo un Log Loss ligeramente inferior al de XGBoost, evidenciando que, para el volumen y la estructura de los datos disponibles, un modelo lineal captura de forma eficiente la señal relevante sin introducir varianza innecesaria.

Interpretabilidad y Estabilidad: El modelo final ofrece probabilidades consistentes y explicables, facilitando su uso en contextos analíticos donde la comprensión del porqué es tan importante como la predicción en sí.

Análisis de Calibración: La evaluación mediante curvas de calibración mostró una alineación razonable entre probabilidades predichas y resultados observados, reforzando la utilidad del modelo como herramienta de análisis probabilístico.

Aplicación Práctica: Los resultados del modelo se integraron en un dashboard interactivo, permitiendo simular enfrentamientos y traducir el output estadístico en insights accionables para usuarios no técnicos.

---

# 🧠 Consideraciones Metodológicas

* Uso de validación temporal en lugar de splits aleatorios.
* Priorización de métricas probabilísticas (Log Loss) sobre accuracy.
* Reconocimiento explícito de la alta varianza e incertidumbre inherentes al fútbol.
* Enfoque en robustez y generalización más que en optimización extrema del modelo.

## 🛠️ Stack Tecnológico
* **Lenguaje:** Python
* **Librerías Clave:** Pandas, NumPy, Scikit-learn (Logistic Regression, métricas, calibración), XGBoost, Matplotlib / Plotly (visualización)
* **Metodología:** **Feature Engineering con ventanas temporales (rolling metrics)**, **Modelado Multiclase**, **Validación Temporal**, **Modelado Probabilístico**, **Football Analytics aplicado a Liga MX**
