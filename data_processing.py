import pandas as pd
import os

def get_product_data(category_path, filters=None):
    """
    Lit les données d'un fichier Excel et retourne un DataFrame, avec filtrage optionnel.
    """
    try:
        df = pd.read_excel(category_path)
        
        if filters:
            for column, value in filters.items():
                if column in df.columns:
                    df = df[df[column].astype(str).str.contains(str(value), case=False, na=False)]
        return df
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier {category_path}: {e}")
        return None

def get_all_categories(base_path):
    """
    Parcourt le répertoire de base et retourne une structure de catégories/sous-catégories.
    """
    categories = {}
    for root, dirs, files in os.walk(base_path):
        # Ignorer les répertoires vides
        if not dirs and not files:
            continue

        # Obtenir le chemin relatif à la base_path
        relative_path = os.path.relpath(root, base_path)
        path_parts = relative_path.split(os.sep)

        current_level = categories
        for part in path_parts:
            if part == ".": # Pour le répertoire de base lui-même
                continue
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]

        # Ajouter les fichiers Excel trouvés à la catégorie la plus profonde
        for f in files:
            if f.endswith(".xlsx"):
                product_name = os.path.splitext(f)[0]
                if "products" not in current_level:
                    current_level["products"] = []
                current_level["products"].append({
                    "name": product_name,
                    "path": os.path.join(root, f)
                })
    return categories


# Exemple d'utilisation (pour les tests)
if __name__ == '__main__':
    # Créez un exemple de structure de fichiers pour tester
    os.makedirs('data/Assurance/Auto', exist_ok=True)
    os.makedirs('data/Manufacturing/Alimentaire/Generale', exist_ok=True)

    # Créez des fichiers Excel factices
    df_auto = pd.DataFrame({'Date': pd.to_datetime(['2023-01-01', '2023-01-02']), 'Prix': [100, 105]})
    df_auto.to_excel('data/Assurance/Auto/prime_assurance.xlsx', index=False)

    df_lait = pd.DataFrame({'Date': pd.to_datetime(['2023-01-01', '2023-01-02']), 'Prix': [1.2, 1.25]})
    df_lait.to_excel('data/Manufacturing/Alimentaire/Generale/lait.xlsx', index=False)

    base_data_path = 'data'
    all_categories = get_all_categories(base_data_path)
    print("Structure des catégories:")
    print(all_categories)

    # Test de lecture d'un fichier spécifique
    if 'Manufacturing' in all_categories and \
       'Alimentaire' in all_categories['Manufacturing'] and \
       'Generale' in all_categories['Manufacturing']['Alimentaire'] and \
       'products' in all_categories['Manufacturing']['Alimentaire']['Generale']:

        lait_path = None
        for product in all_categories['Manufacturing']['Alimentaire']['Generale']['products']:
            if product['name'] == 'lait':
                lait_path = product['path']
                break

        if lait_path:
            print(f"\nDonnées pour le lait ({lait_path}):")
            df_lait_data = get_product_data(lait_path)
            print(df_lait_data)

            # Test avec filtre
            print(f"\nDonnées pour le lait (filtré par Prix > 1.2):")
            df_lait_filtered = get_product_data(lait_path, filters={'Prix': 1.2})
            print(df_lait_filtered)
        else:
            print("Fichier 'lait.xlsx' non trouvé dans la structure.")
    else:
        print("Chemin 'Manufacturing/Alimentaire/Generale' ou 'products' non trouvé dans la structure.")


