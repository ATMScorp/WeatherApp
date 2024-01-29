import tkinter as tk
from tkinter import ttk
import requests
import time


def pobierz_pogode():
    miasto = pole_wprowadzania.get()
    klucz_api = "3e0c2aacd1094b9465fe5d11737be8c8"
    url_api = f"https://api.openweathermap.org/data/2.5/weather?q={miasto}&appid={klucz_api}"

    try:
        odpowiedz = requests.get(url_api)
        odpowiedz.raise_for_status()  # Sprawdź, czy odpowiedź z serwera jest poprawna

        dane = odpowiedz.json()

        warunki = dane['weather'][0]['main']
        temp = int(dane['main']['temp'] - 273.15)
        temp_min, temp_max = map(lambda x: int(x - 273.15), (dane['main']['temp_min'], dane['main']['temp_max']))
        cisnienie, wilgotnosc, wiatr = dane['main']['pressure'], dane['main']['humidity'], dane['wind']['speed']
        wschod_slonca = time.strftime('%I:%M:%S', time.gmtime(dane['sys']['sunrise'] - 21600))
        zachod_slonca = time.strftime('%I:%M:%S', time.gmtime(dane['sys']['sunset'] - 21600))

        info = f"{warunki}\n{temp}°C"
        dane_pogodowe = f"Temp. min: {temp_min}°C, Temp. max: {temp_max}°C\n" \
                        f"Ciśnienie: {cisnienie}, Wilgotność: {wilgotnosc}\n" \
                        f"Prędkość wiatru: {wiatr}, Wschód słońca: {wschod_slonca}, Zachód słońca: {zachod_slonca}"

        etykieta_info.config(text=info)
        etykieta_dane.config(text=dane_pogodowe)
    except requests.exceptions.RequestException:
        etykieta_info.config(text="Błąd: Nieprawidłowe miasto")
        etykieta_dane.config(text="Sprawdź poprawność nazwy miasta.")


# Utwórz główne okno
root = tk.Tk()
root.geometry("600x500")
root.title("Aplikacja Pogodowa")

# Ramka dla pola wprowadzania i przycisku
ramka_wprowadzania = ttk.LabelFrame(root, text="Wprowadź Miasto")
ramka_wprowadzania.pack(pady=20)

# Pole wprowadzania
pole_wprowadzania = ttk.Entry(ramka_wprowadzania, font=("poppins", 14))
pole_wprowadzania.grid(row=0, column=0, padx=10, pady=10)

# Przycisk
przycisk_pobierz_pogode = ttk.Button(ramka_wprowadzania, text="Pobierz Pogodę", command=pobierz_pogode)
przycisk_pobierz_pogode.grid(row=0, column=1, padx=10, pady=10)

# Ramka dla wyników
ramka_wynikow = ttk.LabelFrame(root, text="Informacje o Pogodzie")
ramka_wynikow.pack(pady=20)

# Etykiety do wyświetlenia informacji o pogodzie
etykieta_info = ttk.Label(ramka_wynikow, font=("poppins", 20))
etykieta_info.grid(row=0, column=0, padx=10, pady=10, sticky="w")

etykieta_dane = ttk.Label(ramka_wynikow, font=("poppins", 12))
etykieta_dane.grid(row=1, column=0, padx=10, pady=10, sticky="w")

root.mainloop()