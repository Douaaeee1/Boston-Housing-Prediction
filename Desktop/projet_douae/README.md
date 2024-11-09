
# Boston Housing Prediction

Ce projet permet de prédire le prix des logements dans la région de Boston en utilisant un modèle d'apprentissage automatique. L'application Flask permet de soumettre des données sur les caractéristiques d'une maison et de recevoir une prédiction du prix.

## Prérequis

Avant de tester ou de déployer l'application, vous devez avoir les outils suivants installés :

- [Python 3.x](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/products/docker-desktop) (si vous voulez tester avec Docker)
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) (pour déployer sur Google Cloud)
- Un compte Google Cloud avec **facturation activée** et **Google Cloud Run** activé.

## Installation et configuration

### 1. Cloner le dépôt

Clonez le dépôt du projet sur votre machine locale.

```bash
git clone https://github.com/username/boston-housing-prediction.git
cd boston-housing-prediction
```

### 2. Créer un environnement virtuel (optionnel mais recommandé)

```bash
python -m venv .venv
source .venv/bin/activate  # Sur macOS/Linux
.venv\Scripts\activate     # Sur Windows
```

### 3. Installer les dépendances

Installez les dépendances nécessaires via `pip` :

```bash
pip install -r requirements.txt
```

### 4. Démarrer l'application en local

Lancez l'application Flask sur votre machine locale pour tester l'application avant le déploiement.

```bash
python app.py
```

L'application sera disponible à l'adresse suivante : `http://localhost:8080`

Vous pouvez accéder à l'endpoint `/predict` en envoyant une requête `POST` avec des données JSON. L'endpoint `/health` peut être utilisé pour vérifier que l'application fonctionne correctement.

### Exemple de requête cURL pour tester la prédiction :

```bash
curl -X POST http://localhost:8080/predict -H "Content-Type: application/json" -d '{
    "ZN": 0.0, "INDUS": 6.0, "CHAS": 0, "NOX": 0.5, "RM": 6.5, "AGE": 65.0, 
    "DIS": 4.0, "TAX": 300.0, "PTRATIO": 15.0, "B": 380.0, "LSTAT": 12.0
}'
```

Vous devriez obtenir une réponse contenant le prix prédit de la maison, par exemple :

```json
{
  "prediction": 24.65
}
```  

## Déploiement sur Google Cloud Run

### 1. Se connecter à Google Cloud

Connectez-vous à votre compte Google Cloud avec le SDK :

```bash
gcloud auth login
```

### 2. Sélectionner le projet Google Cloud

Si vous avez plusieurs projets Google Cloud, sélectionnez celui que vous voulez utiliser pour le déploiement :

```bash
gcloud config set project boston-prediction-project
```

### 3. Activer les services Google Cloud nécessaires

Assurez-vous que les services requis sont activés :

```bash
gcloud services enable containerregistry.googleapis.com
gcloud services enable run.googleapis.com
```

### 4. Construire l'image Docker

Si vous n'avez pas encore construit l'image Docker, construisez-la maintenant :

```bash
docker build -t gcr.io/boston-prediction-project/bostonprediction .
```

### 5. Pousser l'image vers Google Container Registry

Poussez l'image construite vers le Google Container Registry (GCR) :

```bash
docker push gcr.io/boston-prediction-project/bostonprediction
```

### 6. Déployer sur Google Cloud Run

Déployez l'image sur Google Cloud Run. Vous devez spécifier un nom pour votre service :

```bash
gcloud run deploy boston-housing-app --image gcr.io/boston-prediction-project/bostonprediction --platform managed --port 8080
```

Lorsque vous y êtes invité, choisissez les options suivantes :
- **Public** : Si vous souhaitez rendre votre application accessible à tous.
- **Port** : Le port par défaut est `8080`, assurez-vous que votre application écoute sur ce port.

### 7. Accéder à l'application déployée

Une fois le déploiement terminé, Google Cloud Run vous fournira un URL public. Vous pouvez accéder à l'application à partir de cette URL.

---

## Structure du projet

Voici la structure des fichiers du projet :

```
boston-housing-prediction/
│
├── app.py                # Code de l'application Flask
├── Dockerfile            # Dockerfile pour créer l'image
├── requirements.txt      # Liste des dépendances Python
├── artefacts/            # Dossier contenant les artefacts du modèle (model.pkl, scaler.pkl, etc.)
├── templates/            # Fichiers HTML (interface utilisateur)
│   └── index.html        # Page d'interface utilisateur pour entrer les données
└── README.md             # Documentation du projet
```

---

## Technologies utilisées

- **Flask** : Framework web Python utilisé pour créer l'application.
- **Scikit-learn** : Pour le modèle d'apprentissage automatique.
- **Docker** : Pour créer des images conteneurisées de l'application.
- **Google Cloud Run** : Pour déployer l'application sur Google Cloud.

---

## Contribuer

Si vous souhaitez contribuer à ce projet, vous pouvez créer une branche, faire vos modifications et soumettre une pull request. Nous serons ravis d'examiner vos contributions.
