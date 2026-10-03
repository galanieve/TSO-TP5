"""
UNJu - Facultad de Ingeniería
Teoría de Sistemas Operativos (TSO) - Ciclo Lectivo 2026
Cátedra: Ing. María Fernanda Vázquez - JTP: Ing. Fabio D. Argañaraz

Ejercicio Práctico N° 2: El Problema del Oso y las Abejas
"""

import sys
import threading
import time
import random

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

M = 10                  # Capacidad del tarro de miel
NUM_ABEJAS = 5          # Número de abejas obreras
tarro_miel = 0          # Variable compartida
simulacion_activa = True

mutex = threading.Lock()
sem_oso = threading.Semaphore(0)
sem_tarro_disponible = threading.Semaphore(1)

def abeja(id_abeja):
    global tarro_miel, simulacion_activa
    while simulacion_activa:
        time.sleep(random.uniform(0.05, 0.2))
        
        sem_tarro_disponible.acquire()
        with mutex:
            if not simulacion_activa:
                sem_tarro_disponible.release()
                break
                
            tarro_miel += 1
            print(f"🐝 Abeja {id_abeja} depositó miel. Tarro: {tarro_miel}/{M}")
            
            if tarro_miel == M:
                print(f"🔔 ¡Tarro lleno ({tarro_miel}/{M})! Abeja {id_abeja} despierta al oso.")
                sem_oso.release()
            else:
                sem_tarro_disponible.release()

def oso(max_tarros=2):
    global tarro_miel, simulacion_activa
    tarros_comidos = 0
    while tarros_comidos < max_tarros and simulacion_activa:
        sem_oso.acquire()
        
        if not simulacion_activa:
            break
            
        print("🐻 Oso despertó y se está comiendo toda la miel...")
        time.sleep(0.05)
        tarro_miel = 0
        tarros_comidos += 1
        print(f"🐻 Oso terminó de comer. Tarros comidos: {tarros_comidos}/{max_tarros}.\n")
        
        sem_tarro_disponible.release()
        
    simulacion_activa = False
    sem_tarro_disponible.release()

if __name__ == "__main__":
    print("=" * 60)
    print(" Iniciando Simulación: El Oso y las Abejas (UNJu FI)")
    print("=" * 60)
    
    t_oso = threading.Thread(target=oso, args=(2,), name="Oso")
    t_oso.start()
    
    hilos_abejas = []
    for i in range(1, NUM_ABEJAS + 1):
        t = threading.Thread(target=abeja, args=(i,), name=f"Abeja-{i}")
        hilos_abejas.append(t)
        t.start()
        
    t_oso.join()
    for t in hilos_abejas:
        t.join()
        
    print("=" * 60)
    print(" Simulación finalizada exitosamente.")
    print("=" * 60)