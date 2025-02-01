import streamlit as st

# Configuration de la page
st.set_page_config(page_title="Accueil - Dashboard Engagement des Contributeurs", layout="wide")

# Styles CSS personnalisés
st.markdown(
    """
    <style>
    .header {
        background-color: #7F8C8D; /* Gris */
        padding: 10px;
        border-radius: 5px;
        color: white;
        text-align: center;
    }
    .section {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .button {
        background-color: #7F8C8D; /* Gris */
        color: white;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    .button:hover {
        background-color: #5D6D7E; /* Gris plus foncé au survol */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Titre principal avec style
st.markdown("""
    <div class="header">
        <h1>Bienvenue sur le Dashboard : Engagement des Contributeurs !</h1>
    </div>
    """, unsafe_allow_html=True)

# Description du projet dans une section stylisée
st.markdown("""
    <div class="section">
        <h2>À propos de ce projet</h2>
        <p>
            Ce <strong>dashboard interactif</strong> a été conçu pour analyser et améliorer <strong>l'engagement des contributeurs</strong> sur la plateforme
            <strong>Management & Data Science</strong>. Il permet de visualiser des indicateurs clés et de fournir des recommandations
            pour accroître la participation et optimiser l'expérience utilisateur.
        </p>
        <h3>Fonctionnalités principales</h3>
        <ul>
            <li><strong>Dashboard KPI</strong> : Indicateurs comme les pages vues moyennes, le taux de rebond, les sessions par canal et l'heure de pic d'activité.</li>
            <li><strong>Analyse par utilisateur</strong> : Découvrez les caractéristiques spécifiques d'un utilisateur et calculez un score d'engagement détaillé.</li>
            <li><strong>Visualisations détaillées</strong> : Graphiques interactifs pour explorer l'activité des visiteurs, les canaux performants et les heures d'engagement.</li>
            <li><strong>Recommandations</strong> : Propositions pour maximiser l'engagement des utilisateurs et améliorer l'expérience globale.</li>
        </ul>
        <h3>Objectifs du Dashboard</h3>
        <p>
            Ce dashboard aide les gestionnaires et analystes à identifier les <strong>facteurs clés d'engagement</strong>, à évaluer les performances des canaux 
            et à optimiser les stratégies pour améliorer la fidélisation et la satisfaction des contributeurs.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Boutons d'accès aux différentes pages
st.markdown("""
    <div style="text-align: center; margin-top: 20px;">
        <a href="/pages/1_Dashboard" class="button">📊 Accéder au Dashboard KPI</a>
        <a href="/pages/User_Analysis" class="button" style="margin-left: 10px;">👤 Analyse par Utilisateur</a>
    </div>
    """, unsafe_allow_html=True)

# Critères d'un bon dashboard
st.markdown("""
    <div class="section">
        <h2>Critères d'un Bon Dashboard</h2>
        <p>
            Ce dashboard respecte les <strong>principes d'accessibilité et de lisibilité</strong> pour garantir une expérience utilisateur optimale :
        </p>
        <ol>
            <li><strong>Clarté des Indicateurs</strong> : Présentation des données sous forme de KPI et graphiques interactifs pour une interprétation rapide.</li>
            <li><strong>Accessibilité</strong> : Design intuitif avec un contraste élevé et des options interactives.</li>
            <li><strong>Interactivité</strong> : Possibilité de filtrer et d'explorer les données en temps réel.</li>
            <li><strong>Recommandations Contextuelles</strong> : Suggestions basées sur les données pour améliorer les performances.</li>
            <li><strong>Navigation Simplifiée</strong> : Accès facile aux différentes sections via la barre latérale.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

# Section Footer
st.markdown("""
    ---
    <div style="text-align: center; color: gray;">
        **Source** : Analyse des données de navigation sur la plateforme Management & Data Science.
    </div>
    """, unsafe_allow_html=True)
