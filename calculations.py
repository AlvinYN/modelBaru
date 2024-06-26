import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors

# Load dataset
dataset_path = "Cleaned_CombinedRecipe.csv"
dataset = pd.read_csv(dataset_path)

# Define allergy categories
allergy_categories = {
    "Nuts": ["Kacang tanah", "Peanuts", "Kacang almond", "Almonds", "Kacang mete", "Cashews", "Kacang pistachio", "Pistachios", "Kacang kenari", "Walnuts", "Kacang pecan", "Pecans", "Kacang pinus", "Pine nuts", "Kacang brazil", "Brazil nuts", "Kacang macadamia", "Macadamia nuts", "Kacang hazelnut", "Hazelnuts"],
    "Eggs": ["Telur ayam", "Chicken eggs", "Telur bebek", "Duck eggs", "Telur angsa", "Goose eggs", "Telur puyuh", "Quail eggs", "Telur orak-arik", "Scrambled eggs", "Telur rebus", "Boiled eggs", "Telor", "Fried eggs", "Telur ceplok", "Omelette", "Telur mata sapi", "Omelet", "Telur"],
    "Seafood": ["Salmon", "Tuna", "Cod", "Trout", "Mackerel", "Sarden", "Sardine", "Anchovy", "Haddock", "Herring", "Halibut", "Udang", "Shrimp", "Lobster", "Kepiting", "Crab", "Kerang", "Clams", "Tiram", "Oysters", "Cumi-cumi", "Squid", "Gurita", "Octopus", "Kerang Simping", "Scallops", "Kerang Hijau", "Mussels", "Kerang Abalon", "Abalone"]
}

# Function to check for allergies in a recipe
def check_allergies(ingredients, user_allergies):
    for allergy_category in user_allergies:
        allergy_list = allergy_categories.get(allergy_category, [])
        for item in allergy_list:
            if item.lower() in ingredients.lower():
                return True
    return False

# Function to calculate ideal body weight
def hitung_berat_badan_ideal(Tb):
    Bi = (Tb - 100) - (0.1 * (Tb - 100))
    return Bi

# Function to calculate basic calorie needs
def hitung_AKEi_umur(Bi, jenis_kelamin, umur):
    print(f"Calculating AKEi for Bi: {Bi}, gender: {jenis_kelamin}, age: {umur}")
    if 20 <= umur <= 29:
        if jenis_kelamin.lower() == "laki-laki":
            AKEi = (15.3 * Bi + 679) * 1.78
        elif jenis_kelamin.lower() == "perempuan":
            AKEi = (14.7 * Bi + 496) * 1.64
        else:
            print("Invalid gender")
            return "Jenis kelamin tidak valid"
    elif 30 <= umur <= 59:
        if jenis_kelamin.lower() == "laki-laki":
            AKEi = (11.6 * Bi + 879) * 1.78
        elif jenis_kelamin.lower() == "perempuan":
            AKEi = (8.7 * Bi + 829) * 1.64
        else:
            print("Invalid gender")
            return "Jenis kelamin tidak valid"
    elif umur >= 60:
        if jenis_kelamin.lower() == "laki-laki":
            AKEi = (13.5 * Bi + 487) * 1.78
        elif jenis_kelamin.lower() == "perempuan":
            AKEi = (13.5 * Bi + 596) * 1.64
        else:
            print("Invalid gender")
            return "Jenis kelamin tidak valid"
    else:
        print("Invalid age")
        return "Umur tidak valid"

    print(f"Calculated AKEi: {AKEi}")
    return AKEi


# Function to calculate the nutritional needs factor based on mealtime
def hitung_kebutuhan_faktor(meal_id):
    faktor_map = {1: 0.25, 2: 0.40, 3: 0.35}
    return faktor_map[meal_id]

# Function to calculate nutritional needs based on mealtime, diseases, and basic calorie intake
def hitung_kebutuhan_nutrisi(meal_id, AKEi, penyakit_input_list, jenis_kelamin):
    faktor = hitung_kebutuhan_faktor(meal_id)
    penyakit_input = set(penyakit_input_list)
    kebutuhan_kalori = protein = lemak = lemak_jenuh = lemak_tidak_jenuh_ganda = lemak_tidak_jenuh_tunggal = karbohidrat = kolesterol = gula = serat = garam = kalium = 0
 
    if {'Diabetes', 'Hipertensi', 'Kolesterol'}.issubset(penyakit_input):
        kebutuhan_kalori = faktor * AKEi
        protein = 0.8 * kebutuhan_kalori / 4
        lemak = 0.2 * kebutuhan_kalori / 9
        lemak_jenuh = 0.5 * lemak / 9
        lemak_tidak_jenuh_ganda = 0.1 * lemak
        lemak_tidak_jenuh_tunggal = lemak - lemak_jenuh - lemak_tidak_jenuh_ganda
        karbohidrat = 0.55 * kebutuhan_kalori / 4
        kolesterol = faktor * 200
        gula = 0.025 * kebutuhan_kalori
        serat = faktor * 12.5
        garam = faktor * 1500
        kalium = faktor * 3500
        return np.array([[kebutuhan_kalori, protein, lemak, lemak_jenuh, lemak_tidak_jenuh_ganda, lemak_tidak_jenuh_tunggal, karbohidrat, kolesterol, gula, serat, garam, kalium]])
    
    if {'Diabetes', 'Hipertensi'}.issubset(penyakit_input):
        kebutuhan_kalori = faktor * AKEi
        protein = 0.8 * kebutuhan_kalori / 4
        lemak = 0.225 * kebutuhan_kalori / 9
        lemak_jenuh = 0.05 * lemak / 9
        lemak_tidak_jenuh_ganda = 0.1 * lemak
        lemak_tidak_jenuh_tunggal = lemak - lemak_jenuh - lemak_tidak_jenuh_ganda
        karbohidrat = 0.55 * kebutuhan_kalori / 4
        kolesterol = faktor * 200
        gula = 0.025 * kebutuhan_kalori
        serat = faktor * 12.5
        garam = faktor * 1500
        kalium = faktor * 3500
        return np.array([[kebutuhan_kalori, protein, lemak, lemak_jenuh, lemak_tidak_jenuh_ganda, lemak_tidak_jenuh_tunggal, karbohidrat, kolesterol, gula, serat, garam, kalium]])
        
    if {'Diabetes', 'Kolesterol'}.issubset(penyakit_input):
        kebutuhan_kalori = faktor * AKEi
        protein = 0.8 * kebutuhan_kalori / 4
        lemak = 0.2 * kebutuhan_kalori / 9
        lemak_jenuh = 0.05 * lemak / 9
        lemak_tidak_jenuh_ganda = 0.1 * lemak
        lemak_tidak_jenuh_tunggal = lemak - lemak_jenuh - lemak_tidak_jenuh_ganda
        karbohidrat = 0.55 * kebutuhan_kalori / 4
        kolesterol = faktor * 200
        gula = 0.025 * kebutuhan_kalori
        serat = faktor * 12.5
        garam = faktor * 1500
        kalium = faktor * 3500
        return np.array([[kebutuhan_kalori, protein, lemak, lemak_jenuh, lemak_tidak_jenuh_ganda, lemak_tidak_jenuh_tunggal, karbohidrat, kolesterol, gula, serat, garam, kalium]])
        
    if {'Hipertensi', 'Kolesterol'}.issubset(penyakit_input):
        kebutuhan_kalori = faktor * AKEi
        protein = 0.8 * kebutuhan_kalori / 4
        lemak = 0.2 * kebutuhan_kalori / 9
        lemak_jenuh = 0.05 * lemak / 9
        lemak_tidak_jenuh_ganda = 0.1 * lemak
        lemak_tidak_jenuh_tunggal = lemak - lemak_jenuh - lemak_tidak_jenuh_ganda
        karbohidrat = 0.6 * kebutuhan_kalori / 4
        kolesterol = faktor * 200
        gula = 0.025 * kebutuhan_kalori
        serat = faktor * 12.5
        garam = faktor * 2400
        kalium = faktor * 3500
        return np.array([[kebutuhan_kalori, protein, lemak, lemak_jenuh, lemak_tidak_jenuh_ganda, lemak_tidak_jenuh_tunggal, karbohidrat, kolesterol, gula, serat, garam, kalium]])
    
    if 'Diabetes' in penyakit_input:
        kebutuhan_kalori = faktor * AKEi
        protein = 0.125 * kebutuhan_kalori / 4
        lemak = 0.225 * kebutuhan_kalori / 9
        lemak_jenuh = 0.05 * lemak / 9
        lemak_tidak_jenuh_ganda = 0.1 * lemak
        lemak_tidak_jenuh_tunggal = lemak - lemak_jenuh - lemak_tidak_jenuh_ganda
        karbohidrat = 0.65 * kebutuhan_kalori / 4
        kolesterol = faktor * 300
        gula = 0.025 * kebutuhan_kalori
        serat = faktor * 25
        garam = faktor * 3000
        kalium = faktor * 3500
    elif 'Hipertensi' in penyakit_input:
        kebutuhan_kalori = faktor * AKEi
        protein = 0.8 * kebutuhan_kalori / 4
        lemak = 0.25 * kebutuhan_kalori / 9
        lemak_jenuh = 0.07 * kebutuhan_kalori / 9
        lemak_tidak_jenuh_ganda = 0.1 * lemak
        lemak_tidak_jenuh_tunggal = lemak - lemak_jenuh - lemak_tidak_jenuh_ganda
        karbohidrat = 0.625 * kebutuhan_kalori / 4
        kolesterol = faktor * 300
        gula = 0.025 * kebutuhan_kalori
        serat = faktor * 12.5
        garam = faktor * 2400
        kalium = faktor * 3500
    elif 'Kolesterol' in penyakit_input:
        kebutuhan_kalori = faktor * AKEi
        protein = 0.8 * kebutuhan_kalori / 4
        karbohidrat = 0.65 * kebutuhan_kalori / 4
        lemak = 0.225 * kebutuhan_kalori / 9
        lemak_jenuh = 0.07 * kebutuhan_kalori / 9
        lemak_tidak_jenuh_ganda = 0.1 * lemak
        lemak_tidak_jenuh_tunggal = lemak - lemak_jenuh - lemak_tidak_jenuh_ganda
        kolesterol = faktor * 200
        gula = 0.025 * kebutuhan_kalori
        if jenis_kelamin.lower() == 'laki-laki':
            serat = faktor * 38
        elif jenis_kelamin.lower() == 'perempuan':
            serat = faktor * 25
        else:
           raise ValueError("Jenis kelamin tidak valid") 
        garam = faktor * 2400
        kalium = faktor * 3500
    else:
        return ValueError("Penyakit tidak valid")
    
    return np.array([[kebutuhan_kalori, protein, lemak, lemak_jenuh, lemak_tidak_jenuh_ganda, lemak_tidak_jenuh_tunggal, karbohidrat, kolesterol, gula, serat, garam, kalium]])

def rekomendasi_makanan(dataset_mealtime, nutrisi_dibutuhkan, user_allergies):
    # Mengambil fitur nutrisi dari subset dataset
    nutrisi_columns = ['Energi (kkal)', 'Protein (g)', 'Lemak (g)', 'Lemak Jenuh (g)', 'Lemak tak Jenuh Ganda (g)', 'Lemak tak Jenuh Tunggal (g)', 'Karbohidrat (g)', 'Kolesterol (mg)', 'Gula (g)', 'Serat (g)', 'Sodium (mg)', 'Kalium (mg)']
    
    if not all(col in dataset_mealtime.columns for col in nutrisi_columns):
        raise ValueError(f"Dataset tidak memiliki kolom nutrisi yang diperlukan: {nutrisi_columns}")

    X_mealtime = dataset_mealtime[nutrisi_columns]
    
    # Menskalakan fitur
    scaler = MinMaxScaler()
    X_mealtime_scaled = scaler.fit_transform(X_mealtime)
    
    # Membuat DataFrame untuk input nutrisi yang dibutuhkan dengan nama kolom yang sesuai
    nutrisi_dibutuhkan_df = pd.DataFrame(nutrisi_dibutuhkan, columns=nutrisi_columns)
    
    # Menskalakan nutrisi yang dibutuhkan
    nutrisi_dibutuhkan_scaled = scaler.transform(nutrisi_dibutuhkan_df)

    # Tentukan n_neighbors secara dinamis berdasarkan ukuran dataset
    n_neighbors = min(100, len(dataset_mealtime))

    # Menggunakan k-NN untuk mencari n_neighbors terdekat
    knn = NearestNeighbors(n_neighbors=n_neighbors)
    knn.fit(X_mealtime_scaled)
    distances, indices = knn.kneighbors(nutrisi_dibutuhkan_scaled)

    rekomendasi = dataset_mealtime.iloc[indices[0]]
    
    # Debugging untuk melihat hasil k-NN sebelum filter
    print(f"Rekomendasi awal dari k-NN: {len(rekomendasi)} resep")
    print(rekomendasi[['Recipe ID', 'Nama Resep', 'Meal ID', 'Ingredients']])
    
    rekomendasi_filtered = rekomendasi[~rekomendasi['Ingredients'].apply(check_allergies, user_allergies=user_allergies)]
    
    # Debugging untuk melihat hasil filter alergi
    print(f"Rekomendasi setelah filter alergi: {len(rekomendasi_filtered)} resep")
    print(rekomendasi_filtered[['Recipe ID', 'Nama Resep', 'Meal ID', 'Ingredients']])
    
    return rekomendasi_filtered
