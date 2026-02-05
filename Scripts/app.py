import os
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import base64
import streamlit.components.v1 as components
import plotly.graph_objects as go # <--- IMPORTANTE: Nueva librería para el gráfico

# =====================================================
# PATHS BASE (PORTABLES)
# =====================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(BASE_DIR, "..", "Data", "matches_model.csv")
MODEL_PATH = os.path.join(BASE_DIR, "..", "Model", "logreg_model.pkl")
ASSETS_PATH = os.path.join(BASE_DIR, "..", "Assets")
BG_IMAGE_PATH = os.path.join(ASSETS_PATH, "background.jpeg")

# =====================================================
# FONDO PERSONALIZADO
# =====================================================
def set_custom_design(image_relative_path):
    base_path = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(base_path, "..", image_relative_path)

    try:
        with open(image_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()

        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpeg;base64,{data}");
                background-size: cover;
                background-position: center bottom;
                background-attachment: fixed;
            }}

            [data-testid="stMetric"] {{
                background: rgba(255, 255, 255, 0.1) !important;
                backdrop-filter: blur(15px);
                border-radius: 15px;
                padding: 15px 10px;
                border: 1px solid rgba(255, 255, 255, 0.2);
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
            }}

            h1, h2, h3, span, p, label, [data-testid="stMarkdownContainer"] {{
                color: white !important;
                text-shadow: 1px 1px 3px rgba(0,0,0,0.8);
            }}

            [data-testid="stDataFrame"] {{
                background: rgba(0, 0, 0, 0.2) !important;
                backdrop-filter: blur(10px);
                border-radius: 10px;
            }}

            [data-testid="stSidebar"] {{
                background-color: rgba(0, 0, 0, 0.7) !important;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except Exception as e:
        st.warning(f"Error cargando diseño: {e}")

set_custom_design("Assets/background.jpeg")

# =====================================================
# CONFIGURACIÓN GENERAL
# =====================================================
st.title("⚽ Liga MX Match Probability Estimator")
st.markdown("Modelo de **Regresión Logística** con jerarquía histórica y forma reciente.")

TIER_MAP = {
    'Club América': 1, 'Tigres UANL': 1, 'Monterrey': 1, 'Cruz Azul': 1, 'Toluca FC': 1,
    'Guadalajara': 2, 'Pachuca': 2, 'León': 2, 'Pumas UNAM': 2, 'Santos Laguna': 2,
    'Tijuana': 3, 'Atlas': 3, 'Atlético de San Luis': 3, 'Necaxa': 3,
    'Querétaro': 3, 'Puebla': 3, 'Juárez': 3, 'Mazatlán FC': 3
}

@st.cache_data
def load_data(ttl=3600):
    return pd.read_csv(
        DATA_PATH,
        parse_dates=["date"]
    )
    ## Ruta local original (NO usar en cloud)
    ## r"D:\101010 Revisiones\GitHub\liga-mx-match-prediction\Data\matches_model.csv"

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)
    ## Ruta local original (NO usar en cloud)
    ## r"D:\101010 Revisiones\GitHub\liga-mx-match-prediction\Model\logreg_model.pkl"

df = load_data()
model = load_model()

# =====================================================
# FUNCIONES AUXILIARES
# =====================================================
def get_last_matches(df, team, n=5):
    return (
        df[(df["home_team"] == team) | (df["away_team"] == team)]
        .sort_values("date", ascending=False)
        .head(n)
    )

def calculate_features(df, team):
    last = get_last_matches(df, team)
    if len(last) < 1:
        return None

    goals_for, goals_against, points = [], [], []
    for _, row in last.iterrows():
        if row["home_team"] == team:
            gf, ga = row["home_goals"], row["away_goals"]
        else:
            gf, ga = row["away_goals"], row["home_goals"]
        goals_for.append(gf)
        goals_against.append(ga)
        points.append(3 if gf > ga else 1 if gf == ga else 0)

    return {
        "form_5": np.mean(points),
        "goals_for_5": np.mean(goals_for),
        "goals_against_5": np.mean(goals_against)
    }

# =====================================================
# INTERFAZ DE USUARIO
# =====================================================
st.sidebar.header("Configuración del Partido")
teams = sorted(TIER_MAP.keys())
home_team = st.sidebar.selectbox("Equipo Local", teams)
away_team = st.sidebar.selectbox("Equipo Visitante", teams)

if home_team == away_team:
    st.warning("⚠️ El equipo local y visitante no pueden ser el mismo.")
    st.stop()

home_feat = calculate_features(df, home_team)
away_feat = calculate_features(df, away_team)

if home_feat is None or away_feat is None:
    st.warning("⚠️ Datos insuficientes para estos equipos.")
    st.stop()

st.sidebar.caption("Dashboard desarrollado por Dan Bernal")
st.sidebar.caption("danbernal.analytics@gmail.com")

# =====================================================
# CONSTRUCCIÓN DEL INPUT
# =====================================================
h_tier = TIER_MAP.get(home_team, 2)
a_tier = TIER_MAP.get(away_team, 2)
diff_tier_val = int(a_tier) - int(h_tier)

X = pd.DataFrame([{
    "diff_tier": diff_tier_val,
    "diff_form_5": home_feat["form_5"] - away_feat["form_5"],
    "diff_goals_for_5": home_feat["goals_for_5"] - away_feat["goals_for_5"],
    "diff_goals_against_5": home_feat["goals_against_5"] - away_feat["goals_against_5"]
}])

st.subheader("Análisis de Fuerza")
c_t1, c_t2 = st.columns(2)
c_t1.metric(f"Tier {home_team}", h_tier)
c_t2.metric(f"Tier {away_team}", a_tier)

st.caption(
    "El 'Tier' refleja la jerarquía histórica del equipo en la Liga MX, "
    "basada en su desempeño y logros en temporadas recientes."
)
st.markdown("1 = Elite | 2 = Medio | 3 = Bajo")

st.divider()

if st.button("🔮 Calcular Probabilidades"):
    probs_raw = model.predict_proba(X)[0]
    prob_dict = dict(zip(model.classes_, probs_raw))

    ordered_labels = ["Victoria Local", "Empate", "Victoria Visitante"]
    ordered_values = [prob_dict.get("H", 0), prob_dict.get("D", 0), prob_dict.get("A", 0)]

    st.subheader("Predicción Probabilística")
    c1, c2, c3 = st.columns(3)
    c1.metric(ordered_labels[0], f"{ordered_values[0]:.2%}")
    c2.metric(ordered_labels[1], f"{ordered_values[1]:.2%}")
    c3.metric(ordered_labels[2], f"{ordered_values[2]:.2%}")

    fig = go.Figure(go.Bar(
        x=ordered_labels,
        y=ordered_values,
        marker_color=['#557B55', '#E0E0E0', '#B35A5A'],
        text=[f"{v:.1%}" for v in ordered_values],
        textposition='auto',
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white"),
        height=350,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False, range=[0, 1])
    )
    st.plotly_chart(fig, use_container_width=True)

    favorite_prob = max(ordered_values)
    if favorite_prob >= 0.65:
        level, interpretation = "Alta", "Superioridad clara basada en jerarquía y forma."
    elif favorite_prob >= 0.45:
        level, interpretation = "Media", "Tendencia marcada, pero el partido será disputado."
    else:
        level, interpretation = "Baja", "Partido muy equilibrado o alta probabilidad de sorpresa."

    st.metric("🔎 Nivel de Confianza", level)
    st.info(interpretation)

    st.caption(
        "Las probabilidades reflejan la estimación del modelo dado el contexto actual. "
        "No representan certezas ni recomendaciones de apuesta."
    )

# =====================================================
# DATOS RECIENTES
# =====================================================
st.divider()
st.subheader("Datos Recientes (Últimos 5 Partidos)")
c_h, c_a = st.columns(2)

with c_h:
    recent_h = get_last_matches(df, home_team)[['date', 'home_team', 'home_goals', 'away_goals', 'away_team', 'result']]
    recent_h.columns = ['Fecha', 'Local', 'GL', 'GV', 'Visita', 'Res']
    st.dataframe(recent_h, hide_index=True)

with c_a:
    recent_a = get_last_matches(df, away_team)[['date', 'home_team', 'home_goals', 'away_goals', 'away_team', 'result']]
    recent_a.columns = ['Fecha', 'Local', 'GL', 'GV', 'Visita', 'Res']
    st.dataframe(recent_a, hide_index=True)

st.caption("GL: Goles Local | GV: Goles Visitante")

# =====================================================
# BLOQUE ÉTICO
# =====================================================
st.divider()
st.caption(
    "⚠️ Este sistema estima probabilidades basadas en patrones históricos. "
    "No predice resultados futuros con certeza ni garantiza beneficios."
)

# =====================================================
# FIN DEL SCRIPT
# =====================================================
#==============
# Correr APP
# streamlit run app.py
# colocarse en la carpeta donde está app.py
#==============