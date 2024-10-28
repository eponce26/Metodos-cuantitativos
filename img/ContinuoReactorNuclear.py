import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class SimuladorEnfriamiento:
    def __init__(self):
        # Configuración de la ventana principal
        self.root = tk.Tk()
        self.root.title("Simulación de Enfriamiento de Reactor Nuclear")
        self.root.geometry('800x500')
        self.root.config(bg='#fcfcfc')
        self.root.resizable(width=0, height=0)
        self.centrar_ventana(self.root, 1000, 800)

        # Frame del formulario
        frame_form = tk.Frame(self.root, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form.pack(side="right", expand=tk.YES, fill=tk.BOTH)

        # Frame superior del formulario
        frame_form_top = tk.Frame(frame_form, height=30, bd=0, relief=tk.SOLID, bg='black')
        frame_form_top.pack(side="top", fill=tk.X)
        title = tk.Label(frame_form_top, text="Simulación de Enfriamiento de Reactor Nuclear", font=('Times', 30), fg="red", bg='#fcfcfc', pady=50)
        title.pack(expand=tk.YES, fill=tk.BOTH)

        # Frame inferior del formulario
        frame_form_fill = tk.Frame(frame_form, height=30, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form_fill.pack(side="bottom", expand=tk.YES, fill=tk.BOTH)

        # Etiquetas y campos de entrada
        tk.Label(frame_form_fill, text="Tasa de generación de calor (W):", font=('Times', 15), bg='#fcfcfc').pack(pady=10)
        self.entry_Q_gen = tk.Entry(frame_form_fill, font=('Times', 15))
        self.entry_Q_gen.pack(pady=10)

        tk.Label(frame_form_fill, text="Coeficiente de enfriamiento (W/°C):", font=('Times', 15), bg='#fcfcfc').pack(pady=10)
        self.entry_k = tk.Entry(frame_form_fill, font=('Times', 15))
        self.entry_k.pack(pady=10)

        tk.Label(frame_form_fill, text="Temperatura del sistema de enfriamiento (°C):", font=('Times', 15), bg='#fcfcfc').pack(pady=10)
        self.entry_T_cool = tk.Entry(frame_form_fill, font=('Times', 15))
        self.entry_T_cool.pack(pady=10)

        tk.Label(frame_form_fill, text="Capacidad térmica del reactor (J/°C):", font=('Times', 15), bg='#fcfcfc').pack(pady=10)
        self.entry_C = tk.Entry(frame_form_fill, font=('Times', 15))
        self.entry_C.pack(pady=10)

        tk.Label(frame_form_fill, text="Temperatura inicial del reactor (°C):", font=('Times', 15), bg='#fcfcfc').pack(pady=10)
        self.entry_T0 = tk.Entry(frame_form_fill, font=('Times', 15))
        self.entry_T0.pack(pady=10)

        # Botón para ejecutar la simulación
        button_run = tk.Button(frame_form_fill, text="Ejecutar Simulación", font=('Times', 15, 'bold'), bg='red', bd=0, fg="#fff", command=self.run_simulation)
        button_run.pack(pady=30)

        # Ejecutar la aplicación
        self.root.mainloop()

    def modelo(self, T, t, Q_gen, k, T_cool, C):
        dT_dt = (Q_gen / C) - k * (T - T_cool)
        return dT_dt

    def run_simulation(self):
        try:
            # Obtener datos del usuario
            Q_gen = float(self.entry_Q_gen.get())
            k = float(self.entry_k.get())
            T_cool = float(self.entry_T_cool.get())
            C = float(self.entry_C.get())
            T0 = float(self.entry_T0.get())
            
            # Tiempo de simulación
            tiempo = np.linspace(0, 200, 1000)
            
            # Resolver la ecuación diferencial
            solucion = odeint(self.modelo, T0, tiempo, args=(Q_gen, k, T_cool, C))
            
            # Graficar los resultados
            plt.figure(figsize=(10, 5))
            plt.plot(tiempo, solucion, label='Temperatura del Reactor')
            plt.xlabel('Tiempo (minutos)')
            plt.ylabel('Temperatura (°C)')
            plt.title('Enfriamiento del Reactor Nuclear')
            plt.axhline(T_cool, color='red', linestyle='--', label='Temperatura del Sistema de Enfriamiento')
            plt.grid(True)
            plt.legend()
            plt.show()
        except ValueError:
            messagebox.showerror("Error de entrada", "Por favor, ingrese valores numéricos válidos.")

    def centrar_ventana(self, ventana, ancho, alto):
        pantalla_ancho = ventana.winfo_screenwidth()
        pantalla_alto = ventana.winfo_screenheight()
        x = int((pantalla_ancho / 2) - (ancho / 2))
        y = int((pantalla_alto / 2) - (alto / 2))
        ventana.geometry(f'{ancho}x{alto}+{x}+{y}')

    def leer_imagen(self, path, size):
        try:
            imagen = Image.open(path)
            imagen = imagen.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(imagen)
        except FileNotFoundError:
            print(f"Image file not found: {path}")
            return None

if __name__ == "__main__":
    app = SimuladorEnfriamiento()
