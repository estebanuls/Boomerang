import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def calcular_parametros(dist_max_diametro, tiempo_vuelo, dist_caida_diametro):
    r = dist_max_diametro / 2
    r_final = (dist_max_diametro - dist_caida_diametro )/2

    w = 2 * np.pi / tiempo_vuelo

    a = - (1 / tiempo_vuelo) * np.log(r_final / r)

    return r_final, w, a

def simular_boomerang(dist_max_diametro, tiempo_vuelo, dist_caida_diametro):
    r, w, a = calcular_parametros(dist_max_diametro, tiempo_vuelo, dist_caida_diametro)

    print("\n--- Parámetros calculados para la simulación ---")
    print(f"Radio (r): {r:.3f} m")
    print(f"Velocidad angular (w): {w:.3f} rad/s")
    print(f"Coeficiente de amortiguamiento (a): {a:.5f} 1/s")
    print("------------------------------------------------")

    fps = 30
    intervalo_milisegundos = 1000 / fps
    t_max = tiempo_vuelo

    fig, ax = plt.subplots(figsize=(8, 8))
    limite = dist_max_diametro * 0.6
    ax.set_xlim(-limite, limite)
    ax.set_ylim(-limite, limite)
    ax.set_xlabel('Posición en X (m)')
    ax.set_ylabel('Posición en Y (m)')
    ax.set_title('Simulación de trayectoria de boomerang')
    ax.grid(True)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.set_aspect('equal', adjustable='box')

    linea, = ax.plot([], [], 'b-', lw=2)

    def init():
        linea.set_data([], [])
        return linea,

    def animate(i):
        t = np.linspace(0, t_max * i / 100, 500)
        x = r * np.cos(w * t) * np.exp(-a * t)
        y = r * np.sin(w * t) * np.exp(-a * t)
        linea.set_data(x, y)
        return linea,

    anim = animation.FuncAnimation(
        fig, animate, init_func=init,
        frames=100, interval=intervalo_milisegundos, blit=True, repeat=False
    )

    plt.show()

if __name__ == '__main__':
    print("=== Simulación de boomerang ===")
    print("Ingresa los datos como se piden (en metros y segundos).")
    try:
        dist_max = (float(input(" Distancia máxima (ida): ")))*2
        tiempo_vuelo = float(input("Tiempo total de vuelo (en segundos): "))
        dist_caida = float(input("Distancia desde el origen al punto donde cayo (en metros): "))
    except ValueError:
        print(" Error: debes ingresar valores numericos.")
        exit()

    if dist_caida >= dist_max:
        print("\n Error: la distancia de caída debe ser menor que la distancia maxima.")
        exit()

    simular_boomerang(dist_max, tiempo_vuelo, dist_caida)
