import simpy
import random
import tkinter as tk
from tkinter import messagebox

# Parámetros de la simulación
SEMILLA = 42
CAPACIDAD_SERVIDOR = 1
CAPACIDAD_COLA = 5
TIEMPO_PROCESAMIENTO_MIN = 2
TIEMPO_PROCESAMIENTO_MAX = 5
TIEMPO_LLEGADAS = 3
TOTAL_PAQUETES = 50

# Variables para seguimiento de estadísticas
paquetes_perdidos = 0
tiempo_total_espera = 0
paquetes_procesados = 0

# Función para simular el proceso de un paquete
def paquete(env, nombre, servidor):
    global paquetes_perdidos, tiempo_total_espera, paquetes_procesados

    llegada = env.now
    print(f'{nombre} llega al servidor en el segundo {llegada:.2f}')

    with servidor.request() as req:
        if len(servidor.queue) >= CAPACIDAD_COLA:
            paquetes_perdidos += 1
            print(f'{nombre} se pierde debido a cola llena en el segundo {env.now:.2f}')
            return

        yield req
        espera = env.now - llegada
        tiempo_total_espera += espera
        print(f'{nombre} comienza a ser procesado después de esperar {espera:.2f} segundos en el segundo {env.now:.2f}')

        tiempo_procesamiento = random.randint(TIEMPO_PROCESAMIENTO_MIN, TIEMPO_PROCESAMIENTO_MAX)
        yield env.timeout(tiempo_procesamiento)
        print(f'{nombre} termina de ser procesado en el segundo {env.now:.2f}')
        paquetes_procesados += 1

# Función para la llegada de paquetes
def llegada_paquetes(env, servidor):
    for i in range(TOTAL_PAQUETES):
        yield env.timeout(random.expovariate(1.0 / TIEMPO_LLEGADAS))
        env.process(paquete(env, f'Paquete {i + 1}', servidor))

# Función para ejecutar la simulación
def run_simulation(capacidad_servidor, capacidad_cola, tiempo_llegadas, total_paquetes):
    global paquetes_perdidos, tiempo_total_espera, paquetes_procesados
    paquetes_perdidos = 0
    tiempo_total_espera = 0
    paquetes_procesados = 0

    random.seed(SEMILLA)
    env = simpy.Environment()
    servidor = simpy.Resource(env, capacidad_servidor)
    env.process(llegada_paquetes(env, servidor))
    env.run()

    if paquetes_procesados > 0:
        tasa_perdida = 100 * paquetes_perdidos / total_paquetes
        tiempo_promedio_espera = tiempo_total_espera / paquetes_procesados
        utilizacion_servidor = 100 * (paquetes_procesados * ((TIEMPO_PROCESAMIENTO_MIN + TIEMPO_PROCESAMIENTO_MAX) / 2) / env.now)

        result = (f'Total de paquetes simulados: {total_paquetes}\n'
                  f'Paquetes procesados: {paquetes_procesados}\n'
                  f'Paquetes perdidos: {paquetes_perdidos}\n'
                  f'Tasa de pérdida de paquetes: {tasa_perdida:.2f}%\n'
                  f'Tiempo promedio de espera de los paquetes: {tiempo_promedio_espera:.2f} segundos\n'
                  f'Utilización del servidor: {utilizacion_servidor:.2f}%')
    else:
        result = "No se procesaron paquetes."

    messagebox.showinfo("Resultados de la Simulación", result)

# Clase para la interfaz gráfica
class Aplicacion:
    def __init__(self):        
        self.ventana = tk.Tk()                             
        self.ventana.title('Simulación de Servidor de Red')
        self.ventana.geometry('800x500')
        self.ventana.config(bg='#fcfcfc')
        self.ventana.resizable(width=0, height=0)    
        self.centrar_ventana(self.ventana, 800, 600)

        # Frame del formulario
        frame_form = tk.Frame(self.ventana, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form.pack(expand=tk.YES, fill=tk.BOTH)

        # Frame superior del formulario
        frame_form_top = tk.Frame(frame_form, height=30, bd=0, relief=tk.SOLID, bg='black')
        frame_form_top.pack(side="top", fill=tk.X)
        title = tk.Label(frame_form_top, text="Simulación de Servidor de Red", font=('Times', 30), fg="red", bg='#fcfcfc', pady=10)
        title.pack(expand=tk.YES, fill=tk.BOTH)

        # Entradas
        tk.Label(frame_form, text="Capacidad del Servidor:", bg='#fcfcfc', font=('Times', 15)).pack(pady=10)
        self.capacidad_servidor_entry = tk.Entry(frame_form, font=('Times', 15))
        self.capacidad_servidor_entry.pack(pady=10)

        tk.Label(frame_form, text="Capacidad de la Cola:", bg='#fcfcfc', font=('Times', 15)).pack(pady=10)
        self.capacidad_cola_entry = tk.Entry(frame_form, font=('Times', 15))
        self.capacidad_cola_entry.pack(pady=10)

        tk.Label(frame_form, text="Tiempo entre llegadas (segundos):", bg='#fcfcfc', font=('Times', 15)).pack(pady=10)
        self.tiempo_llegadas_entry = tk.Entry(frame_form, font=('Times', 15))
        self.tiempo_llegadas_entry.pack(pady=10)

        tk.Label(frame_form, text="Total de Paquetes:", bg='#fcfcfc', font=('Times', 15)).pack(pady=10)
        self.total_paquetes_entry = tk.Entry(frame_form, font=('Times', 15))
        self.total_paquetes_entry.pack(pady=10)

        start_button = tk.Button(frame_form, text="Iniciar Simulación", font=('Times', 15, 'bold'), bg='red', fg="#fff", command=self.start_simulation)
        start_button.pack(pady=30)

        self.ventana.mainloop()

    def start_simulation(self):
        try:
            capacidad_servidor = int(self.capacidad_servidor_entry.get())
            capacidad_cola = int(self.capacidad_cola_entry.get())
            tiempo_llegadas = int(self.tiempo_llegadas_entry.get())
            total_paquetes = int(self.total_paquetes_entry.get())

            # Validación adicional
            if capacidad_servidor <= 0 or capacidad_cola < 0 or tiempo_llegadas <= 0 or total_paquetes <= 0:
                raise ValueError("Todos los valores deben ser mayores que cero.")

            run_simulation(capacidad_servidor, capacidad_cola, tiempo_llegadas, total_paquetes)
        except ValueError as e:
            messagebox.showerror("Error de entrada", str(e))

    def centrar_ventana(self, ventana, ancho, alto):
        pantalla_ancho = ventana.winfo_screenwidth()
        pantalla_alto = ventana.winfo_screenheight()
        x = int((pantalla_ancho / 2) - (ancho / 2))
        y = int((pantalla_alto / 2) - (alto / 2))
        ventana.geometry(f'{ancho}x{alto}+{x}+{y}')

if __name__ == "__main__":
    app = Aplicacion()
