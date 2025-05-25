import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def calcular_parametros(dist_max, tiempo, dist_caida):
    r = dist_max/2
    r_final = (dist_max - dist_caida) / 2
    w = 2 * np.pi / tiempo
    a = - (1 / tiempo) * np.log(r_final / r) #despeje de la ecuacion diferencial
    w_final = w * np.exp(-a * tiempo) # Tiempo final// se asume que el radio decrese de igual forma que la velocidad angular
    return r, w, a,w_final

def imprimir_datos(r,w,a,w_final):
  
    print("\nParámetros calculados:")
    print(f"radio inicial (r): {r:.2f} m")
    print(f"velocidad angular inicial estimada (w): {w:.4f} rad/s")
    print(f"Velocidad angular final estimada (w): {w_final:.4f} rad/s")
    print(f"Coeficiente de amortiguamiento (a): {a:.6f} 1/s")
    
def crear_lienzo(dist_max):
    fig, ax = plt.subplots(figsize=(7.68, 7.68))
    limite = dist_max * 0.6
    ax.set_xlim(-limite, limite)
    ax.set_ylim(-limite, limite)
    ax.set_xlabel('Posición en X (m)')
    ax.set_ylabel('Posición en Y (m)')
    ax.set_title('Simulación Boomerang')
    ax.grid(True)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.set_aspect('equal', adjustable='box')
    return fig, ax

def simular_boomerang(dist_max, tiempo, dist_caida):
    r, w, a, w_final = calcular_parametros(dist_max, tiempo, dist_caida)

    imprimir_datos(r,w,a,w_final)
    fps = 30
    intervalo = 1000 / fps
    t_max = tiempo

    fig, ax = crear_lienzo(dist_max)

    linea, = ax.plot([], [], 'b', lw=2)
    punto_inicio, = ax.plot([], [], 'ro', markersize=6, label='Inicio')  # rojo
    punto_final, = ax.plot([], [], 'go', markersize=6, label='Final')    # verde


    def init():
        linea.set_data([], [])
        return linea,

    def animate(i):
        t = np.linspace(0, t_max * i / 100, 500)

        # se hace que la velocidad angular varie//w_real es la velocidad angular en cada momento durante su vuelo
        w_real = w * np.exp(-a * t)
        dt = np.gradient(t)
        theta = np.cumsum(w_real * dt)

        #hacer que no parezca un "circulo perfecto"
        r_var = r * (1 - 0.35 * np.sin(theta / 2))


        elongacion_x = 1.08
        
        x = r_var * elongacion_x * np.cos(theta) * np.exp(-a * t)
        y = r_var * np.sin(theta) * np.exp(-a * t)

        linea.set_data(x, y)
        punto_inicio.set_data(x[0], y[0])
        punto_final.set_data(x[-1], y[-1])

        return linea, punto_inicio, punto_final

    bumeran = animation.FuncAnimation(fig, animate, init_func=init, frames=100, interval=intervalo, blit=True, repeat=False
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
