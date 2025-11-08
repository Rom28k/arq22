import asyncio
import time

# ===============================
# FUNCIONES MATEMÁTICAS
# ===============================

def is_prime(x: int) -> bool:
    if x < 2:
        return False
    if x % 2 == 0:
        return x == 2
    i = 3
    while i * i <= x:
        if x % i == 0:
            return False
        i += 2
    return True


def nth_prime(n: int) -> int:
    """Devuelve el n-ésimo número primo."""
    count, candidate = 0, 1
    while count < n:
        candidate += 1
        if is_prime(candidate):
            count += 1
    return candidate


def fact(n: int) -> int:
    """Devuelve el factorial de n."""
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def fib(n: int) -> int:
    """Devuelve el n-ésimo número de Fibonacci."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


# ===============================
# SERVIDOR ASÍNCRONO
# ===============================

async def handle_client(reader, writer):
    """Atiende cada conexión de cliente."""
    addr = writer.get_extra_info("peername")
    print(f"Conexión desde {addr}")

    while True:
        data = await reader.readline()
        if not data:
            break

        message = data.decode().strip()
        print(f"Recibido: {message}")

        start_time = time.perf_counter()  # Medir tiempo de cómputo

        # Determinar el tipo de operación
        try:
            if message.startswith("Fib(") and message.endswith(")"):
                n = int(message[4:-1])
                result = fib(n)
            elif message.startswith("Fact(") and message.endswith(")"):
                n = int(message[5:-1])
                result = fact(n)
            elif message.startswith("Prime(") and message.endswith(")"):
                n = int(message[6:-1])
                result = nth_prime(n)
            else:
                result = "ERROR: Comando no válido. Usa Fib(N), Fact(N) o Prime(N)."
        except Exception as e:
            result = f"ERROR al procesar: {e}"

        elapsed = time.perf_counter() - start_time
        response = f"Resultado: {result} (tiempo de cómputo: {elapsed:.6f}s)\n"

        writer.write(response.encode())
        await writer.drain()

    print(f"Cliente {addr} desconectado.")
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(handle_client, "127.0.0.1", 5000)
    addr = server.sockets[0].getsockname()
    print(f"Servidor escuchando en {addr}")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
