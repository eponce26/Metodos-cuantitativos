import tkinter as tk
import subprocess
import simpy
import random
from PIL import Image, ImageTk
from tkinter import messagebox

# Parámetros de la simulación (se inicializan con valores predeterminados)
SEMILLA = 42
NUM_MESAS = 5
TIEMPO_COMER_MIN = 20
TIEMPO_COMER_MAX = 40
TIEMPO_LLEGADAS = 10
TOTAL_CLIENTES = 10

class Aplicacion:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title('Calculadora para Simulaciones')
        self.ventana.geometry('800x500')
        self.ventana.config(bg='#fcfcfc')
        self.ventana.resizable(width=0, height=0)
        self.centrar_ventana(self.ventana, 800, 600)

        

        # Frame del formulario
        frame_form = tk.Frame(self.ventana, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form.pack(side="right", expand=tk.YES, fill=tk.BOTH)

        # Frame superior del formulario
        frame_form_top = tk.Frame(frame_form, height=30, bd=0, relief=tk.SOLID, bg='black')
        frame_form_top.pack(side="top", fill=tk.X)
        title = tk.Label(frame_form_top, text="Simulación de Restaurante", font=('Times', 30), fg="red", bg='#fcfcfc', pady=20)
        title.pack(expand=tk.YES, fill=tk.BOTH)

        # Frame inferior del formulario
        frame_form_fill = tk.Frame(frame_form, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form_fill.pack(side="bottom", expand=tk.YES, fill=tk.BOTH)

        # Entradas de datos
        tk.Label(frame_form_fill, text="Número de Mesas:", font=('Times', 15), bg='#fcfcfc').pack(padx=10, pady=5)
        self.num_mesas_entry = tk.Entry(frame_form_fill)
        self.num_mesas_entry.pack(padx=10, pady=5)

        tk.Label(frame_form_fill, text="Tiempo Comer Mín (min):", font=('Times', 15), bg='#fcfcfc').pack(padx=10, pady=5)
        self.tiempo_comer_min_entry = tk.Entry(frame_form_fill)
        self.tiempo_comer_min_entry.pack(padx=10, pady=5)

        tk.Label(frame_form_fill, text="Tiempo Comer Máx (min):", font=('Times', 15), bg='#fcfcfc').pack(padx=10, pady=5)
        self.tiempo_comer_max_entry = tk.Entry(frame_form_fill)
        self.tiempo_comer_max_entry.pack(padx=10, pady=5)

        tk.Label(frame_form_fill, text="Tiempo Entre Llegadas (min):", font=('Times', 15), bg='#fcfcfc').pack(padx=10, pady=5)
        self.tiempo_llegadas_entry = tk.Entry(frame_form_fill)
        self.tiempo_llegadas_entry.pack(padx=10, pady=5)

        tk.Label(frame_form_fill, text="Total Clientes:", font=('Times', 15), bg='#fcfcfc').pack(padx=10, pady=5)
        self.total_clientes_entry = tk.Entry(frame_form_fill)
        self.total_clientes_entry.pack(padx=10, pady=5)

        # Botón para iniciar la simulación
        start_button = tk.Button(frame_form_fill, text="Iniciar Simulación", font=('Times', 15), bg='red', bd=0, fg="#fff", command=self.start_simulation)
        start_button.pack(fill=tk.X, padx=270, pady=30)

        self.ventana.mainloop()

    def start_simulation(self):
        try:
            num_mesas = int(self.num_mesas_entry.get())
            tiempo_comer_min = int(self.tiempo_comer_min_entry.get())
            tiempo_comer_max = int(self.tiempo_comer_max_entry.get())
            tiempo_llegadas = int(self.tiempo_llegadas_entry.get())
            total_clientes = int(self.total_clientes_entry.get())

            self.run_simulation(num_mesas, tiempo_comer_min, tiempo_comer_max, tiempo_llegadas, total_clientes)
        except ValueError:
            messagebox.showerror("Error de entrada", "Por favor, ingrese valores válidos.")

    def run_simulation(self, num_mesas, tiempo_comer_min, tiempo_comer_max, tiempo_llegadas, total_clientes):
        random.seed(SEMILLA)
        env = simpy.Environment()
        restaurante = simpy.Resource(env, num_mesas)
        resultados = []

        env.process(self.llegada_clientes(env, restaurante, resultados, total_clientes, tiempo_llegadas))
        env.run()

        if resultados:
            tiempo_total = sum(resultados)
            tiempo_promedio = tiempo_total / len(resultados)
            messagebox.showinfo("Resultados de la Simulación",
                                f"Tiempo promedio de espera y consumo: {tiempo_promedio:.2f} minutos")
        else:
            messagebox.showinfo("Resultados de la Simulación", "No se atendieron clientes.")

    def llegada_clientes(self, env, restaurante, resultados, total_clientes, tiempo_llegadas):
        for i in range(total_clientes):
            yield env.timeout(random.expovariate(1.0 / tiempo_llegadas))
            env.process(self.cliente(env, f'Cliente {i + 1}', restaurante, resultados))

    def cliente(self, env, nombre, restaurante, resultados):
        llegada = env.now
        print(f'{nombre} llega al restaurante en el minuto {llegada:.2f}')

        with restaurante.request() as mesa:
            yield mesa
            espera = env.now - llegada
            print(f'{nombre} toma una mesa en el minuto {env.now:.2f} (esperó {espera:.2f} minutos)')

            tiempo_comer = random.randint(TIEMPO_COMER_MIN, TIEMPO_COMER_MAX)
            yield env.timeout(tiempo_comer)
            print(f'{nombre} termina de comer y deja la mesa en el minuto {env.now:.2f}')

            resultados.append(espera + tiempo_comer)

    def centrar_ventana(self, ventana, ancho, alto):
        pantalla_ancho = ventana.winfo_screenwidth()
        pantalla_alto = ventana.winfo_screenheight()
        x = int((pantalla_ancho / 2) - (ancho / 2))
        y = int((pantalla_alto / 2) - (alto / 2))
        ventana.geometry(f'{ancho}x{alto}+{x}+{y}')

    def leer_imagen(self, path, size):
        imagen = Image.open(path)
        imagen = imagen.resize(size, Image.Resampling.LANCZOS)  # Actualizado a LANCZOS
        return ImageTk.PhotoImage(imagen)

if __name__ == "__main__":
    app = Aplicacion()
