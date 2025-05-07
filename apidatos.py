import requests
from pymongo import MongoClient
import dash
from dash import html, dash_table

# -------------------- 1. OBTENER Y LIMPIAR DATOS --------------------
url = "https://restcountries.com/v3.1/all"
response = requests.get(url)

data_limpia = []

if response.status_code == 200:
    paises = response.json()
    for pais in paises:
        nombre = pais.get("name", {}).get("common")
        capital = pais.get("capital", [])
        region = pais.get("region")
        poblacion = pais.get("population", 0)

        if nombre and isinstance(nombre, str):
            data_limpia.append({
                "País": nombre,
                "Capital": capital[0] if capital else "Desconocida",
                "Región": region if region else "Sin datos",
                "Población": poblacion if isinstance(poblacion, int) else 0
            })

# Ordenar por población descendente
data_limpia = sorted(data_limpia, key=lambda x: x["Población"], reverse=True)

# -------------------- 2. SUBIR A MONGODB ATLAS --------------------
# URI de conexión (reemplázala con la tuya si cambia)
uri = "mongodb+srv://Countries:Country1@cluster0.0b8ol.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Conectar con MongoDB Atlas
cliente = MongoClient(uri)

# Base de datos y colección
db = cliente["dashboard_paises"]
coleccion = db["paises"]

# Limpiar colección e insertar nuevos datos
coleccion.delete_many({})
coleccion.insert_many(data_limpia)

print("✅ Datos subidos exitosamente a MongoDB Atlas.")

# -------------------- 3. CREAR DASHBOARD --------------------
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard de Países (REST Countries API + MongoDB)"),
    dash_table.DataTable(
        columns=[{"name": col, "id": col} for col in data_limpia[0].keys()],
        data=data_limpia,
        page_size=10,
        filter_action="native",
        sort_action="native",
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left'},
        style_header={'fontWeight': 'bold', 'backgroundColor': '#f0f0f0'}
    )
])

if __name__ == "__main__":
    app.run(debug=True)
