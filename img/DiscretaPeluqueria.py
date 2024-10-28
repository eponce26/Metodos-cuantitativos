import random
import math
import simpy
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class SimuladorPeluqueria:
    def __init__(self):
        # Configuración de la ventana principal
        self.root = tk.Tk()
        self.root.title("Simulación de Peluquería")
        self.root.geometry('800x500')
        self.root.config(bg='#fcfcfc')
        self.root.resizable(width=0, height=0)
        self.centrar_ventana(self.root, 800, 750)

        # Frame del formulario
        frame_form = tk.Frame(self.root, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form.pack(side="right", expand=tk.YES, fill=tk.BOTH)

        # Frame superior del formulario
        frame_form_top = tk.Frame(frame_form, height=30, bd=0, relief=tk.SOLID, bg='black')
        frame_form_top.pack(side="top", fill=tk.X)
        title = tk.Label(frame_form_top, text="Simulación de Peluquería", font=('Times', 30), fg="red", bg='#fcfcfc', pady=50)
        title.pack(expand=tk.YES, fill=tk.BOTH)

        # Frame inferior del formulario
        frame_form_fill = tk.Frame(frame_form, height=30, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form_fill.pack(side="bottom", expand=tk.YES, fill=tk.BOTH)

        # Etiquetas y campos de entrada
        tk.Label(frame_form_fill, text="Número de peluqueros:", font=('Times', 15), bg='#fcfcfc').pack(pady=10)
        self.entry_peluqueros = tk.Entry(frame_form_fill, font=('Times', 15))
        self.entry_peluqueros.pack(pady=10)

        tk.Label(frame_form_fill, text="Tiempo de corte mínimo (min):", font=('Times', 15), bg='#fcfcfc').pack(pady=10)
        self.entry_tiempo_min = tk.Entry(frame_form_fill, font=('Times', 15))
        self.entry_tiempo_min.pack(pady=10)

        tk.Label(frame_form_fill, text="Tiempo de corte máximo (min):", font=('Times', 15), bg='#fcfcfc').pack(pady=10)
        self.entry_tiempo_max = tk.Entry(frame_form_fill, font=('Times', 15))
        self.entry_tiempo_max.pack(pady=10)

        tk.Label(frame_form_fill, text="Promedio de llegadas (min):", font=('Times', 15), bg='#fcfcfc').pack(pady=10)
        self.entry_llegadas = tk.Entry(frame_form_fill, font=('Times', 15))
        self.entry_llegadas.pack(pady=10)

        tk.Label(frame_form_fill, text="Total de clientes:", font=('Times', 15), bg='#fcfcfc').pack(pady=10)
        self.entry_clientes = tk.Entry(frame_form_fill, font=('Times', 15))
        self.entry_clientes.pack(pady=10)

        # Botón para ejecutar la simulación
        btn_simular = tk.Button(frame_form_fill, text="Ejecutar Simulación", font=('Times', 15, 'bold'), bg='red', bd=0, fg="#fff", command=self.ejecutar_simulacion)
        btn_simular.pack(fill=tk.X, padx=270, pady=20)

        # Inicializar variables globales
        self.te = 0.0  # tiempo de espera total
        self.dt = 0.0  # duración del servicio
        self.fin = 0.0  # minuto en que finaliza
        self.num_peluqueros = 1  # Inicializar con un valor por defecto

        # Ejecutar la aplicación
        self.root.mainloop()

    def cortar(self, cliente, tiempo_corte_min, tiempo_corte_max):
        tiempo_corte = random.uniform(tiempo_corte_min, tiempo_corte_max)  # distribución uniforme
        yield env.timeout(tiempo_corte)  # dejar correr el tiempo n minutos
        self.dt += tiempo_corte  # acumular tiempo de uso de la instalación
        print(f"Corte listo a {cliente} en {tiempo_corte:.2f} minutos")

    def cliente(self, env, name, personal, tiempo_corte_min, tiempo_corte_max):
        llega = env.now  # guarda el minuto de llegada del cliente
        with personal.request() as request:  # espera turno
            yield request  # obtener turno
            pasa = env.now
            espera = pasa - llega  # acumulo tiempo de espera
            self.te += espera  # acumulo tiempo de espera
            print(f"{name} pasa y espera en la peluquería en el minuto {pasa:.2f}, habiendo esperado {espera:.2f}")
            yield env.process(self.cortar(name, tiempo_corte_min, tiempo_corte_max))  # llamar al proceso cortar
            deja = env.now  # momento en que el cliente deja la peluquería
            self.fin = deja  # guardo el minuto en que termina
            print(f"{name} deja la peluquería en el minuto {deja:.2f}")

    def principal(self, env, personal, tot_clientes, t_llegadas, tiempo_corte_min, tiempo_corte_max):
        for i in range(tot_clientes):
            llegada = -t_llegadas * math.log(random.random())  # llegada exponencial
            yield env.timeout(llegada)  # dejo transcurrir un tiempo entre un cliente y otro
            env.process(self.cliente(env, f'Cliente {i + 1}', personal, tiempo_corte_min, tiempo_corte_max))

    def mostrar_resultados(self, tot_clientes):
        lpc = self.te / self.fin if self.fin > 0 else 0
        tep = self.te / tot_clientes if tot_clientes > 0 else 0
        upi = (self.dt / self.fin) / self.num_peluqueros if self.fin > 0 else 0

        resultados = (
            f"---Resultados de la Simulación---\n"
            f"Longitud promedio de la cola: {lpc:.2f}\n"
            f"Tiempo de espera promedio: {tep:.2f} minutos\n"
            f"Uso promedio de la instalación: {upi:.2f}"
        )

        # Crear ventana emergente con los resultados
        messagebox.showinfo("Resultados de la Simulación", resultados)

    def ejecutar_simulacion(self):
        global env  # Hacer global para el acceso en la simulación
        # Obtener datos de entrada
        try:
            self.num_peluqueros = int(self.entry_peluqueros.get())
            tiempo_corte_min = int(self.entry_tiempo_min.get())
            tiempo_corte_max = int(self.entry_tiempo_max.get())
            t_llegadas = int(self.entry_llegadas.get())
            tot_clientes = int(self.entry_clientes.get())
            
            # Programa principal
            random.seed(30)
            env = simpy.Environment()  # creo el entorno de simulación
            personal = simpy.Resource(env, self.num_peluqueros)  # crea los recursos peluqueros
            env.process(self.principal(env, personal, tot_clientes, t_llegadas, tiempo_corte_min, tiempo_corte_max))
            env.run()
            
            # Mostrar los resultados en una ventana emergente
            self.mostrar_resultados(tot_clientes)
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores válidos.")

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
    app = SimuladorPeluqueria()
