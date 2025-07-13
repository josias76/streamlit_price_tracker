# Application de Suivi des Prix - Version Streamlit

## Description

Cette application Streamlit permet de suivre et d'analyser l'évolution des prix de différents produits organisés par catégories et sous-catégories. Elle offre une interface utilisateur moderne et interactive pour visualiser les données de prix avec des fonctionnalités de filtrage avancées.

## Fonctionnalités

### 🔍 **Filtrage Avancé**
- Filtres par marque, type, gramage, origine, format
- Filtres par plage de prix (minimum/maximum)
- Combinaison de plusieurs filtres simultanément
- Interface intuitive avec sélecteurs déroulants

### 📊 **Visualisations Interactives**
- Graphiques de l'évolution des prix dans le temps
- Graphiques interactifs avec Plotly
- Tooltips détaillés au survol
- Zoom et navigation dans les graphiques

### 📈 **Statistiques**
- Prix moyen, minimum et maximum
- Nombre total d'entrées
- Statistiques mises à jour en temps réel selon les filtres

### 📋 **Tableau de Données**
- Affichage des données filtrées
- Tri par colonnes
- Interface responsive

## Structure des Données

L'application attend une structure de fichiers Excel organisée comme suit :

```
data/
├── CATEGORIE/
│   ├── SOUS_CATEGORIE/
│   │   ├── SOUS_SOUS_CATEGORIE/
│   │   │   └── produit.xlsx
```

### Format des Fichiers Excel

Chaque fichier Excel doit contenir les colonnes suivantes :
- **marque** : Marque du produit
- **type** : Type/variété du produit
- **gramage** : Poids ou quantité
- **prix** : Prix en euros
- **origine** : Pays ou région d'origine
- **date** : Date de relevé des prix
- **format** : Format d'emballage

## Installation

### Prérequis
- Python 3.7 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation des dépendances

```bash
pip install streamlit pandas openpyxl plotly
```

## Utilisation

### Démarrage de l'application

```bash
cd streamlit_price_tracker
streamlit run app.py
```

L'application sera accessible à l'adresse : `http://localhost:8501`

### Navigation

1. **Sélection du produit** : Utilisez le sélecteur dans la barre latérale pour choisir un produit
2. **Application des filtres** : Utilisez les filtres pour affiner les données affichées
3. **Analyse des données** : Consultez les statistiques, graphiques et tableau de données

## Structure du Projet

```
streamlit_price_tracker/
├── app.py                 # Application principale Streamlit
├── data_processing.py     # Fonctions de traitement des données
├── data/                  # Dossier contenant les fichiers de données
├── README.md             # Documentation
└── requirements.txt      # Dépendances Python
```

## Fonctionnalités Techniques

### Cache des Données
- Utilisation du cache Streamlit pour optimiser les performances
- Rechargement automatique lors de modifications des données

### Interface Responsive
- Design adaptatif pour différentes tailles d'écran
- Interface optimisée pour desktop et mobile

### Gestion d'Erreurs
- Messages d'erreur informatifs
- Gestion des fichiers manquants
- Validation des données d'entrée

## Personnalisation

### Ajout de Nouveaux Produits
1. Placez le fichier Excel dans la structure de dossiers appropriée
2. Redémarrez l'application
3. Le nouveau produit apparaîtra automatiquement dans le sélecteur

### Modification des Filtres
Les filtres peuvent être personnalisés en modifiant le fichier `app.py` dans la section des filtres.

## Dépannage

### Problèmes Courants

**L'application ne démarre pas :**
- Vérifiez que toutes les dépendances sont installées
- Assurez-vous d'être dans le bon répertoire

**Données non affichées :**
- Vérifiez que les fichiers Excel sont dans la bonne structure de dossiers
- Vérifiez que les colonnes requises sont présentes dans les fichiers

**Erreurs de chargement :**
- Vérifiez le format des fichiers Excel
- Assurez-vous que les données sont dans le bon format

## Support

Pour toute question ou problème, consultez les logs de l'application dans le terminal où Streamlit est exécuté.

## Version

Version 1.0 - Application Streamlit de suivi des prix avec filtrage avancé et graphiques interactifs.

---

*Application développée avec Streamlit, Pandas et Plotly*

