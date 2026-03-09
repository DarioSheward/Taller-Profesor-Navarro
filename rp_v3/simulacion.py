#Importamos las librerias necesarias
import numpy as np
import h5py as h5
#from tqdm import trange
from tqdm import tqdm
import os

#Las condiones iniaciales se obtienen a traves de un archivo con columnas definidass como:
#N , theta0 , p0 , t , dt , distribucion theta , distribucion p.

#Creo que la idea sería hacer un script que genere las condiciones inic. deseadas y las guarde, 
#pero tambien genere un .txt que actualice los parametros.a .h5 a traves de un script similar o el mismo.
def abrir_con_listdir(ruta_carpeta):
    # Listamos y filtramos archivos que terminen en .h5
    archivos = [f for f in os.listdir(ruta_carpeta) if f.endswith('.h5')]

    if len(archivos) == 1:
        ruta_completa = os.path.join(ruta_carpeta, archivos[0])

        nombre_archivo = os.path.basename(ruta_completa).replace(".h5", "")
        partes = nombre_archivo.split("_")
        return h5.File(ruta_completa, 'r'), int(partes[3])
    #Nomenclatura esperada: rp_v3/input/civ_N.h5
    # Manejo de errores igual al ejemplo anterior...
    elif len(archivos) == 0:
        print("No se encontraron archivos .h5")
    else:
        print(f"Error: Se encontraron {len(archivos)} archivos. No sé cuál abrir.")
    return None

def distribucion(dis, low, high, size):
    if dis == 'u':  #waterbag
        return np.random.uniform(low, high, size)

def Mag(theta):
    seno=np.sin(theta)
    coseno=np.cos(theta)
    M_y=np.mean(seno)
    M_x=np.mean(coseno)
    Mag=np.hypot(M_x,M_y)
    return Mag, M_x, M_y, M_y*seno-M_x*coseno

ruta_carpeta = 'rp_v3/input'  # Carpeta donde buscar el archivo .h5
archivo_h5, v_ci = abrir_con_listdir(ruta_carpeta)

BUFFER_SIZE = 1000  # Número de pasos temporales a guardar en RAM antes de volcar a disco

for i in range(v_ci):
    with abrir_con_listdir(ruta_carpeta)[0] as f_ini:
        N = int(f_ini['N'][(i)])
        theta0 = float(f_ini['theta0'][(i)])
        p0 = float(f_ini['p0'][(i)])
        t_total = float(f_ini['t'][(i)])
        dt = float(f_ini['dt'][(i)])
    
        distrib_theta = f_ini['distribucion_theta'][()].decode('utf-8')
        distrib_p = f_ini['distribucion_p'][()].decode('utf-8')
    f_ini.close()
    theta= distribucion(distrib_theta, -theta0, theta0, N)
    p= distribucion(distrib_p, -p0, p0, N)
    atem= np.arange(0,t_total,dt)
    total_steps=len(atem)



    with h5.File(f'rp_v3/output/data_{theta0}_{p0}_{t_total}_{dt}.h5', 'w') as f:
        
        # 1. Creamos datasets CON EL TAMAÑO TOTAL RESERVADO
        # Esto puede tardar unos segundos si el archivo es gigante (GBs), 
        # pero es necesario para la estructura contigua.
        print("Asignando espacio en disco...")
        dset_theta = f.create_dataset('theta', shape=(N, total_steps), dtype='float64')
        dset_p = f.create_dataset('p', shape=(N, total_steps), dtype='float64')
        
        mag, mx, my, force = Mag(theta)

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
                
                mag, mx, my, force = Mag(theta)
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