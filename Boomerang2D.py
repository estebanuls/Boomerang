import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def trayectoria_boomerang(radio_inicial, velocidad_angular, amortiguamiento, tiempo_maximo):
  # Tiempo máximo de la simulación
    fps = 30
    intervalo_milisegundos = 1000 / fps

    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(-radio_inicial * 1.1, radio_inicial * 1.1)  # Ajustar límites para ver la trayectoria completa
    ax.set_ylim(-radio_inicial * 1.1, radio_inicial * 1.1)
    ax.set_xlabel('Posición en X')
    ax.set_ylabel('Posición en Y')
    ax.set_title('Trayectoria del boomerang')
    ax.grid(True)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.set_aspect('equal', adjustable='box')


    linea, = ax.plot([], [], 'b-') 
    def iniciar_animacion():
        linea.set_data([], [])
        return linea,

    def animar_cuadro(cuadro):
        t = np.linspace(0, tiempo_maximo * cuadro / 100, 100) # El tiempo aumenta linealmente con el cuadro
        x = radio_inicial * np.cos(velocidad_angular * t) * np.exp(-amortiguamiento * t)
        y = radio_inicial * np.sin(velocidad_angular * t) * np.exp(-amortiguamiento * t)
        linea.set_data(x, y)
        return linea,

    animacion_boomerang = animation.FuncAnimation(fig, animar_cuadro, init_func=iniciar_animacion,
                                            frames=100, interval=intervalo_milisegundos, blit=True, repeat=False) 

    plt.show()

if _name_ == '_main_':
    try:
        radio = float(input("ingresar radio inicial: "))
        velocidad = float(input("ingresa velocidad angular: "))
        amort = float(input("ingresa el coeficiente de amortiguamiento: "))
        tiempo = float(input("ingresa el tiempo maximo de la simulacion: "))
    except ValueError:
        print("ingresa los valores numericos validos.")
    else:
        trayectoria_boomerang(radio, velocidad, amort, tiempo)
