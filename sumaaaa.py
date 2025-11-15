import time
from threading import Thread
import matplotlib.pyplot as plt

# ============================
#  FUNCIONES DE LA PREGUNTA 1
# ============================

def suma_pares_serial(n: int) -> int:
    """Suma 2 + 4 + ... + 2n de forma secuencial."""
    s = 0
    for i in range(1, n + 1):
        s += 2 * i
    return s


def suma_parcial(inicio: int, fin: int, resultados: list[int], idx: int):
    """Suma parcial de 2i para i en [inicio, fin] y guarda en resultados[idx]."""
    total = 0
    for i in range(inicio, fin + 1):
        total += 2 * i
    resultados[idx] = total


def suma_pares_paralela(n: int, num_hilos: int) -> int:
    """Suma 2 + 4 + ... + 2n usando num_hilos hilos."""
    if num_hilos > n:
        num_hilos = n  # evitar hilos sin trabajo

    resultados = [0] * num_hilos
    hilos = []

    tam_segmento = n // num_hilos
    resto = n % num_hilos

    inicio = 1
    for idx in range(num_hilos):
        fin = inicio + tam_segmento - 1
        if idx < resto:
            fin += 1

        t = Thread(target=suma_parcial, args=(inicio, fin, resultados, idx))
        t.start()
        hilos.append(t)

        inicio = fin + 1

    for t in hilos:
        t.join()

    return sum(resultados)


# ============================
#  EXPERIMENTOS (c) y (d)
# ============================

def main():
    # n solicitados
    n_values = [10**5, 10**6, 5 * 10**6, 10**7, 5 * 10**7, 10**8, 10**9]
    # núcleos (hilos) solicitados
    p_values = [4, 8, 16]

    # Para guardar tiempos y speedups
    tiempos_serial = {}
    tiempos_paralelos = {p: {} for p in p_values}
    speedups = {p: [] for p in p_values}

    for n in n_values:
        # ----- tiempo serial -----
        t0 = time.perf_counter()
        suma_s = suma_pares_serial(n)
        t1 = time.perf_counter()
        ts = t1 - t0
        tiempos_serial[n] = ts

        # comprobación con la fórmula cerrada n*(n+1)
        assert suma_s == n * (n + 1)

        print(f"N = {n}")
        print(f"Tiempo de ejecución serial: {ts:.6f} s")

        # ----- tiempos paralelos para cada P -----
        for p in p_values:
            t0 = time.perf_counter()
            suma_p = suma_pares_paralela(n, p)
            t1 = time.perf_counter()
            tp = t1 - t0
            tiempos_paralelos[p][n] = tp

            # comprobación
            assert suma_p == suma_s == n * (n + 1)

            print(f"P = {p}, Tiempo de ejecución paralelo: {tp:.6f} s")

        print("-" * 40)

    # ----- Calcular SpeedUp y graficar (d) -----
    for p in p_values:
        for n in n_values:
            ts = tiempos_serial[n]
            tp = tiempos_paralelos[p][n]
            su = ts / tp if tp > 0 else 0.0
            speedups[p].append(su)

    # Gráfico SpeedUp vs n
    plt.figure()
    for p in p_values:
        plt.plot(n_values, speedups[p], marker="o", label=f"P = {p}")
    plt.xscale("log")  # opcional, porque n crece mucho
    plt.xlabel("n (tamaño del problema)")
    plt.ylabel("SpeedUp = T_serial / T_paralelo")
    plt.title("SpeedUp en función de n para distintos números de hilos")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
