import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from data_processing import get_all_categories, get_product_data
import numpy as np
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="Tableau de Bord - Suivi des Prix",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour améliorer l'apparence
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    .filter-section {
        background: #f8f9ff;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .stSelectbox > div > div {
        background-color: white;
    }
</style>
""", unsafe_allow_html=True)

# Titre principal
st.markdown("""
<div class="main-header">
    <h1>📊 Tableau de Bord - Suivi des Prix</h1>
    <p>Suivez l'évolution des prix par catégorie et sous-catégorie</p>
</div>
""", unsafe_allow_html=True)

# Initialisation des variables de session
if 'selected_product' not in st.session_state:
    st.session_state.selected_product = None
if 'filtered_data' not in st.session_state:
    st.session_state.filtered_data = None

# Sidebar pour la navigation
st.sidebar.title("🗂️ Navigation")

# Chargement des catégories
@st.cache_data
def load_categories():
    try:
        base_path = os.path.join(os.path.dirname(__file__), "data")
        return get_all_categories(base_path)
    except Exception as e:
        st.error(f"Erreur lors du chargement des catégories: {e}")
        return {}

categories = load_categories()

# Sélection des catégories dans la sidebar
if categories:
    # Créer une liste simple des fichiers Excel disponibles
    products_list = ["MANUFACTURING/MANUFACTURING_ALIMENTAIRE/ALIMENTAIRE_GENERALE/riz.xlsx"]
    
    # Sélecteur de produit
    selected_product = st.sidebar.selectbox(
        "Sélectionnez un produit:",
        [""] + products_list,
        index=0
    )
    
    if selected_product:
        st.session_state.selected_product = selected_product

# Section principale
if st.session_state.selected_product:
    # Chargement des données du produit
    @st.cache_data
    def load_product_data(product_path):
        try:
            base_path = os.path.join(os.path.dirname(__file__), "data")
            full_path = os.path.join(base_path, product_path)
            
            st.write(f"Debug: Tentative de chargement de {full_path}")
            
            if os.path.exists(full_path):
                return get_product_data(full_path)
            else:
                st.error(f"Fichier non trouvé: {full_path}")
                return None
        except Exception as e:
            st.error(f"Erreur lors du chargement des données: {e}")
            return None
    
    data = load_product_data(st.session_state.selected_product)
    
    if data is not None and not data.empty:
        # Section de filtrage
        st.markdown("### 🔍 Filtres")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            marques = ["Toutes"] + sorted(data['marque'].dropna().unique().tolist())
            selected_marque = st.selectbox("Marque:", marques)
        
        with col2:
            types = ["Tous"] + sorted(data['type'].dropna().unique().tolist())
            selected_type = st.selectbox("Type:", types)
        
        with col3:
            gramages = ["Tous"] + sorted(data['gramage'].dropna().unique().tolist())
            selected_gramage = st.selectbox("Gramage:", gramages)
        
        with col4:
            origines = ["Toutes"] + sorted(data['origine'].dropna().unique().tolist())
            selected_origine = st.selectbox("Origine:", origines)
        
        # Filtres de prix
        col5, col6 = st.columns(2)
        with col5:
            prix_min = st.number_input("Prix minimum (€):", min_value=0.0, value=0.0, step=0.1)
        with col6:
            prix_max = st.number_input("Prix maximum (€):", min_value=0.0, value=float(data['prix'].max()), step=0.1)
        
        # Application des filtres
        filtered_data = data.copy()
        
        if selected_marque != "Toutes":
            filtered_data = filtered_data[filtered_data['marque'] == selected_marque]
        if selected_type != "Tous":
            filtered_data = filtered_data[filtered_data['type'] == selected_type]
        if selected_gramage != "Tous":
            filtered_data = filtered_data[filtered_data['gramage'] == selected_gramage]
        if selected_origine != "Toutes":
            filtered_data = filtered_data[filtered_data['origine'] == selected_origine]
        
        filtered_data = filtered_data[
            (filtered_data['prix'] >= prix_min) & 
            (filtered_data['prix'] <= prix_max)
        ]
        
        st.session_state.filtered_data = filtered_data
        
        # Affichage des métriques
        if not filtered_data.empty:
            st.markdown("### 📈 Statistiques")
            
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("Nombre d'entrées", len(filtered_data))
            
            with col2:
                st.metric("Prix moyen", f"{filtered_data['prix'].mean():.2f} €")
            
            with col3:
                st.metric("Prix minimum", f"{filtered_data['prix'].min():.2f} €")
            
            with col4:
                st.metric("Prix maximum", f"{filtered_data['prix'].max():.2f} €")
            
            with col5:
                if len(filtered_data) > 1:
                    prix_initial = filtered_data['prix'].iloc[0]
                    prix_final = filtered_data['prix'].iloc[-1]
                    evolution = ((prix_final - prix_initial) / prix_initial) * 100
                    st.metric("Évolution", f"{evolution:.1f}%", delta=f"{evolution:.1f}%")
                else:
                    st.metric("Évolution", "N/A")
            
            # Graphique interactif
            st.markdown("### 📊 Évolution des Prix")
            
            # Options de graphique
            chart_type = st.radio(
                "Type de graphique:",
                ["Ligne", "Points", "Ligne + Points", "Histogramme"],
                horizontal=True
            )
            
            # Conversion de la colonne date
            if 'date' in filtered_data.columns:
                filtered_data['date'] = pd.to_datetime(filtered_data['date'])
                filtered_data = filtered_data.sort_values('date')
            
            if chart_type in ["Ligne", "Points", "Ligne + Points"]:
                fig = go.Figure()
                
                mode = "lines" if chart_type == "Ligne" else "markers" if chart_type == "Points" else "lines+markers"
                
                fig.add_trace(go.Scatter(
                    x=filtered_data['date'],
                    y=filtered_data['prix'],
                    mode=mode,
                    name='Prix',
                    line=dict(color='#667eea', width=3),
                    marker=dict(
                        color='#667eea',
                        size=8,
                        line=dict(color='white', width=2)
                    ),
                    hovertemplate=
                        '<b>Date:</b> %{x}<br>' +
                        '<b>Prix:</b> %{y:.2f} €<br>' +
                        '<b>Marque:</b> %{customdata[0]}<br>' +
                        '<b>Type:</b> %{customdata[1]}<br>' +
                        '<b>Origine:</b> %{customdata[2]}<br>' +
                        '<b>Gramage:</b> %{customdata[3]}<br>' +
                        '<extra></extra>',
                    customdata=filtered_data[['marque', 'type', 'origine', 'gramage']].values
                ))
                
                # Ligne de tendance optionnelle
                if st.checkbox("Afficher la ligne de tendance"):
                    if len(filtered_data) > 1:
                        x_numeric = pd.to_numeric(filtered_data['date'])
                        z = np.polyfit(x_numeric, filtered_data['prix'], 1)
                        p = np.poly1d(z)
                        
                        fig.add_trace(go.Scatter(
                            x=filtered_data['date'],
                            y=p(x_numeric),
                            mode='lines',
                            name='Tendance',
                            line=dict(color='red', width=2, dash='dash')
                        ))
                
                fig.update_layout(
                    title="Évolution des Prix dans le Temps",
                    xaxis_title="Date",
                    yaxis_title="Prix (€)",
                    hovermode='closest',
                    height=500,
                    showlegend=True
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
            elif chart_type == "Histogramme":
                fig = px.histogram(
                    filtered_data, 
                    x='prix', 
                    nbins=20,
                    title="Distribution des Prix",
                    color_discrete_sequence=['#667eea']
                )
                fig.update_layout(
                    xaxis_title="Prix (€)",
                    yaxis_title="Fréquence",
                    height=500
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Graphiques supplémentaires
            st.markdown("### 📊 Analyses Complémentaires")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Graphique par marque
                if len(filtered_data['marque'].unique()) > 1:
                    fig_marque = px.box(
                        filtered_data, 
                        x='marque', 
                        y='prix',
                        title="Distribution des Prix par Marque",
                        color_discrete_sequence=['#667eea']
                    )
                    fig_marque.update_layout(height=400)
                    st.plotly_chart(fig_marque, use_container_width=True)
            
            with col2:
                # Graphique par origine
                if len(filtered_data['origine'].unique()) > 1:
                    fig_origine = px.box(
                        filtered_data, 
                        x='origine', 
                        y='prix',
                        title="Distribution des Prix par Origine",
                        color_discrete_sequence=['#764ba2']
                    )
                    fig_origine.update_layout(height=400)
                    st.plotly_chart(fig_origine, use_container_width=True)
            
            # Tableau des données
            st.markdown("### 📋 Données Détaillées")
            
            # Options d'affichage du tableau
            show_all = st.checkbox("Afficher toutes les données", value=False)
            
            if show_all:
                st.dataframe(filtered_data, use_container_width=True)
            else:
                st.dataframe(filtered_data.head(20), use_container_width=True)
                if len(filtered_data) > 20:
                    st.info(f"Affichage des 20 premières entrées sur {len(filtered_data)} au total.")
            
            # Bouton de téléchargement
            csv = filtered_data.to_csv(index=False)
            st.download_button(
                label="📥 Télécharger les données (CSV)",
                data=csv,
                file_name=f"donnees_prix_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
            
        else:
            st.warning("Aucune donnée ne correspond aux filtres sélectionnés.")
    
    else:
        st.error("Impossible de charger les données du produit sélectionné.")

else:
    # Page d'accueil
    st.markdown("### 🏠 Bienvenue")
    st.info("Sélectionnez un produit dans la barre latérale pour commencer l'analyse des prix.")
    
    # Affichage de la structure des catégories
    if categories:
        st.markdown("### 📁 Catégories Disponibles")
        
        for category, subcategories in categories.items():
            with st.expander(f"📂 {category}"):
                if isinstance(subcategories, dict):
                    for subcategory, items in subcategories.items():
                        st.write(f"📁 **{subcategory}**")
                        if isinstance(items, dict):
                            for subsubcat, files in items.items():
                                st.write(f"  📁 {subsubcat}")
                                if isinstance(files, list):
                                    for file in files:
                                        st.write(f"    📄 {file}")
                        else:
                            if isinstance(items, list):
                                for item in items:
                                    st.write(f"  📄 {item}")

# Footer
st.markdown("---")
st.markdown("*Application de suivi des prix développée avec Streamlit*")

