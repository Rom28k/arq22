import asyncio
import time

SOCK_BUFFER = 1024  # Tamaño del buffer de lectura

# ------------------------------------------------------------
# Función asíncrona: envía una operación al servidor y recibe el resultado
# ------------------------------------------------------------
async def send_request(message: str):
    reader, writer = await asyncio.open_connection("127.0.0.1", 5000)

    print(f"Enviando: {message}")
    writer.write((message + "\n").encode("utf-8"))
    await writer.drain()

    # Leer respuesta del servidor con tamaño fijo
    data = await reader.read(SOCK_BUFFER)
    response = data.decode("utf-8").strip()
    print(f"Respuesta recibida: {response}")

    writer.close()
    await writer.wait_closed()

    return response


# ------------------------------------------------------------
# Función principal (lanza varias tareas en paralelo)
# ------------------------------------------------------------
async def main():
    # Lista de operaciones que se enviarán al servidor
    mensajes = ["Fib(10)", "Fact(6)", "Prime(15)"]

    # Crear tareas concurrentes (una por operación)
    tasks = [send_request(msg) for msg in mensajes]

    # Ejecutarlas simultáneamente
    respuestas = await asyncio.gather(*tasks)

    print("\nResultados finales:")
    for r in respuestas:
        print(r)


# ------------------------------------------------------------
# Ejecución principal
# ------------------------------------------------------------
if __name__ == "__main__":
    inicio = time.perf_counter()

    asyncio.run(main())

    fin = time.perf_counter()
    tiempo_total = fin - inicio

    print(f"\nTiempo total de ejecución: {tiempo_total:.6f} segundos")
    print("Fin del programa.")

