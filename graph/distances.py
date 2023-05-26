import requests
import json
def obtener_distancia_tiempo(origen, destino, clave_api):
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": origen,
        "destinations": destino,
        "key": clave_api
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data["status"] == "OK":
        distancia = data["rows"][0]["elements"][0]["distance"]["text"]
        duracion = data["rows"][0]["elements"][0]["duration"]["text"]
        return distancia, duracion
    else:
        print("No se pudo obtener la distancia y el tiempo.")
        return None, None


clave_api = "AIzaSyB1D0U0ER1HERIY2tDyxMlbhhIbPcU1rHE"
ciudades = ["Bogotá", "Medellín", "Cali", "Barranquilla", "Cartagena", "Pereira", "Manizales", "Armenia", "Bucaramanga", "Pasto",
            "Neiva", "Santa Marta", "Cúcuta", "Valledupar", "Montería", "Ibagué", "Villavicencio", "Sincelejo", "Popayán", "Tunja", "Quibdó"]
distancias_tiempo = {}
for i in range(len(ciudades)):
    print(" asd")
    for j in range(i + 1, len(ciudades)):
        origen = ciudades[i] + ", Colombia"
        destino = ciudades[j] + ", Colombia"
        distancia, duracion = obtener_distancia_tiempo(origen, destino, clave_api)

        if distancia is not None and duracion is not None:
            distancias_tiempo[f"{ciudades[i]} - {ciudades[j]}"] = {
                "distancia": distancia,
                "tiempo": duracion
            }

with open("distancias_tiempo.json", "w") as archivo:
    json.dump(distancias_tiempo, archivo, indent=2)

print("El archivo distancias_tiempo.json se ha generado correctamente.")


