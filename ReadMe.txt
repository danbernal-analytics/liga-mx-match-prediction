Opción 1: LinkedIn Post / Portfolio (Español)
Título: Optimización de Modelos Probabilísticos en la Liga MX: El Peso de la Jerarquía Histórica

Recientemente finalicé el desarrollo de un estimador de probabilidades para la Liga MX utilizando Regresión Logística. Durante el proceso de entrenamiento, identifiqué que depender únicamente de la "forma reciente" (ventanas móviles de 5 partidos) generaba una alta varianza en las predicciones, especialmente en las jornadas inaugurales.

Para estabilizar el modelo, implementé una variable de Jerarquía Histórica (Dynamic Tiering). Al asignar pesos estructurales a los equipos (Tier 1 a Tier 3), logré:

Calibrar el sesgo de localía: Evitando que el modelo sobreestime al equipo local en duelos con brechas de talento evidentes.

Optimización de Log Loss: El modelo final alcanzó un Log Loss de 0.996, superando a arquitecturas más complejas como XGBoost, demostrando que en entornos de datos de baja frecuencia, la linealidad y la robustez superan a la complejidad.

Como aspirante a Football Data Analyst, entiendo que el valor no está en predecir el futuro, sino en capturar con precisión las probabilidades subyacentes para una toma de decisiones informada.

Option 2: Technical Summary / GitHub Readme (English)
Project: Liga MX Probabilistic Forecasting using Logistic Regression & Dynamic Tiering

My focus for this project was to move beyond deterministic "win-lose" predictions and focus on Probability Calibration and Uncertainty Management in professional football.

Key Technical Highlights:

Feature Engineering: Engineered rolling averages for offensive and defensive efficiency. I leveraged a 5-match window to capture tactical momentum without losing long-term signal.

Structural Anchoring: Developed a proprietary "Tier Map" to weight teams based on structural strength. This acted as a Bayesian-like prior that stabilized predictions when short-term form was noisy.

Model Selection: After rigorous testing, Logistic Regression outperformed XGBoost (0.996 vs 1.0042 Log Loss), proving that for Liga MX datasets, a well-featured linear approach offers better generalization.

Visual Analytics: Built a Streamlit Dashboard using Glassmorphism and Plotly to ensure that data insights are not only accurate but also interpretable for non-technical stakeholders (coaching staff or management).