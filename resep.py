from flask import Flask, request, jsonify
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)

# Load the kNN model and scaler
with open('C:\\Users\\aallv\\Documents\\Project TA\\Model-Model-Model\\knn_model.pkl', 'rb') as model_file:
    knn = pickle.load(model_file)

with open('C:\\Users\\aallv\\Documents\\Project TA\\Model-Model-Model\\scaler.pkl', 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)
    
# Fungsi untuk menghitung berat badan ideal
def hitung_berat_badan_ideal(Tb):
    return (Tb - 100) - (0.1 * (Tb - 100))

# Fungsi untuk menghitung kebutuhan kalori dasar
def hitung_AKEi_umur(Bi, jenis_kelamin, umur):
    if 20 <= umur <= 29:
        AKEi = (15.3 * Bi + 679) * 1.78 if jenis_kelamin.lower() == 'pria' else (14.7 * Bi + 496) * 1.64
    elif 30 <= umur <= 59:
        AKEi = (11.6 * Bi + 879) * 1.78 if jenis_kelamin.lower() == 'pria' else (8.7 * Bi + 829) * 1.64
    elif umur >= 60:
        AKEi = (13.5 * Bi + 487) * 1.78 if jenis_kelamin.lower() == 'pria' else (13.5 * Bi + 596) * 1.64
    return AKEi

# Fungsi untuk menghitung faktor kebutuhan nutrisi berdasarkan mealtime
def hitung_kebutuhan_faktor(meal_id):
    faktor_map = {'sarapan': 0.25, 'makan siang': 0.40, 'makan malam': 0.35}
    return faktor_map[meal_id]

def hitung_kebutuhan_nutrisi(mealtime, AKEi, penyakit_input_list, jenis_kelamin, alergi):
    faktor = hitung_kebutuhan_faktor(mealtime)
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
        print("Ini ketiga penyakit disatukan")
        # Kondisi untuk diabetes, hipertensi, dan kolesterol bersamaan
        return np.array([[kebutuhan_kalori, protein, lemak, lemak_jenuh, lemak_tidak_jenuh_ganda, lemak_tidak_jenuh_tunggal, karbohidrat, kolesterol, gula, serat, garam, kalium]])
    
    if {'Diabetes', 'Hipertensi'}.issubset(penyakit_input):
        # Kondisi untuk diabetes dan hipertensi
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
        print("Ini diabetes dan hipertensi")
        return np.array([[kebutuhan_kalori, protein, lemak, lemak_jenuh, lemak_tidak_jenuh_ganda, lemak_tidak_jenuh_tunggal, karbohidrat, kolesterol, gula, serat, garam, kalium]])
        
    if {'Diabetes', 'Kolesterol'}.issubset(penyakit_input):
        # Kondisi untuk diabetes dan kolesterol
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
        print("Ini diabetes dan kolesterol")
        return np.array([[kebutuhan_kalori, protein, lemak, lemak_jenuh, lemak_tidak_jenuh_ganda, lemak_tidak_jenuh_tunggal, karbohidrat, kolesterol, gula, serat, garam, kalium]])
        
    if {'Hipertensi', 'Kolesterol'}.issubset(penyakit_input):
        # Kondisi untuk hipertensi dan kolesterol
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
        print("Ini hipertensi dan kolesterol")
        return np.array([[kebutuhan_kalori, protein, lemak, lemak_jenuh, lemak_tidak_jenuh_ganda, lemak_tidak_jenuh_tunggal, karbohidrat, kolesterol, gula, serat, garam, kalium]])
    
    if 'Diabetes' in penyakit_input:
        kebutuhan_kalori = faktor * AKEi
        protein = 0.125 * kebutuhan_kalori / 4
        lemak = 0.225 * kebutuhan_kalori / 9
        lemak_jenuh = 0.05 * lemak / 9
        lemak_tidak_jenuh_ganda = 0.1 * lemak
        lemak_tidak_jenuh_tunggal = lemak - lemak_jenuh - lemak_tidak_jenuh_ganda
        karbohidrat = 0.65 * kebutuhan_kalori / 4
        kolesterol = faktor * 150
        gula = 0.025 * kebutuhan_kalori
        serat = faktor * 12.5
        garam = faktor * 1500
        kalium = faktor * 3500
        print("Ini diabetes")
    elif 'Hipertensi' in penyakit_input:
        kebutuhan_kalori = faktor * AKEi
        protein = 0.8 * kebutuhan_kalori / 4
        lemak = 0.25 * kebutuhan_kalori / 9
        lemak_jenuh = 0.07 * kebutuhan_kalori / 9
        lemak_tidak_jenuh_ganda = 0.1 * lemak
        lemak_tidak_jenuh_tunggal = lemak - lemak_jenuh - lemak_tidak_jenuh_ganda
        karbohidrat = 0.625 * kebutuhan_kalori / 4
        kolesterol = 300
        gula = 0.025 * kebutuhan_kalori
        serat = 12.5
        garam = 2400
        kalium = 3500
        print("Ini hipertensi")
    elif 'Kolesterol' in penyakit_input:
        kebutuhan_kalori = faktor * AKEi
        protein = 0.8 * AKEi / 4
        karbohidrat = 0.65 * AKEi / 4
        lemak = 0.225 * AKEi / 9
        lemak_jenuh = 0.07 * AKEi / 9
        lemak_tidak_jenuh_ganda = 0.1 * lemak
        lemak_tidak_jenuh_tunggal = lemak - lemak_jenuh - lemak_tidak_jenuh_ganda
        kolesterol = 200
        gula = 0.025 * AKEi
        if jenis_kelamin == 'pria':
            serat = 38
        elif jenis_kelamin.lower() == 'wanita':
            serat = 25
        else:
           raise ValueError("Jenis kelamin tidak valid") 
        garam = 2400
        kalium = 3500
        print("Ini kolesterol")
    else:
        return ValueError("Penyakit tidak valid")
    
    return np.array([[kebutuhan_kalori, protein, lemak, lemak_jenuh, lemak_tidak_jenuh_ganda, lemak_tidak_jenuh_tunggal, karbohidrat, kolesterol, gula, serat, garam, kalium]])


@app.route('/rekomendasi', methods=['POST'])
def rekomendasi():
    data = request.get_json()
    Tb = int(data['tinggi_badan'])
    jenis_kelamin = data['jenis_kelamin']
    umur = int(data['umur'])
    penyakit_input = data['penyakit'].split(',')
    alergi = data['alergi'].split(',')
    
    dataset = pd.read_csv("C:\\Users\\aallv\\Documents\\Project TA\\Model-Model-Model\\CombinedResep.csv")
    
    meal_factors = {1: 0.25, 2: 0.40, 3: 0.35}
    results = {}
    
    berat_badan_ideal = hitung_berat_badan_ideal(Tb)
    AKEi = hitung_AKEi_umur(berat_badan_ideal, jenis_kelamin, umur)
    
    mealtime_map = {1: 'sarapan', 2: 'makan siang', 3: 'makan malam'}
    
    for meal_id, factor in meal_factors.items():
        meal_dataset = dataset[dataset['Meal ID'] == meal_id]
        if meal_dataset.empty:
            continue
        
        features = meal_dataset[['Energi (kkal)', 'Protein (g)', 'Lemak (g)', 'Lemak Jenuh (g)', 'Lemak tak Jenuh Ganda (g)', 'Lemak tak Jenuh Tunggal (g)', 'Karbohidrat (g)', 'Kolesterol (mg)', 'Gula (g)', 'Serat (g)', 'Sodium (mg)', 'Kalium (mg)']]
        features_scaled = scaler.transform(features)  # Langsung transform menggunakan scaler yang dimuat
        
        mealtime = mealtime_map[meal_id]
        target = hitung_kebutuhan_nutrisi(mealtime, AKEi * factor, penyakit_input, jenis_kelamin, alergi)
        target_scaled = scaler.transform(target.reshape(1, -1))  # Pastikan target berbentuk array 2D
        
        distances , indices = knn.kneighbors(target_scaled, return_distance=True)
        
        recommendations = []
        for idx in indices[0]:
            recommended_food = meal_dataset.iloc[idx]
            if not any(allergen in recommended_food['Ingredients'] for allergen in alergi):
                recommendations.append(recommended_food[['Nama Resep', 'Energi (kkal)', 'Karbohidrat (g)', 'Lemak (g)', 'Protein (g)']].to_dict())
        
        results[mealtime] = recommendations
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
