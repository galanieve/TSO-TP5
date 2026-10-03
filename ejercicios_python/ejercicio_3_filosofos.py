"""
UNJu - Facultad de Ingeniería
Teoría de Sistemas Operativos (TSO) - Ciclo Lectivo 2026
Cátedra: Ing. María Fernanda Vázquez - JTP: Ing. Fabio D. Argañaraz

Ejercicio Práctico N° 3: La Cena de los Filósofos (Prevención de Deadlock)
"""

import threading
import time
import random

NUM_FILOSOFOS = 5
tenedores = [threading.Lock() for _ in range(NUM_FILOSOFOS)]
comidas = [0] * NUM_FILOSOFOS
lock_print = threading.Lock()

def log(msg):
    with lock_print:
        print(msg)

def pensar(id):
    log(f"🤔 Filósofo {id} está pensando...")
    time.sleep(random.uniform(0.05, 0.15))

def comer(id):
    log(f"🍝 Filósofo {id} está comiendo espagueti...")
    comidas[id] += 1
    time.sleep(random.uniform(0.05, 0.15))
    log(f"✨ Filósofo {id} terminó de comer (total comidas: {comidas[id]}).")

def filosofo(id, rondas=3):
    for _ in range(rondas):
        pensar(id)
        
        tenedor_izq = id
        tenedor_der = (id + 1) % NUM_FILOSOFOS
        
        # Estrategia Asimétrica de Dijkstra (Prevención de Deadlock)
        if id == NUM_FILOSOFOS - 1:
            primer_tenedor = tenedores[tenedor_der]
            segundo_tenedor = tenedores[tenedor_izq]
        else:
            primer_tenedor = tenedores[tenedor_izq]
            segundo_tenedor = tenedores[tenedor_der]
            
        with primer_tenedor:
            with segundo_tenedor:
                comer(id)

if __name__ == "__main__":
    print("=" * 60)
    print(" Iniciando Simulación de los Filósofos Comensales (UNJu FI)")
    print("=" * 60)
    
    hilos = []
    for i in range(NUM_FILOSOFOS):
        t = threading.Thread(target=filosofo, args=(i, 3), name=f"Filosofo-{i}")
        hilos.append(t)
        t.start()
        
    for t in hilos:
        t.join()
        
    print("=" * 60)
    print(" Resumen de Comidas:")
    for i, c in enumerate(comidas):
        print(f" - Filósofo {i}: {c} veces comió.")
    print(" ¡Simulación completada sin Interbloqueo (Deadlock)!")
    print("=" * 60)
    