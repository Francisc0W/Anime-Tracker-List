from flask import Flask, render_template, request, redirect, send_file
import csv
import os

app = Flask(__name__)

# Ruta principal
@app.route('/')
def index():
    animes = [
        {"id": 1, "titulo": "Naruto", "imagen": "https://cdn.myanimelist.net/images/anime/13/17405.jpg", "link": "https://myanimelist.net/anime/20/Naruto"},
        {"id": 2, "titulo": "Attack on Titan", "imagen": "https://cdn.myanimelist.net/images/anime/10/47347.jpg", "link": "https://myanimelist.net/anime/16498/Shingeki_no_Kyojin"},
        {"id": 3, "titulo": "Death Note", "imagen": "https://cdn.myanimelist.net/images/anime/9/9453.jpg", "link": "https://myanimelist.net/anime/1535/Death_Note"},
        {"id": 4, "titulo": "Fullmetal Alchemist", "imagen": "https://cdn.myanimelist.net/images/anime/1223/96541.jpg", "link": "https://myanimelist.net/anime/5114/Fullmetal_Alchemist__Brotherhood"},
        {"id": 5, "titulo": "Demon Slayer", "imagen": "https://cdn.myanimelist.net/images/anime/1286/99889.jpg", "link": "https://myanimelist.net/anime/38000/Kimetsu_no_Yaiba"},
        {"id": 6, "titulo": "Jujutsu Kaisen", "imagen": "https://cdn.myanimelist.net/images/anime/1171/109222.jpg", "link": "https://myanimelist.net/anime/40748/Jujutsu_Kaisen"}
    ]
    return render_template("index.html", animes=animes)

# Ruta para marcar como visto con perfil
@app.route('/marcar_visto', methods=["POST"])
def marcar_visto():
    anime_id = request.form["anime_id"]
    titulo = request.form["titulo"]
    perfil = request.form["perfil"]

    archivo = "data/lista_animes.csv"

    # Verificar si ya existe ese anime para ese perfil
    ya_visto = False
    if os.path.exists(archivo):
        with open(archivo, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 3 and row[0] == perfil and row[1] == anime_id:
                    ya_visto = True
                    break

    # Guardar solo si no está repetido
    if not ya_visto:
        with open(archivo, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([perfil, anime_id, titulo])

    return "", 204  # Respuesta vacía (sin redireccionar)

# Ruta para ver animes vistos
@app.route('/vistos')
def vistos():
    animes_vistos = []
    try:
        with open("data/lista_animes.csv", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 3:
                    perfil, anime_id, titulo = row
                    animes_vistos.append({"perfil": perfil, "titulo": titulo})
    except FileNotFoundError:
        animes_vistos = []

    return render_template("vistos.html", animes=animes_vistos)

# Ruta para descargar el CSV
@app.route('/descargar')
def descargar():
    archivo = "data/lista_animes.csv"
    if os.path.exists(archivo):
        return send_file(archivo, as_attachment=True)
    else:
        return "No hay archivo para descargar", 404

# Ejecutar servidor
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
