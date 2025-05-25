import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

def calcular_parametros(dist_max, tiempo, dist_caida):
    r = dist_max / 2
    r_final = (dist_max - dist_caida) / 2
    w = 2 * np.pi / tiempo
    a = - (1 / tiempo) * np.log(r_final / r)
    return r, w, a

def dibujar_elipsoide(ax, centro, radios, color='blue', alpha=0.5):
    u = np.linspace(0, 2 * np.pi, 30)
    v = np.linspace(0, np.pi, 30)
    x = radios[0] * np.outer(np.cos(u), np.sin(v)) + centro[0]
    y = radios[1] * np.outer(np.sin(u), np.sin(v)) + centro[1]
    z = radios[2] * np.outer(np.ones_like(u), np.cos(v)) + centro[2]
    ax.plot_surface(x, y, z, color=color, alpha=alpha)

def simular_boomerang_3d(dist_max, tiempo, dist_caida, amplitud_vertical):
    r, w_inicial, a = calcular_parametros(dist_max, tiempo, dist_caida)
    a_z = amplitud_vertical

    print("\nParámetros calculados:")
    print(f"Radio inicial (r): {r:.2f} m")
    print(f"Velocidad angular inicial (w): {w_inicial:.4f} rad/s")
    print(f"Coeficiente de amortiguamiento (a): {a:.6f} 1/s")
    print(f"Amplitud vertical (a_z): {a_z:.2f} m")
    print("------------------------------------------------")

    fps = 30
    intervalo = 1000 / fps
    t_max = tiempo

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    limite = dist_max * 0.6
    ax.set_xlim(-limite, limite)
    ax.set_ylim(-limite, limite)
    ax.set_zlim(0, a_z * 1.5)

    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_title('Simulación 3D Boomerang - Ideal vs Real')

    elongacion_x = 1.08
    radios_persona = (0.5, 0.3, 1.5)
    posicion_inicial_x = r * elongacion_x
    posicion_inicial_y = 0
    posicion_inicial_z = radios_persona[2] / 2

    centro_persona = (posicion_inicial_x, posicion_inicial_y, posicion_inicial_z)
    dibujar_elipsoide(ax, centro_persona, radios_persona, color='orange', alpha=0.6)

    linea_ideal, = ax.plot([], [], [], 'g-', lw=2, label='Ideal (sin amortiguamiento)')
    linea_real, = ax.plot([], [], [], 'r--', lw=2, label='Real (con amortiguamiento)')
    ax.legend()

    def init():
        linea_ideal.set_data([], [])
        linea_ideal.set_3d_properties([])
        linea_real.set_data([], [])
        linea_real.set_3d_properties([])
        return linea_ideal, linea_real

    def animate(i):
        t = np.linspace(0, t_max * i / 100, 500)

        theta_ideal = w_inicial * t
        r_ideal = r

        x_ideal = r_ideal * elongacion_x * np.cos(theta_ideal)
        y_ideal = r_ideal * np.sin(theta_ideal)
        z_ideal = a_z * np.sin(np.pi * t / t_max)

        w_real = w_inicial * np.exp(-a * t)
        dt = np.gradient(t)
        theta_real = np.cumsum(w_real * dt)

        r_deform = r * (1 - 0.15 * np.sin(2 * theta_real))

        x_real = r_deform * elongacion_x * np.cos(theta_real)
        y_real = r_deform * np.sin(theta_real)
        z_real = a_z * np.sin(np.pi * t / t_max)

        linea_ideal.set_data(x_ideal, y_ideal)
        linea_ideal.set_3d_properties(z_ideal)

        linea_real.set_data(x_real, y_real)
        linea_real.set_3d_properties(z_real)

        return linea_ideal, linea_real

    anim = animation.FuncAnimation(
        fig, animate, init_func=init,
        frames=100, interval=intervalo, blit=True, repeat=False
    )

    plt.show()

if __name__ == '__main__':
    print("Ingrese los datos como se piden (en metros y segundos).")
    try:
        dist_max = float(input("Distancia máxima (m): "))
        tiempo = float(input("Tiempo total de vuelo (s): "))
        dist_caida = float(input("Distancia hasta donde cayó (m): "))
        amplitud_vertical = float(input("Amplitud vertical (m): "))
    except ValueError:
        print("Error: Debe ingresar números válidos.")
        exit()

    if dist_caida >= dist_max:
        print("\nError: La distancia de caída debe ser menor que la distancia máxima.")
        exit()

    simular_boomerang_3d(dist_max, tiempo, dist_caida, amplitud_vertical)
