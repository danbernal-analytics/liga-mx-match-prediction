# ⚽ Liga MX Match Probability Estimator
**Modelado probabilístico y cuantificación de incertidumbre en Football Analytics**

`dashboard link:` https://ligamx-match-prediction-vlpu.onrender.com/

## 🎯 Objetivo del Proyecto
El fútbol es un deporte de baja frecuencia de eventos y alta varianza. El objetivo de este proyecto no es realizar predicciones deterministas (ganar/perder), sino construir un modelo estadístico calibrado que estime probabilidades reales para los resultados: **Victoria Local**, **Empate** y **Victoria Visitante**.

## ⚙️ Metodología y Feature Engineering

### 1. Integridad Temporal (Anti-Leakage)
Se implementó un protocolo estricto de validación temporal.
* **Corte temporal:** `2025-01-01`.
* **Entrenamiento:** Datos históricos 2012-2024 (4070 partidos).
* **Test:** Temporada 2025 en adelante (196 partidos).
* **Rolling Windows:** Todas las métricas de forma se calcularon con un `shift(1)` para garantizar que el modelo solo \"vea\" información disponible antes del pitazo inicial.

### 2. Variables Dinámicas
En lugar de promedios globales, se generaron features de ventanas móviles (5 partidos) para capturar el *momentum*:
* `diff_form_5`: Diferencia de puntos obtenidos en los últimos 5 juegos.
* `diff_goals_for/against`: Diferencia en eficiencia ofensiva y defensiva reciente.

### 3. Jerarquía Estructural (Tiering)
Se creó un **Ranking Histórico** dividiendo a los equipos en 3 Tiers (Élite, Medio, Bajo) basado en su *win rate* y diferencia de goles histórica.
* **Impacto:** La variable `diff_tier` (Diferencia de Jerarquía) resultó ser la característica más importante del modelo (consistentemente destacada como una de las variables más influyentes), validando que la historia pesa más que la racha reciente en la Liga MX.

## 📊 Resultados y Evaluación
La métrica principal de éxito fue el **Log Loss**, que penaliza la incertidumbre y premia la calibración.

| Modelo | Log Loss | Observación |
| :--- | :--- | :--- |
| **Baseline (Frecuencia Histórica)** | `1.0578` | Probabilidad "ciega" basada solo en localía. |
| **XGBoost (Calibrado)** | `1.0145` | Ligero sobreajuste por la complejidad del modelo. |
| **Logistic Regression (Final)** | **`1.0103`** | **Mejor rendimiento y generalización.** |

**Conclusión Técnica:**
A pesar de la popularidad de los modelos de Boosting, la **Regresión Logística** demostró ser superior para este volumen de datos. Su naturaleza lineal capturó eficientemente la ventaja de localía (coeficiente positivo consistente con la ventaja histórica de localía) y la jerarquía de los equipos, ofreciendo probabilidades más robustas y menos propensas al ruido que XGBoost.

## 🛠️ Stack Tecnológico
* **Lenguaje:** Python.
* **Data Processing:** Pandas, NumPy (Manejo de series temporales y rolling windows).
* **Machine Learning:** Scikit-learn (LogisticRegression, CalibratedClassifierCV), XGBoost.
* **Visualización:** Matplotlib, Seaborn (Curvas de calibración y Feature Importance).
* **Despliegue:** Streamlit (Dashboard interactivo).

---
Desarrollado por: Dan Bernal
Data Analyst | Tactical & Performance | Probabilistic Modeling
