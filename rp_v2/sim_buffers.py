#Este código fue creado por Gemini
import numpy as np
import h5py
from tqdm import tqdm # Usamos tqdm para una barra de carga real

# --- Parámetros ---
N = 1000 
theta0 = 0.78
p0 = 1.39
t_total = 100     
dt = 0.01

# Definición temporal
atem = np.arange(0, t_total, dt)
total_steps = len(atem)

# Buffer: Cantidad de pasos a guardar en RAM antes de volcar al disco
# 1000 pasos es un buen equilibrio entre velocidad y memoria RAM.
BUFFER_SIZE = 1000 

print(f"Pasos totales: {total_steps}. Guardando cada {BUFFER_SIZE} pasos.")

# --- Funciones (Optimizadas con Numba si fuera necesario, pero Numpy va bien) ---
def get_forces(theta):
    seno = np.sin(theta)
    coseno = np.cos(theta)
    M_y = np.mean(seno)
    M_x = np.mean(coseno)
    Mag = np.hypot(M_x, M_y)
    force = M_y * seno - M_x * coseno
    return Mag, M_x, M_y, force

# --- Inicialización ---
theta = np.random.uniform(-theta0, theta0, N)
p = np.random.uniform(-p0, p0, N)

# Pre-cálculo inicial
mag, mx, my, force = get_forces(theta)

print("Iniciando simulación...")

# Usamos 'w' para crear archivo nuevo.
with h5py.File('rp_v2/output/data_casoprueba_opt.h5', 'w') as f:
    
    # 1. Creamos datasets CON EL TAMAÑO TOTAL RESERVADO
    # Esto puede tardar unos segundos si el archivo es gigante (GBs), 
    # pero es necesario para la estructura contigua.
    print("Asignando espacio en disco...")
    dset_theta = f.create_dataset('theta', shape=(N, total_steps), dtype='float64')
    dset_p = f.create_dataset('p', shape=(N, total_steps), dtype='float64')
    
    dset_Mag = f.create_dataset('Mag', shape=(total_steps,), dtype='float64')
    dset_Mx = f.create_dataset('M_x', shape=(total_steps,), dtype='float64')
    dset_My = f.create_dataset('M_y', shape=(total_steps,), dtype='float64')
    
    # Guardamos el tiempo de una vez (es rápido)
    f.create_dataset('tiempo', data=atem)

    # 2. Guardamos Condición Inicial (Índice 0)
    dset_theta[:, 0] = theta
    dset_p[:, 0] = p
    dset_Mag[0] = mag
    dset_Mx[0] = mx
    dset_My[0] = my

    # --- BUCLE POR BLOQUES (BUFFER) ---
    # Esto elimina el cuello de botella de I/O
    
    current_step = 1 # Empezamos en 1 porque 0 ya está guardado
    pbar = tqdm(total=total_steps-1, desc="Simulando")

    while current_step < total_steps:
        # Calculamos cuántos pasos hacer en esta tanda
        steps_to_run = min(BUFFER_SIZE, total_steps - current_step)
        
        # Arrays temporales en RAM (rápidos)
        buff_theta = np.zeros((N, steps_to_run))
        buff_p = np.zeros((N, steps_to_run))
        buff_mag = np.zeros(steps_to_run)
        buff_mx = np.zeros(steps_to_run)
        buff_my = np.zeros(steps_to_run)

        # Bucle de cálculo intensivo (sin tocar el disco)
        for i in range(steps_to_run):
            # Velocity Verlet
            p = p + dt * force * 0.5
            theta = theta + p * dt
            
            # Periodicidad INLINE (mucho más rápido que llamar a función)
            # theta = (theta + np.pi) % (2 * np.pi) - np.pi 
            # Nota: Si no necesitas periodicidad estricta para el cálculo de fuerzas (sen/cos ya son periódicos),
            # puedes saltarte esto para ganar velocidad y aplicarlo solo al graficar.
            
            mag, mx, my, force = get_forces(theta)
            p = p + dt * force * 0.5
            
            # Guardar en buffer
            buff_theta[:, i] = theta
            buff_p[:, i] = p
            buff_mag[i] = mag
            buff_mx[i] = mx
            buff_my[i] = my

        # VOLCADO A DISCO (Una sola escritura grande)
        end_step = current_step + steps_to_run
        
        dset_theta[:, current_step:end_step] = buff_theta
        dset_p[:, current_step:end_step] = buff_p
        dset_Mag[current_step:end_step] = buff_mag
        dset_Mx[current_step:end_step] = buff_mx
        dset_My[current_step:end_step] = buff_my
        
        current_step += steps_to_run
        pbar.update(steps_to_run)

    pbar.close()
    print("\n¡Simulación terminada!")