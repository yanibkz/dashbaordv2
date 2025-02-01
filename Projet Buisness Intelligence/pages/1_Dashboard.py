import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
from config import DATABASE_URL  # Importer l'URL PostgreSQL

st.set_page_config(page_title="Dashboard - Engagement", layout="wide")

# 🔹 Charger les données depuis PostgreSQL au lieu du CSV
@st.cache_data
def load_data():
    engine = create_engine(DATABASE_URL)
    query = "SELECT * FROM engagement_data"
    df = pd.read_sql(query, engine)
    return df

df = load_data()


st.title("KPI Dashboard - Engagement des Contributeurs")
st.subheader("Visualisez les indicateurs clés de performance")

# ----------------------------
# Sélecteur de source de trafic (filtre)
# ----------------------------
all_mediums = sorted(df["medium"].unique())
selected_medium = st.selectbox(
    "Choisissez un canal de trafic à afficher :",
    options=["Tous"] + all_mediums,
    index=0
)

if selected_medium != "Tous":
    df = df[df["medium"] == selected_medium]

# ----------------------------
# Calculs des métriques de base
# ----------------------------
if not df.empty:
    avg_pageviews = df["num_pageviews"].mean()
    bounce_rate = df["is_bounce"].mean() * 100
    peak_hour = df["hour_x"].mode()[0]

    # Calcul des proportions
    regular_visitors = df["is_new_visitor"].value_counts(normalize=True).get(0, 0) * 100
    new_visitors = df["is_new_visitor"].value_counts(normalize=True).get(1, 0) * 100
else:
    avg_pageviews = 0
    bounce_rate = 0
    peak_hour = "N/A"
    regular_visitors = 0
    new_visitors = 0

# ----------------------------
# Affichage des KPI
# ----------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Pages Vues Moyennes", f"{avg_pageviews:.1f}")
    with st.expander("Détails des Pages Vues"):
        if not df.empty:
            fig_pageviews = px.histogram(df, x="num_pageviews", nbins=20, title="Distribution des Pages Vues")
            st.plotly_chart(fig_pageviews, use_container_width=True)
        else:
            st.write("Aucune donnée pour ce filtre.")

with col2:
    st.metric("Taux de Rebond (%)", f"{bounce_rate:.1f}%")
    with st.expander("Détails sur le Taux de Rebond"):
        if not df.empty:
            df_bounce = df.groupby("medium")["is_bounce"].mean().reset_index()
            fig_bounce = px.bar(
                df_bounce,
                x="medium",
                y="is_bounce",
                title="Taux de Rebond par Canal",
                labels={"is_bounce": "Taux de Rebond", "medium": "Canal"}
            )
            st.plotly_chart(fig_bounce, use_container_width=True)
        else:
            st.write("Aucune donnée pour ce filtre.")

with col3:
    st.metric("Heure de Pic d'Activité", f"{peak_hour}h")
    with st.expander("Détails sur l'Activité Horaire"):
        if not df.empty:
            fig_hourly = px.line(
                df.groupby("hour_x")["session_id"].count().reset_index(),
                x="hour_x",
                y="session_id",
                title="Évolution des Sessions par Heure",
                labels={"hour_x": "Heure de la Journée", "session_id": "Nombre de Sessions"}
            )
            st.plotly_chart(fig_hourly, use_container_width=True)
        else:
            st.write("Aucune donnée pour ce filtre.")

with col4:
    st.metric("Visiteurs : Réguliers vs Nouveaux", f"{regular_visitors:.1f}% / {new_visitors:.1f}%")
    with st.expander("Répartition des Visiteurs"):
        if not df.empty:
            fig_visitors = px.pie(
                names=["Visiteurs Réguliers", "Nouveaux Visiteurs"],
                values=[regular_visitors, new_visitors],
                title="Proportion de Visiteurs"
            )
            st.plotly_chart(fig_visitors, use_container_width=True)
        else:
            st.write("Aucune donnée pour ce filtre.")

# ----------------------------
# Bloc de visualisations interactives
# ----------------------------
st.header("Visualisations Clés")

row1_col1, row1_col2 = st.columns(2)

# 1) Moyenne des Pages Vues par Canal
with row1_col1:
    if not df.empty:
        df_medium_pageviews = df.groupby("medium", as_index=False)["num_pageviews"].mean()
        fig_medium = px.bar(
            df_medium_pageviews, 
            x="medium", 
            y="num_pageviews", 
            title="Pages Vues Moyennes par Canal",
            labels={"medium": "Canal", "num_pageviews": "Pages Vues Moyennes"}
        )
        st.plotly_chart(fig_medium, use_container_width=True)
    else:
        st.write("Aucune donnée.")

# 2) Proportion des Sessions par Canal
with row1_col2:
    if not df.empty:
        df_medium_count = df["medium"].value_counts(normalize=True) * 100
        fig_medium_pie = px.pie(
            names=df_medium_count.index,
            values=df_medium_count.values,
            title="Proportion des Sessions par Canal",
        )
        st.plotly_chart(fig_medium_pie, use_container_width=True)
    else:
        st.write("Aucune donnée.")

row2_col1, row2_col2 = st.columns(2)

# 3) Activité par Heure : Nouveaux vs Réguliers
with row2_col1:
    if not df.empty:
        fig_hour_comparison = px.histogram(
            df, 
            x="hour_x", 
            color="is_new_visitor",
            barmode="group",
            title="Activité par Heure : Nouveaux vs Réguliers",
            labels={"is_new_visitor": "Type de Visiteur"}
        )
        st.plotly_chart(fig_hour_comparison, use_container_width=True)
    else:
        st.write("Aucune donnée.")

# 4 & 5) Graphique interactif : Sessions vs Nouveaux Utilisateurs
with row2_col2:
    if not df.empty:
        fig_toggle = go.Figure()

        # Trace 1 : Nombre de sessions par canal
        df_sessions = df.groupby("medium")["session_id"].count().reset_index()
        fig_toggle.add_trace(go.Bar(
            x=df_sessions["medium"],
            y=df_sessions["session_id"],
            name="Nombre de Sessions"
        ))

        # Trace 2 : Nouveaux utilisateurs par canal
        df_new_users = df[df["is_new_visitor"] == 1].groupby("medium")["session_id"].count().reset_index()
        fig_toggle.add_trace(go.Bar(
            x=df_new_users["medium"],
            y=df_new_users["session_id"],
            name="Nouveaux Utilisateurs"
        ))

        # Ajout de boutons interactifs positionnés à côté du graphique
        fig_toggle.update_layout(
            margin={"r": 150},  # marge à droite pour laisser de la place aux boutons
            title="Comparaison des Canaux : Sessions vs Nouveaux Utilisateurs",
            updatemenus=[
                dict(
                    type="buttons",
                    direction="down",
                    showactive=True,
                    x=1.1,      # positionné à l'extérieur du graphique
                    xanchor="left",
                    y=0.5,      # centré verticalement par rapport au graphique
                    yanchor="middle",
                    pad={"r": 10, "t": 10},
                    buttons=[
                        dict(
                            label="Sessions",
                            method="update",
                            args=[{"visible": [True, False]},
                                  {"title": "Sessions par Canal"}]
                        ),
                        dict(
                            label="Nouveaux Utilisateurs",
                            method="update",
                            args=[{"visible": [False, True]},
                                  {"title": "Nouveaux Utilisateurs par Canal"}]
                        ),
                        dict(
                            label="Comparaison",
                            method="update",
                            args=[{"visible": [True, True]},
                                  {"title": "Comparaison des Canaux : Sessions vs Nouveaux Utilisateurs"}]
                        )
                    ]
                )
            ]
        )
        st.plotly_chart(fig_toggle, use_container_width=True)
    else:
        st.write("Aucune donnée.")
