import threading 
import time
from threading import Lock
# Saldo inicial de la cuenta
saldo = 10000

lock = Lock()

def retirar(cantidad):
   
    global saldo
    with lock: 
 
        if saldo >= cantidad:
            temp = saldo                # Leer el saldo actual
            time.sleep(0.001)           # Simular retraso → expone la condición de carrera
            saldo = temp - cantidad     # Actualizar el saldo
            print(f"Retiro de {cantidad} realizado. Saldo restante: {saldo}")
        else:
            print("Saldo insuficiente.")


if __name__ == "__main__":
    hilos = []

    
    for i in range(15):
        hilo = threading.Thread(target=retirar, args=(100,))

        hilos.append(hilo)
        hilo.start()  # Iniciar cada hilo

    # Esperar a que todos los hilos terminen
    for hilo in hilos:
        hilo.join()

    print(f"\nSaldo final: {saldo}")
