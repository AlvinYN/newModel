import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import numpy as np

# Fungsi untuk menghitung berat badan ideal
def hitung_berat_badan_ideal(Tb):
    ideal_weight = (Tb - 100) - (0.1 * (Tb - 100))
    print(f"hitung_berat_badan_ideal - Tb: {Tb}, Ideal Weight: {ideal_weight}")
    return ideal_weight

# Fungsi untuk menghitung kebutuhan kalori dasar
def hitung_AKEi_umur(Bi, jenis_kelamin, umur):
    if 20 <= umur <= 29:
        AKEi = (15.3 * Bi + 679) * 1.78 if jenis_kelamin == 'laki-laki' else (14.7 * Bi + 496) * 1.64
    elif 30 <= umur <= 59:
        AKEi = (11.6 * Bi + 879) * 1.78 if jenis_kelamin == 'laki-laki' else (8.7 * Bi + 829) * 1.64
    elif umur >= 60:
        AKEi = (13.5 * Bi + 487) * 1.78 if jenis_kelamin == 'laki-laki' else (13.5 * Bi + 596) * 1.64
    else:
        AKEi = 0  # asumsi untuk umur di luar range
    print(f"hitung_AKEi_umur - Bi: {Bi}, Gender: {jenis_kelamin}, Age: {umur}, AKEi: {AKEi}")
    return AKEi


# Fungsi untuk menghitung faktor kebutuhan nutrisi berdasarkan mealtime
def hitung_kebutuhan_faktor(meal_id):
    faktor_map = {'sarapan': 0.25, 'makan siang': 0.40, 'makan malam': 0.35}
    return faktor_map[meal_id]

def hitung_kebutuhan_nutrisi(mealtime, AKEi, penyakit_input_list, jenis_kelamin):
    faktor = hitung_kebutuhan_faktor(mealtime)
    penyakit_input = set(penyakit_input_list)
    # Initialize all nutritional needs to zero
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
        print(f"Untuk Diabetes, Hipertensi, Kolesterol bersamaan - Kalori: {kebutuhan_kalori}, Protein: {protein}")
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
        print(f"Untuk Diabetes dan Hipertensi - Kalori: {kebutuhan_kalori}, Protein: {protein}")
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
        print(f"Untuk Diabetes dan Kolesterol - Kalori: {kebutuhan_kalori}, Protein: {protein}")
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
        print(f"Untuk Hipertensi dan Kolesterol - Kalori: {kebutuhan_kalori}, Protein: {protein}")
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
        print("Ini diabetes")
        print(f"Untuk Diabetes - Kalori: {kebutuhan_kalori}, Protein: {protein}")
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
        print("Ini hipertensi")
        print(f"Untuk Hipertensi - Kalori: {kebutuhan_kalori}, Protein: {protein}")
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
        print("Ini kolesterol")
        print(f"Untuk Kolesterol - Kalori: {kebutuhan_kalori}, Protein: {protein}")
    else:
        return ValueError("Penyakit tidak valid")
    
    return np.array([[kebutuhan_kalori, protein, lemak, lemak_jenuh, lemak_tidak_jenuh_ganda, lemak_tidak_jenuh_tunggal, karbohidrat, kolesterol, gula, serat, garam, kalium]])
