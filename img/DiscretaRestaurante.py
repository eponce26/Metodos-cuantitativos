import os
import random
import simpy
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Variables globales
SUM_ALL = 0.00
TEMP = 0
CALC = [0] * 500  # Capacidad de entrada

# Parámetros de simulación
HOUR_OPEN = 7  # Hora de apertura
HOUR_CLOSE = 23  # Hora de cierre
START = HOUR_OPEN * 60
SIM_TIME = HOUR_CLOSE * 60
CUSTOMER_RANGE_NORM = [5, 10]  # Intervalo normal para la llegada de clientes

# Funciones de la simulación
def toc(raw):
    return '%02d:%02d' % (raw // 60, raw % 60)

class WaitingLane:
    def __init__(self, env):
        self.env = env
        self.lane = simpy.Resource(env, 3)

    def serve(self, cust):
        yield self.env.timeout(0)
        print("[w] (%s) %s entered the area" % (toc(self.env.now), cust))

class CounterFirst:
    def __init__(self, env):
        self.env = env
        self.employee = simpy.Resource(env, 1)

    def serve(self, cust):
        yield self.env.timeout(random.randint(1, 3))  # 2 minutos en promedio
        print("[?] (%s) %s ordered the menu" % (toc(self.env.now), cust))

class CounterSecond:
    def __init__(self, env):
        self.env = env
        self.employee = simpy.Resource(env, 1)

    def serve(self, cust):
        yield self.env.timeout(random.randint(1, 2))  # 1 minuto en promedio
        print("[$] (%s) %s paid the order" % (toc(self.env.now), cust))

class CounterThird:
    def __init__(self, env):
        self.env = env
        self.employee = simpy.Resource(env, 1)

    def serve(self, cust):
        yield self.env.timeout(random.randint(2, 4))  # 3 minutos en promedio
        print("[#] (%s) %s took the order" % (toc(self.env.now), cust))

def customer_process(env, name, wl, ce1, ce2, ce3):
    with wl.lane.request() as request:
        yield request
        yield env.process(wl.serve(name))

    print("[v] (%s) %s is in drive-thru counter" % (toc(env.now), name))

    with ce1.employee.request() as request:
        yield request
        CALC[int(name[5:])] = env.now
        yield env.process(ce1.serve(name))

    with ce2.employee.request() as request:
        yield request
        yield env.process(ce2.serve(name))

    with ce3.employee.request() as request:
        yield request
        yield env.process(ce3.serve(name))

    print("[^] (%s) %s leaves" % (toc(env.now), name))
    global TEMP
    TEMP += 1
    CALC[int(name[5:])] = env.now - CALC[int(name[5:])]

def setup(env, cr):
    wl = WaitingLane(env)
    ce1 = CounterFirst(env)
    ce2 = CounterSecond(env)
    ce3 = CounterThird(env)
    i = 0

    while True:
        yield env.timeout(random.randint(*cr))
        i += 1
        env.process(customer_process(env, "Cust %d" % i, wl, ce1, ce2, ce3))

def run_simulation(num_counters):
    global SUM_ALL, TEMP, CALC
    env = simpy.Environment(initial_time=START)

    env.process(setup(env, CUSTOMER_RANGE_NORM))
    env.run(until=SIM_TIME)

    for i in range(TEMP):
        SUM_ALL += CALC[i]

    if TEMP > 0:
        average_time_service = SUM_ALL / TEMP
        service_per_second = 1.00 / (average_time_service * 60)
        service_per_minute = service_per_second * 60

        results = f"""
        Fin!
        Model: {num_counters} counters
        Tiempo Promedio: {average_time_service:.4f}
        Servicio por minuto: {service_per_minute:.2f}
        """
    else:
        results = "No customers were served."

    messagebox.showinfo("Simulation Results", results)

def start_simulation():
    try:
        num_counters = int(counter_entry.get())
        run_simulation(num_counters)
    except ValueError:
        messagebox.showerror("Input Error", "Por favor, ingrese un número válido.")

class SimulationApp:
    def __init__(self):
        self.ventana = tk.Tk()                             
        self.ventana.title('Calculadora para Simulaciones')
        self.ventana.geometry('800x500')
        self.ventana.config(bg='#fcfcfc')
        self.ventana.resizable(width=0, height=0)    
        self.centrar_ventana(self.ventana, 500, 300)

        # Llamar a la configuración de la interfaz gráfica
        self.setup_gui()

    def centrar_ventana(self, ventana, ancho, alto):
        # Obtener dimensiones de la pantalla
        pantalla_x = ventana.winfo_screenwidth()
        pantalla_y = ventana.winfo_screenheight()
        # Calcular la posición para centrar la ventana
        pos_x = (pantalla_x // 2) - (ancho // 2)
        pos_y = (pantalla_y // 2) - (alto // 2)
        ventana.geometry(f'{ancho}x{alto}+{pos_x}+{pos_y}')

    def setup_gui(self):
        global counter_entry

        # Frame superior
        frame_top = tk.Frame(self.ventana, bd=0, relief=tk.SOLID, bg='black', height=50)
        frame_top.pack(side="top", fill=tk.X)
        title = tk.Label(frame_top, text="Simulador de Restaurante", font=('Times', 30), fg="red", bg='#fcfcfc', pady=50)
        title.pack(expand=tk.YES, fill=tk.BOTH)

        # Frame de formulario
        frame_form = tk.Frame(self.ventana, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form.pack(expand=tk.YES, fill=tk.BOTH)

        # Etiquetas y entradas
        tk.Label(frame_form, text="Número de Contador:", font=('Times', 15), bg='#fcfcfc').grid(row=0, column=0, padx=10, pady=10, sticky='e')
        counter_entry = tk.Entry(frame_form, font=('Times', 15))
        counter_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        # Botón para iniciar la simulación
        start_button = tk.Button(frame_form, text="Iniciar Simulación", font=('Times', 15, 'bold'), bg='red', bd=0, fg="#fff", command=start_simulation)
        start_button.grid(row=1, columnspan=2, pady=30)

        # Centrar el contenido en el frame
        for widget in frame_form.winfo_children():
            widget.grid_configure(padx=20, pady=10)

        # Centrar el frame dentro de la ventana
        frame_form.pack(expand=True)

    def run(self):
        # Ejecutar la aplicación
        self.ventana.mainloop()

if __name__ == "__main__":
    app = SimulationApp()
    app.run()
