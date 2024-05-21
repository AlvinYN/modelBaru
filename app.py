from flask import Flask, request, jsonify
import pandas as pd
from calculations import ( # Mengimpor fungsi-fungsi perhitungan dari calculations.py
    hitung_berat_badan_ideal,
    hitung_AKEi_umur,
    hitung_kebutuhan_nutrisi,
    rekomendasi_makanan,
    dataset
)

app = Flask(__name__)

@app.route('/api/rekomendasi', methods=['POST'])
def api_rekomendasi():
    data = request.json
    Tb = data.get('tinggi_badan')
    jenis_kelamin = data.get('jenis_kelamin')
    umur = data.get('umur')
    penyakit_input = data.get('penyakit', "").split(",")
    user_allergies = data.get('alergi', "").split(",")

    if not Tb or not jenis_kelamin or not umur:
        return jsonify({"error": "Invalid input"}), 400

    # Memanggil fungsi hitung Berat badan ideal
    berat_badan_ideal = hitung_berat_badan_ideal(Tb)

    # Memanggil fungsi hitung AKEi
    AKEi = hitung_AKEi_umur(berat_badan_ideal, jenis_kelamin, umur)

    # Format respon data
    response_data = {
        "sarapan": [],
        "makan siang": [],
        "makan malam": []
    }

    # Memisahkan dataset berdasarkan Meal ID
    dataset_sarapan = dataset[dataset['Meal ID'] == 1]
    dataset_makan_siang = dataset[dataset['Meal ID'] == 2]
    dataset_makan_malam = dataset[dataset['Meal ID'] == 3]

    # Menghitung dan menampilkan rekomendasi makanan untuk setiap waktu makan
    for meal_id, meal_name, dataset_mealtime in [(1, "sarapan", dataset_sarapan), (2, "makan siang", dataset_makan_siang), (3, "makan malam", dataset_makan_malam)]:
        # Menghitung kebutuhan nutrisi berdasarkan meal_id, AKEi, penyakit, dan jenis_kelamin
        nutrisi_dibutuhkan = hitung_kebutuhan_nutrisi(meal_id, AKEi, penyakit_input, jenis_kelamin)
        # Mendapatkan rekomendasi makanan berdasarkan dataset waktu makan, kebutuhan nutrisi, dan alergi pengguna
        rekomendasi = rekomendasi_makanan(dataset_mealtime, nutrisi_dibutuhkan, user_allergies)
        
        # Menambahkan Recipe ID ke dalam response
        response_data[meal_name] = [{"Recipe ID": int(recipe_id)} for recipe_id in rekomendasi['Recipe ID']]

    return jsonify(response_data) # Mengembalikan respon

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050) # Menjalankan pada port 8050
