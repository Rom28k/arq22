from multiprocessing import Process, Array

def suma_parcial(arr, inicio, fin, idx):
  
    total = 0

    # Recorrer el rango asignado y sumar el cuadrado de cada número
    for i in range(inicio, fin + 1):
        total += i * i

    # Guardar el resultado en el array compartido
    arr[idx] = total


if __name__ == "__main__":
    # Array compartido de 8 posiciones para los 8 resultados parciales
    compartido = Array('i', 8)

    procesos = []
    N = 1000
    bloques = N // 8  # Cada proceso procesará un bloque de igual tamaño

    # Crear los 8 procesos
    for idx in range(8):
        inicio = idx * bloques + 1
        fin = inicio + bloques - 1

        # Ajustar último proceso para llegar exactamente a 1000
        if idx == 7:
            fin = N

        p = Process(target=suma_parcial, args=(compartido, inicio, fin, idx))
        procesos.append(p)
        p.start()

    # Esperar que todos los procesos terminen
    for p in procesos:
        p.join()

    # Sumar los resultados parciales del array compartido
    suma_total = sum(compartido[:])

    print(f"Suma total de cuadrados del 1 al 1000: {suma_total}")
