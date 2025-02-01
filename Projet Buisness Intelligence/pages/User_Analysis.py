import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from config import DATABASE_URL  # Importer l'URL PostgreSQL

@st.cache_data
def load_data():
    engine = create_engine(DATABASE_URL)
    query = "SELECT * FROM engagement_data"
    df = pd.read_sql(query, engine)
    return df

df = load_data()


# Vérifier les colonnes disponibles
if "visitor_id" not in df.columns or "session_id" not in df.columns:
    st.error("Les colonnes nécessaires ('visitor_id', 'session_id') sont absentes des données.")
    st.stop()

# Supprimer les doublons pour éviter les erreurs d'analyse
df = df.drop_duplicates()

# Filtrer les utilisateurs ayant visité plus d'une fois
visitor_counts = df["visitor_id"].value_counts()
frequent_visitors = visitor_counts[visitor_counts > 1].index
filtered_df = df[df["visitor_id"].isin(frequent_visitors)]

# Vérifier s'il y a des utilisateurs fréquents
if filtered_df.empty:
    st.warning("Aucun utilisateur avec plus d'une visite trouvé.")
    st.stop()

# Sélectionner un utilisateur parmi ceux ayant visité plus d'une fois
user_ids = filtered_df["visitor_id"].unique()
selected_user = st.selectbox("Sélectionnez un utilisateur (avec >1 visite) :", options=user_ids)

# Filtrer les données pour l'utilisateur sélectionné
user_data = filtered_df[filtered_df["visitor_id"] == selected_user]

# Vérifiez si les données de l'utilisateur existent
if user_data.empty:
    st.warning("Aucune donnée pour cet utilisateur sélectionné.")
else:
    st.write(f"### Analyse pour l'utilisateur : {selected_user}")

    # Afficher un aperçu des données de l'utilisateur
    st.write(user_data.head())

    # Calcul d'un score d'engagement basé sur les colonnes disponibles
    if all(col in user_data.columns for col in ["num_pageviews", "is_bounce"]):
        score_engagement = (
            user_data["num_pageviews"].mean() * (1 - user_data["is_bounce"].mean())
        )
        st.metric("Score d'Engagement", f"{score_engagement:.2f}")

        # Bouton pour afficher les explications du score d'engagement
        with st.expander("ℹ️ Explication du Score d'Engagement"):
            st.markdown("""
            **Comment le score d'engagement est calculé :**
            
            - **Pages Vues Moyennes** : Représente la moyenne des pages vues par session pour cet utilisateur.
            - **Taux de Rebonds Inverse (1 - Bounce Rate)** : Plus le taux de rebond est bas, plus l'utilisateur est considéré engagé.
            - **Formule :**
                \nScore d'Engagement = (Pages Vues Moyennes) × (1 - Taux de Rebonds)
            
            **Interprétation du Score :**
            
            - Un score plus élevé indique un utilisateur fortement engagé, visitant plusieurs pages par session et ayant un faible taux de rebonds.
            - Un score faible peut indiquer un désintérêt ou une navigation rapide sans interaction.
            """)
    else:
        st.warning("Les colonnes nécessaires au calcul du score d'engagement sont manquantes.")

# Visualisation : Pages vues par session
if "session_id" in user_data.columns and "num_pageviews" in user_data.columns:
    # Ajouter une colonne d'index pour remplacer les session_id par des indices simples
    user_data = user_data.reset_index()
    user_data["session_index"] = user_data.index + 1  # Index commençant à 1

    # Création du graphique
    fig = px.bar(
        user_data,
        x="session_index",
        y="num_pageviews",
        title="Pages Vues par Session",
        labels={"session_index": "Session (Index)", "num_pageviews": "Pages Vues"},
    )
    fig.update_layout(
        xaxis=dict(
            tickmode="linear",  # Afficher tous les ticks de manière linéaire
            tick0=1,            # Premier tick commence à 1
            dtick=1,            # Écart d'unité entre chaque tick
            title="Sessions (Index)"
        ),
        yaxis=dict(title="Pages Vues")
    )
    st.plotly_chart(fig, use_container_width=True)

    # Ajout d'une explication sous le graphique
    st.markdown("""
    **Note :** L'axe X représente un index simplifié des sessions pour cet utilisateur. 
    Chaque valeur correspond à une session unique, numérotée dans l'ordre chronologique.
    """)



    # Visualisation : Activité horaire de l'utilisateur
    if "hour_x" in user_data.columns:
        fig_hour = px.histogram(
            user_data,
            x="hour_x",
            title="Distribution de l'Activité Horaire",
            labels={"hour_x": "Heure de la Journée"},
            nbins=24,
        )
        st.plotly_chart(fig_hour, use_container_width=True)

    # Visualisation : Moyenne des pages vues par canal
    if "medium" in user_data.columns and "num_pageviews" in user_data.columns:
        fig_medium = px.bar(
            user_data.groupby("medium", as_index=False)["num_pageviews"].mean(),
            x="medium",
            y="num_pageviews",
            title="Moyenne des Pages Vues par Canal",
            labels={"medium": "Canal", "num_pageviews": "Pages Vues Moyennes"},
        )
        st.plotly_chart(fig_medium, use_container_width=True)

    # Recommandations basées sur l'engagement
    st.markdown("### Recommandations Basées sur l'Engagement")
    if score_engagement < 10:
        st.warning(
            "L'engagement de cet utilisateur est faible. Envisagez des actions pour le réengager, "
            "comme des campagnes ciblées ou du contenu personnalisé."
        )
    else:
        st.success("L'utilisateur montre un bon engagement. Continuez à lui offrir du contenu pertinent.")
