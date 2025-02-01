import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Récupérer l'URL de connexion PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")

# Vérifier que la connexion est bien récupérée
if DATABASE_URL is None:
    raise ValueError("❌ ERREUR : La variable d'environnement DATABASE_URL est introuvable. Vérifie ton fichier .env !")