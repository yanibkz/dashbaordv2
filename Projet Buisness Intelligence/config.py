import streamlit as st
from sqlalchemy import create_engine

# Récupérer DATABASE_URL depuis les secrets de Streamlit
DATABASE_URL = st.secrets["DATABASE_URL"]

# Configurer la connexion à PostgreSQL
engine = create_engine(DATABASE_URL)
