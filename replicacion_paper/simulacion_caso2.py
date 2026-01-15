import numpy as np      #importamos los paquetes a usar
import matplotlib.pyplot as plt
import h5py
from tqdm import trange

N=1000 #numero de particulas
theta0=0.78
p0=1.90

theta= np.random.uniform(-theta0,theta0,N)   #inicializamos las particulas en theta y p


p= np.random.uniform(-p0,p0,N)
t=1000   # numero de pasos temporales
dt=0.1   # paso temporal propuesto
tem=np.arange(0,t,dt)


def periodicidad(dset):
    """
    Aplica condiciones periódicas de frontera directamente sobre un dataset h5py.
    Lee los datos, normaliza a [-pi, pi) y guarda los cambios en el disco.
    """
    # 1. Leemos todo el contenido del dataset a la memoria RAM
    #    El uso de [:] fuerza la carga de los datos.
    data = dset[:]
    
    # 2. Aplicamos la corrección matemática vectorizada
    data = (data + np.pi) % (2 * np.pi) - np.pi
    
    # 3. Escribimos los datos corregidos de vuelta al dataset en el disco
    #    Es CRUCIAL usar [:] a la izquierda para asignar dentro del archivo
    dset[:] = data
    
    # Retornamos el dataset por si quieres encadenar operaciones, 
    # aunque ya fue modificado en disco.
    return dset
def Mag(theta):
    seno=np.sin(theta)
    coseno=np.cos(theta)
    M_y=np.mean(seno)
    M_x=np.mean(coseno)
    Mag=np.hypot(M_x,M_y)
    return Mag, M_x, M_y, M_y*seno-M_x*coseno
#def A(theta):
#    return M_y(theta)[0]*M_y(theta)[1]-M_x(theta)[0]*M_x(theta)[1]
# creamos el archivo con los arrays
with h5py.File('replicacion_paper/output/data_caso2.h5', 'w') as f:
    # Creamos el dataset inicial (0 filas, N columnas)
    # maxshape=(None, 10) permite filas infinitas

    dset_theta = f.create_dataset('theta', shape=(N, 0), maxshape=(N, None), dtype='float64')
    dset_theta[:,] = theta  # Guardamos el estado inicial
    
    dset_tiempo= f.create_dataset('tiempo', data=tem, dtype='float64')  #aun por implementar
    dset_tiempo=tem
    dset_p = f.create_dataset('p', shape=(N, 0), maxshape=(N, None), dtype='float64')
    dset_p[:,] = p  # Guardamos el estado inicial
    Mag_val=Mag(theta)
    dset_M_y = f.create_dataset('M_y', shape=(1,), maxshape=(None,), dtype='float64')
    dset_M_y[0,] = Mag_val[2]  # Guardamos el estado inicial
    dset_M_x = f.create_dataset('M_x', shape=(1,), maxshape=(None,), dtype='float64')
    dset_M_x[0,] = Mag_val[1]      # Guardamos el estado inicial
    dset_Mag = f.create_dataset('Mag', shape=(1,), maxshape=(None,), dtype='float64')
    
    for i in trange(len(tem)):
        # Guardamos los nuevos datos al final
        Mag_val=Mag(theta)
        p=p + dt*Mag_val[3]*0.5
        theta=theta +   p*dt 
        p=p + dt*Mag_val[3]*0.5   

        dset_theta.resize(dset_theta.shape[1]+1, axis=1)
        dset_theta[:,-1] = theta

        dset_p.resize(dset_p.shape[1]+1, axis=1)
        dset_p[:,-1] = p
        dset_Mag.resize(dset_Mag.shape[0]+1, axis=0)
        dset_Mag[-1] = Mag_val[0]
        dset_M_y.resize(dset_M_y.shape[0]+1, axis=0)
        dset_M_y[-1] = Mag_val[2]
        dset_M_x.resize(dset_M_x.shape[0]+1, axis=0)
        dset_M_x[-1] = Mag_val[1]

    dset_theta[:]= periodicidad(dset_theta)
    
 #XCreo que no necesitamos guardar los valores de t sino que informar la cantidad de pasos dados... es mejor dejar un dataset dado ndjsndjs.

