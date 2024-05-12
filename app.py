from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
import pickle
from calculations import hitung_berat_badan_ideal, hitung_AKEi_umur, hitung_kebutuhan_nutrisi

app = Flask(__name__)

# Load your dataset and models outside of the route to improve performance
dataset = pd.read_csv("CombinedResep.csv")
with open('knn_model.pkl', 'rb') as file:
    knn = pickle.load(file)

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    Tb = int(data['tinggi_badan'])
    jenis_kelamin = data['jenis_kelamin'].lower()  # normalize input to lower case to match calculation assumptions
    umur = int(data['umur'])
    penyakit_input = data['penyakit'].split(",")  # split diseases by comma
    alergi = data['alergi'].split(",")  # split allergies by comma

    berat_badan_ideal = hitung_berat_badan_ideal(Tb)
    AKEi = hitung_AKEi_umur(berat_badan_ideal, jenis_kelamin, umur)
    
    print(f"Processed Inputs: TB={Tb}, Gender={jenis_kelamin}, Age={umur}, Ideal Weight={berat_badan_ideal}, AKEi={AKEi}, Diseases={penyakit_input}, Allergies={alergi}")

    recommendations = {}
    meal_factors = {1: 0.25, 2: 0.40, 3: 0.35}
    mealtime_map = {1: 'sarapan', 2: 'makan siang', 3: 'makan malam'}
    
    scaler = MinMaxScaler()

    for meal_id, factor in meal_factors.items():
        mealtime = mealtime_map[meal_id]
        meal_dataset = dataset[dataset['Meal ID'] == meal_id]

        if meal_dataset.empty:
            continue

        features = meal_dataset[['Energi (kkal)', 'Protein (g)', 'Lemak (g)', 'Lemak Jenuh (g)', 'Lemak tak Jenuh Ganda (g)', 'Lemak tak Jenuh Tunggal (g)', 'Karbohidrat (g)', 'Kolesterol (mg)', 'Gula (g)', 'Serat (g)', 'Sodium (mg)', 'Kalium (mg)']]
        features_scaled = scaler.fit_transform(features)

        target = hitung_kebutuhan_nutrisi(mealtime, AKEi, penyakit_input, jenis_kelamin)
        if isinstance(target, list):
            target = np.array(target)  # Ensure target is numpy array
        if target.ndim == 1:
            target = target.reshape(1, -1)  # Reshape if it's a flat array

        print(f"Shape of target for scaling: {target.shape}")  # Debugging statement
        target_scaled = scaler.transform(target)
        distances, indices = knn.kneighbors(target_scaled, return_distance=True)
        food_list = []
        
        for idx, distance in zip(indices[0], distances[0]):
            recommended_food = meal_dataset.iloc[idx]
            if not any(allergen in recommended_food['Ingredients'] for allergen in alergi):
                food_details = {'Recipe ID': int(recommended_food['Recipe ID'])}
                food_details['distance'] = distance
                food_list.append(food_details)

        recommendations[mealtime] = food_list
    print(f"Recommendations: {recommendations}")
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050)
