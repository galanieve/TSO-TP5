"""
UNJu - Facultad de Ingeniería
Teoría de Sistemas Operativos (TSO) - Ciclo Lectivo 2026
Cátedra: Ing. María Fernanda Vázquez - JTP: Ing. Fabio D. Argañaraz

Ejercicio Práctico N° 5: Lectores - Escritores (Acceso Concurrente vs. Exclusión Mutua)
"""

import sys
import threading
import time
import random

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

mutex = threading.Semaphore(1)
sem_write = threading.Semaphore(1)
readcounter = 0

base_de_datos = {
    "version": 1,
    "contenido": "Datos iniciales consistentes del sistema operativo."
}

print_lock = threading.Lock()

def log(msg):
    with print_lock:
        print(f"[{time.strftime('%H:%M:%S')}] {msg}")

def lector(id_lector, iteraciones=2):
    global readcounter
    for _ in range(iteraciones):
        time.sleep(random.uniform(0.05, 0.15))
        
        # --- ENTRADA DEL LECTOR ---
        mutex.acquire()
        readcounter += 1
        if readcounter == 1:
            sem_write.acquire()
        mutex.release()

        # --- SECCIÓN CRÍTICA DE LECTURA ---
        log(f"📖 Lector {id_lector} LEYENDO datos (v{base_de_datos['version']}) | Lectores activos: {readcounter}")
        time.sleep(random.uniform(0.1, 0.2))
        log(f"✨ Lector {id_lector} terminó de leer.")

        # --- SALIDA DEL LECTOR ---
        mutex.acquire()
        readcounter -= 1
        if readcounter == 0:
            sem_write.release()
        mutex.release()

def escritor(id_escritor, iteraciones=2):
    global base_de_datos
    for _ in range(iteraciones):
        time.sleep(random.uniform(0.1, 0.2))
        
        log(f"⏳ Escritor {id_escritor} solicitando permiso para escribir...")
        sem_write.acquire()

        # --- SECCIÓN CRÍTICA DE ESCRITURA ---
        nueva_version = base_de_datos["version"] + 1
        log(f"✍️️ [EXCLUSIÓN MUTUA] Escritor {id_escritor} MODIFICANDO la BD a versión {nueva_version}...")
        time.sleep(random.uniform(0.1, 0.2))
        base_de_datos["version"] = nueva_version
        base_de_datos["contenido"] = f"Registro actualizado por escritor {id_escritor} a las {time.strftime('%H:%M:%S')}"
        log(f"✅ Escritor {id_escritor} finalizó escritura de versión {nueva_version}.")

        sem_write.release()

if __name__ == "__main__":
    print("=" * 70)
    print("EJERCICIO 5: Lectores y Escritores (Algoritmo de Courtois)")
    print("=" * 70)
    
    hilos = []
    
    for i in range(1, 6):
        t = threading.Thread(target=lector, args=(i,))
        hilos.append(t)
        
    for j in range(1, 3):
        t = threading.Thread(target=escritor, args=(j,))
        hilos.append(t)
        
    random.shuffle(hilos)
    for t in hilos:
        t.start()
        
    for t in hilos:
        t.join()
        
    print("\nSimulación finalizada. Estado final de la BD:", base_de_datos)