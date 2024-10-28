import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class SimuladorDescomposicion:
    def __init__(self):
        # Configuración de la ventana principal
        self.ventana = tk.Tk()
        self.ventana.title("Simulador de Descomposición de Reactivo")
        self.ventana.geometry('800x500')
        self.ventana.config(bg='#fcfcfc')
        self.ventana.resizable(width=0, height=0)    
        self.centrar_ventana(self.ventana, 800, 500)


        # Frame del formulario
        frame_form = tk.Frame(self.ventana, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form.pack(side="right", expand=tk.YES, fill=tk.BOTH)

        # Frame superior del formulario
        frame_form_top = tk.Frame(frame_form, height=30, bd=0, relief=tk.SOLID, bg='black')
        frame_form_top.pack(side="top", fill=tk.X)
        title = tk.Label(frame_form_top, text="Simulador de Descomposición de Reactivo", font=('Times', 20), fg="red", bg='#fcfcfc', pady=50)
        title.pack(expand=tk.YES, fill=tk.BOTH)

        # Frame inferior del formulario
        frame_form_fill = tk.Frame(frame_form, height=30, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form_fill.pack(side="bottom", expand=tk.YES, fill=tk.BOTH)

        # Etiquetas y campos de entrada
        label_k = tk.Label(frame_form_fill, text="Constante de velocidad (k):", font=('Times', 15), bg='#fcfcfc')
        label_k.pack(pady=10)
        self.entry_k = tk.Entry(frame_form_fill, font=('Times', 15))
        self.entry_k.pack(pady=10)

        label_A0 = tk.Label(frame_form_fill, text="Concentración inicial de A (mol/L):", font=('Times', 15), bg='#fcfcfc')
        label_A0.pack(pady=10)
        self.entry_A0 = tk.Entry(frame_form_fill, font=('Times', 15))
        self.entry_A0.pack(pady=10)

        # Botón para ejecutar la simulación
        boton_simular = tk.Button(frame_form_fill, text="Simular", font=('Times', 15, 'bold'), bg='red', bd=0, fg="#fff", command=self.simular)
        boton_simular.pack(pady=30)

        # Iniciar la aplicación
        self.ventana.mainloop()

    def simular(self):
        try:
            # Obtener la constante de velocidad y la concentración inicial
            k = float(self.entry_k.get().strip())  # Obtener la constante de velocidad
            A0 = float(self.entry_A0.get().strip())  # Obtener la concentración inicial
            
            # Verificación de los valores ingresados
            print(f"Constante de velocidad (k): {k}, Concentración inicial de A (A0): {A0}")
            
            # Ecuación diferencial para la concentración de A
            def modelo(A, t):
                dA_dt = -k * A
                return dA_dt

            # Tiempo de simulación (0 a 50 minutos, con 1000 puntos)
            tiempo = np.linspace(0, 50, 1000)  # Tiempo en minutos

            # Resolver la ecuación diferencial
            solucion = odeint(modelo, A0, tiempo)

            # Graficar los resultados
            plt.figure(figsize=(10, 5))
            plt.plot(tiempo, solucion, label='Concentración de [A]')
            plt.xlabel('Tiempo (minutos)')
            plt.ylabel('Concentración (mol/L)')
            plt.title('Descomposición de un Reactivo de Primer Orden')
            plt.grid(True)
            plt.legend()
            plt.show()

        except ValueError as e:
            messagebox.showerror("Error", f"Por favor, ingrese valores numéricos válidos.\nDetalles: {e}")

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
    app = SimuladorDescomposicion()
