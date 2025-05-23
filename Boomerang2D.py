import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def calcular_parametros(dist_max, tiempo, dist_caida):
    r = dist_max/2
    r_final = (dist_max - dist_caida) / 2
    w = 2 * np.pi / tiempo
    a = - (1 / tiempo) * np.log(r_final / r) #despeje de la ecuacion diferencial

    return r, w, a

def simular_boomerang(dist_max, tiempo, dist_caida):
    r, w, a = calcular_parametros(dist_max, tiempo, dist_caida)



    print("\nParámetros calculados:")
    print(f"radio inicial (r): {r:.2f} m")
    print(f"velocidad angular promedio: {w:.4f} rad/s")
    print(f"Coeficiente de amortiguamiento (a): {a:.6f} 1/s")
    print("------------------------------------------------")

    fps = 30
    intervalo = 1000 / fps
    t_max = tiempo

    fig, ax = plt.subplots(figsize=(7.68, 7.68))
    limite = (dist_max)*0.6
    ax.set_xlim(-limite, limite)
    ax.set_ylim(-limite, limite)
    ax.set_xlabel('Posición en X (m)')
    ax.set_ylabel('Posición en Y (m)')
    ax.set_title('Simulación Boomerang')
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

        dt = np.gradient(t)
        theta = np.cumsum(w * dt)

        #hacer que no parezca un "circulo perfecto"
        r_var = r * (1 - 0.35 * np.sin(theta / 2))


        estirar_x = 1.08
        estirar_y = 1.0

        x = r_var * estirar_x * np.cos(theta) * np.exp(-a * t)
        y = r_var * estirar_y * np.sin(theta) * np.exp(-a * t)

        linea.set_data(x, y)
        return linea,

    anim = animation.FuncAnimation(
        fig, animate, init_func=init,
        frames=100, interval=intervalo, blit=True, repeat=False
    )

    plt.show()

if __name__ == '__main__':
    print("ingresa los datos como se piden (en metros y segundos).")
    try:
        dist_max = float(input("distancia maxima: "))
        tiempo = float(input("tiempo total de vuelo: "))
        dist_caida = float(input("distancia desde tu posicion hasta donde cayó (en metros): "))
    except ValueError:
        print(" error: debes ingresar numeros.")
        exit()

    if dist_caida >= dist_max:
        print("\n error: la distancia de caida debe ser menor que la distancia maxima.")
        exit()

    simular_boomerang(dist_max, tiempo, dist_caida)
