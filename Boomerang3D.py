import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

def trayectoria_comparativa_3d(radio_inicial, velocidad_angular, amortiguamiento, tiempo_maximo):
    # Simula y compara dos trayectorias 3D: una ideal (sin pérdida de energía)
    # y otra realista con amortiguamiento exponencial

    fps = 30
    intervalo_milisegundos = 1000 / fps

    # Crear la figura y el gráfico 3D
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(-radio_inicial * 1.2, radio_inicial * 1.2)
    ax.set_ylim(-radio_inicial * 1.2, radio_inicial * 1.2)
    ax.set_zlim(-radio_inicial * 0.6, radio_inicial * 0.6)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Comparación de trayectorias 3D del boomerang')

    # Inicializar líneas vacías para ambas trayectorias
    linea_ideal, = ax.plot([], [], [], 'g-', lw=2, label='Ideal')
    linea_real, = ax.plot([], [], [], 'r--', lw=2, label='Real')
    ax.legend()

    # Función de inicialización para la animación
    def iniciar_animacion():
        linea_ideal.set_data([], [])
        linea_ideal.set_3d_properties([])
        linea_real.set_data([], [])
        linea_real.set_3d_properties([])
        return linea_ideal, linea_real

    # Función que actualiza los datos de cada cuadro
    def animar_cuadro(cuadro):
        t = np.linspace(0, tiempo_maximo * cuadro / 100, 300)

        # Trayectoria ideal (sin amortiguamiento)
        x_ideal = radio_inicial * np.cos(velocidad_angular * t)
        y_ideal = radio_inicial * np.sin(velocidad_angular * t)
        z_ideal = 0.2 * radio_inicial * np.sin(2 * velocidad_angular * t)

        # Trayectoria real (con amortiguamiento)
        x_real = x_ideal * np.exp(-amortiguamiento * t)
        y_real = y_ideal * np.exp(-amortiguamiento * t)
        z_real = z_ideal

        linea_ideal.set_data(x_ideal, y_ideal)
        linea_ideal.set_3d_properties(z_ideal)
        linea_real.set_data(x_real, y_real)
        linea_real.set_3d_properties(z_real)
        return linea_ideal, linea_real

    # Crear y mostrar la animación
    animacion = animation.FuncAnimation(
        fig, animar_cuadro, init_func=iniciar_animacion,
        frames=100, interval=intervalo_milisegundos, blit=True, repeat=False
    )

    plt.show()

if __name__ == '__main__':
    # Pedir parámetros al usuario y ejecutar la simulación
    try:
        radio = float(input("Ingresar radio inicial: "))
        velocidad = float(input("Ingresar velocidad angular: "))
        amort = float(input("Ingresar el coeficiente de amortiguamiento: "))
        tiempo = float(input("Ingresar el tiempo máximo de la simulación: "))
    except ValueError:
        print("Ingresa valores numéricos válidos.")
    else:
        trayectoria_comparativa_3d(radio, velocidad, amort, tiempo)
