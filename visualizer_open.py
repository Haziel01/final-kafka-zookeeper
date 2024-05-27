import pymongo
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import tkinter as tk
import threading
from PIL import Image, ImageTk
from googletrans import Translator

def mostrar_openweathermap():
    client = pymongo.MongoClient('mongodb+srv://dbUser:010801Haziel@cluster0.dx95efh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
    db = client['CPD']
    collection = db['openweathermap']

    latest_document = collection.find_one({}, sort=[('_id', pymongo.DESCENDING)])

    country = latest_document["sys"]["country"]
    city = latest_document["name"]
    temp_kelvin = latest_document["main"]["temp"]
    feels_like_kelvin = latest_document["main"]["feels_like"]
    temp_min_kelvin = latest_document["main"]["temp_min"]
    temp_max_kelvin = latest_document["main"]["temp_max"]
    wind_speed_ms = latest_document["wind"]["speed"]
    clouds_percent = latest_document["clouds"]["all"]
    pressure_hpa = latest_document["main"]["pressure"]
    weather_main = latest_document["weather"][0]["main"]
    weather_description = latest_document["weather"][0]["description"]
    humidity = latest_document["main"]["humidity"]

    temp_celsius = temp_kelvin - 273.15
    feels_like_celsius = feels_like_kelvin - 273.15
    temp_min_celsius = temp_min_kelvin - 273.15
    temp_max_celsius = temp_max_kelvin - 273.15
    wind_speed_kmh = wind_speed_ms * 3.6
    pressure_psi = round(pressure_hpa / 68.9475729, 2)

    ventana = tk.Tk()
    ventana.title("El Clima")

    fondo_color = "#FFDAB9"
    imagen_degradado = Image.new("RGB", (800, 600), fondo_color)
    fondo = ImageTk.PhotoImage(imagen_degradado)

    label_fondo = tk.Label(ventana, image=fondo)
    label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

    font_title = ("Helvetica", 36, "bold")
    font_data = ("Helvetica", 20)
    font_small_data = ("Helvetica", 14, "underline")

    etiqueta_ciudad_pais = tk.Label(ventana, text=f"{city}, {country}", font=font_title, highlightthickness=0)
    etiqueta_ciudad_pais.pack(pady=10)

    try:
        translator = Translator()
        weather_main_es = translator.translate(weather_main, dest='es').text
        weather_description_es = translator.translate(weather_description, dest='es').text
    except Exception as e:
        print("Error al traducir:", e)
        weather_main_es = "Despejado"
        weather_description_es = "Cielo despejado"

    datos_temperatura = f"Temperatura: {temp_celsius:.1f} °C (Min: {temp_min_celsius:.1f} °C, Max: {temp_max_celsius:.1f} °C)"
    etiqueta_temperatura = tk.Label(ventana, text=datos_temperatura, font=font_data, highlightthickness=0)
    etiqueta_temperatura.pack()

    datos_sensacion_termica = f"Sensación Térmica: {feels_like_celsius:.1f} °C"
    etiqueta_sensacion_termica = tk.Label(ventana, text=datos_sensacion_termica, font=font_data, highlightthickness=0)
    etiqueta_sensacion_termica.pack(pady=10)

    datos_extra = f"Clima: {weather_main_es}, {weather_description_es} |  Humedad: {humidity}%"
    etiqueta_extra = tk.Label(ventana, text=datos_extra, font=font_small_data, highlightthickness=0)
    etiqueta_extra.pack()

    datos_viento_nubosidad_presion = f"Velocidad del Viento: {wind_speed_kmh:.1f} km/h   |   Nubosidad: {clouds_percent}%   |   Presión Atmosférica: {pressure_psi} PSI"
    etiqueta_viento_nubosidad_presion = tk.Label(ventana, text=datos_viento_nubosidad_presion, font=font_small_data, highlightthickness=0)
    etiqueta_viento_nubosidad_presion.pack(pady=10)

    ventana.mainloop()

def mostrar_exchangerate():
    client = pymongo.MongoClient('mongodb+srv://dbUser:010801Haziel@cluster0.dx95efh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
    db = client['CPD']
    collection = db['exchangerate']

    latest_document = collection.find_one({}, sort=[('_id', pymongo.DESCENDING)])
    desired_currencies = ["MXN", "ARS", "EUR", "JPY", "GBP",
                          'CAD', 'KWD', 'CHF', 'BRL', 'DKK',
                          'NZD', 'RUB', 'CNY', 'CLP' ,'COP', 'KRW']

    if latest_document:
        conversion_rates = latest_document.get("conversion_rates", {})
        conversion_values = [conversion_rates.get(currency, 0) for currency in desired_currencies]

        time_last_update_utc = latest_document.get("time_last_update_utc", "")
        time_next_update_utc = latest_document.get("time_next_update_utc", "")

        plt.figure(figsize=(12, 8))
        colors = ['skyblue', 'salmon', 'lightgreen', 'gold', 'lightcoral',
                  'cornflowerblue', 'orangered', 'limegreen', 'khaki', 'tomato',
                  'deepskyblue', 'darkorange', 'mediumseagreen', 'palegoldenrod', 'coral']
        plt.bar(desired_currencies, conversion_values, color=colors)
        plt.xlabel('Divisa')
        plt.ylabel('Valor de Conversión')
        plt.title(f'Cambio de 1 Dolar Americano\nÚltima actualización: {time_last_update_utc}\nPróxima actualización: {time_next_update_utc}')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()

        for i, v in enumerate(conversion_values):
            plt.text(i, v + 0.01, f'{v:.2f}', ha='center', va='bottom', fontweight='bold')

        plt.show()
    else:
        print("No se encontraron datos en la colección 'exchangerate'.")

def ejecutar_en_hilo(func):
    thread = threading.Thread(target=func)
    thread.start()

if __name__ == "__main__":
    ejecutar_en_hilo(mostrar_openweathermap)
    ejecutar_en_hilo(mostrar_exchangerate)
