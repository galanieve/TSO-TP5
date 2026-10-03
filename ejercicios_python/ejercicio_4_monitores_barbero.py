"""
UNJu - Facultad de Ingeniería
Teoría de Sistemas Operativos (TSO) - Ciclo Lectivo 2026
Cátedra: Ing. María Fernanda Vázquez - JTP: Ing. Fabio D. Argañaraz

Ejercicio Práctico N° 4: Monitores y Variables de Condición (El Barbero Dormilón)
"""

import sys
import threading
import time
import random

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

class BarberiaMonitor:
    def __init__(self, num_sillas_espera=3):
        self.num_sillas = num_sillas_espera
        self.clientes_esperando = 0
        
        self.lock = threading.Lock()
        self.cond_barbero = threading.Condition(self.lock)
        self.cond_sala_espera = threading.Condition(self.lock)
        self.cond_corte = threading.Condition(self.lock)
        
        self.silla_barbero_ocupada = False
        self.cliente_listo_en_sillon = False
        self.corte_terminado = False
        self.barberia_abierta = True

    def entrar_cliente(self, cliente_id):
        with self.lock:
            print(f"👤 Cliente {cliente_id} llega a la barbería. (Sillas ocupadas: {self.clientes_esperando}/{self.num_sillas})")
            
            if self.clientes_esperando >= self.num_sillas:
                print(f"🚪 [SALA LLENA] Cliente {cliente_id} se va sin cortarse el pelo.")
                return False
                
            self.clientes_esperando += 1
            self.cond_barbero.notify()
            
            while self.silla_barbero_ocupada:
                self.cond_sala_espera.wait()
                
            self.clientes_esperando -= 1
            self.silla_barbero_ocupada = True
            self.cliente_listo_en_sillon = True
            self.corte_terminado = False
            self.cond_barbero.notify()
            
            while not self.corte_terminado:
                self.cond_corte.wait()
                
            self.silla_barbero_ocupada = False
            self.cliente_listo_en_sillon = False
            self.cond_barbero.notify()
            self.cond_sala_espera.notify()
            
            print(f"💈 Cliente {cliente_id} se retira con corte nuevo.")
            return True

    def atender_siguiente_cliente(self):
        with self.lock:
            while not self.cliente_listo_en_sillon and self.barberia_abierta:
                if self.clientes_esperando > 0:
                    self.cond_sala_espera.notify()
                self.cond_barbero.wait()
                
            if not self.barberia_abierta and not self.cliente_listo_en_sillon:
                return False
                
            return True

    esperar_cliente_para_corte = atender_siguiente_cliente

    def finalizar_corte(self):
        with self.lock:
            self.corte_terminado = True
            self.cond_corte.notify()
            while self.silla_barbero_ocupada:
                self.cond_barbero.wait()

    def cerrar_barberia(self):
        with self.lock:
            self.barberia_abierta = False
            self.cond_barbero.notify_all()
            self.cond_sala_espera.notify_all()
            self.cond_corte.notify_all()


def hilo_barbero(barberia):
    while True:
        hay_cliente = barberia.atender_siguiente_cliente()
        if not hay_cliente:
            break
        print("✂️ [Barbero] Cortando el cabello...")
        time.sleep(random.uniform(0.05, 0.15))
        barberia.finalizar_corte()

def hilo_cliente(barberia, cliente_id):
    time.sleep(random.uniform(0.02, 0.1))
    barberia.entrar_cliente(cliente_id)

if __name__ == "__main__":
    print("=" * 60)
    print(" Barbería con Monitores y Variables de Condición (UNJu FI)")
    print("=" * 60)
    
    barberia = BarberiaMonitor(num_sillas_espera=3)
    
    t_barbero = threading.Thread(target=hilo_barbero, args=(barberia,), name="Barbero")
    t_barbero.start()
    
    clientes = []
    for i in range(1, 9):
        t_cli = threading.Thread(target=hilo_cliente, args=(barberia, i), name=f"Cliente-{i}")
        clientes.append(t_cli)
        t_cli.start()
        
    for t_cli in clientes:
        t_cli.join()
        
    time.sleep(0.2)
    barberia.cerrar_barberia()
    t_barbero.join()
    
    print("=" * 60)
    print(" Simulación de Barbería finalizada.")
    print("=" * 60)