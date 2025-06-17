from flask import Flask, render_template, request

app = Flask(__name__)

# Fungsi keanggotaan segitiga
def triangular(x, a, b, c):
    if x <= a or x >= c:
        return 0
    elif a < x <= b:
        return (x - a) / (b - a)
    elif b < x < c:
        return (c - x) / (c - b)

# Fungsi keanggotaan karburator
def karburator_kecil(x): return triangular(x, 10, 15, 20)
def karburator_normal(x): return triangular(x, 15, 25, 30)
def karburator_besar(x): return triangular(x, 25, 35, 40)

# Fungsi estimasi kebutuhan bensin
def estimasi_bensin(kecepatan, jarak_km=100):
    if kecepatan <= 40:
        efisiensi = 40  # km/liter
    elif kecepatan <= 70:
        efisiensi = 30
    else:
        efisiensi = 20
    return jarak_km / efisiensi  # liter

# Nilai kecepatan (output)
def kecepatan_lambat(): return 30
def kecepatan_sedang(): return 60
def kecepatan_cepat(): return 100

# Fungsi untuk menghasilkan data grafik fuzzy mamdani
def generate_fuzzy_chart_data():
    x_vals = [x * 1.0 for x in range(10, 41)]  # Ukuran karburator dari 10 cm³ sampai 40 cm³
    kecil = [karburator_kecil(x) for x in x_vals]
    normal = [karburator_normal(x) for x in x_vals]
    besar = [karburator_besar(x) for x in x_vals]
    return x_vals, kecil, normal, besar

# Inferensi fuzzy sugeno
def fuzzy_inferensi(karburator_input):
    μ_kecil = karburator_kecil(karburator_input)
    μ_normal = karburator_normal(karburator_input)
    μ_besar = karburator_besar(karburator_input)

    numerator = (
        μ_kecil * kecepatan_lambat() +
        μ_normal * kecepatan_sedang() +
        μ_besar * kecepatan_cepat()
    )
    denominator = μ_kecil + μ_normal + μ_besar

    if denominator == 0:
        return 0, (μ_kecil, μ_normal, μ_besar)
    return numerator / denominator, (μ_kecil, μ_normal, μ_besar)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    degrees = (0, 0, 0)
    input_value = None
    bensin = None

    x_vals, kecil_vals, normal_vals, besar_vals = generate_fuzzy_chart_data()

    if request.method == "POST":
        input_value = float(request.form["karburator"])
        result, degrees = fuzzy_inferensi(input_value)
        bensin = estimasi_bensin(result)

    return render_template(
        "index.html",
        result=result,
        input_value=input_value,
        degrees=degrees,
        bensin=bensin,
        x_vals=x_vals,
        kecil_vals=kecil_vals,
        normal_vals=normal_vals,
        besar_vals=besar_vals
    )

if __name__ == "__main__":  #untuk menjalankan aplikasi pada server Flask
    app.run(debug=True)
