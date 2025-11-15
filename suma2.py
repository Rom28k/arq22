import random
import time
from threading import Thread

def estimate_e_serial(n: int) -> float:
    total_sum = 0

    for _ in range(n):
        suma = 0.0
        count = 0
        while suma <= 1.0:
            r = random.random()  # U(0,1)
            suma += r
            count += 1
        total_sum += count

    return total_sum / n

def worker_estimate_e(num_iter: int, resultados: list[int], idx: int):
    """
    Hilo worker: ejecuta num_iter veces el experimento
    y guarda su suma parcial en resultados[idx].
    """
    # Semilla distinta por hilo (no es obligatorio, pero queda más prolijo)
    random.seed(time.time_ns() ^ (idx << 16))

    total_sum = 0
    for _ in range(num_iter):
        suma = 0.0
        count = 0
        while suma <= 1.0:
            r = random.random()
            suma += r
            count += 1
        total_sum += count

    resultados[idx] = total_sum


def estimate_e_threads(n: int, num_threads: int) -> float:
    """
    Estima e usando num_threads hilos.
    """
    if num_threads > n:
        num_threads = n  # evitar hilos sin trabajo

    # Repartir las n iteraciones entre los hilos
    base = n // num_threads
    resto = n % num_threads
    trabajos = [base + (1 if i < resto else 0) for i in range(num_threads)]

    resultados = [0] * num_threads
    hilos = []

    for idx, iteraciones in enumerate(trabajos):
        t = Thread(target=worker_estimate_e, args=(iteraciones, resultados, idx))
        t.start()
        hilos.append(t)

    # Esperar a todos los hilos
    for t in hilos:
        t.join()

    total_sum = sum(resultados)
    return total_sum / n


if __name__ == "__main__":
    n = 5 * 10**5  # OJO: para probar usa algo mucho menor que 5*10**7

    # Tiempo serial
    t0 = time.perf_counter()
    e_serial = estimate_e_serial(n)
    t1 = time.perf_counter()
    t_serial = t1 - t0
    print(f"Estimación serial: {e_serial}")
    print(f"Tiempo serial: {t_serial:.6f} s\n")

    # Prueba con distintos números de hilos
    for p in [2, 4, 8, 16]:
        t0 = time.perf_counter()
        e_par = estimate_e_threads(n, p)
        t1 = time.perf_counter()
        t_par = t1 - t0

        speedup = t_serial / t_par
        print(f"P = {p}")
        print(f"  Estimación paralela: {e_par}")
        print(f"  Tiempo paralelo: {t_par:.6f} s")
        print(f"  SpeedUp: {speedup:.3f}\n")
