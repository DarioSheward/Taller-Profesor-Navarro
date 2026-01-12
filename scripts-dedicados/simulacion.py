import numpy as np      #importamos los paquetes a usar
import matplotlib.pyplot as plt
import h5py
N=1000 #numero de particulas

#metodo randomizado respecto a una referencia.
theta= np.random.triangular(left=-np.pi, mode=0, right=np.pi, size=N)

#p= np.random.default_rng(-1,1,N)

#todas las particulas juntas
#theta= np.linspace(-1,1,N)
#p= np.linspace(-1,1,N)
# metodo de grid homogeneo
# theta,p=np.mgrid[-1:1:N*1j,-1:1:N*1j]
# theta=theta.flatten()
# p=p.flatten()
p=np.mgrid[-1:1:N*1j]
p=p.flatten()

t=100   # numero de pasos temporales
dt=0.01   # paso temporal propuesto
tem=np.arange(0,t,dt)


def M_y(theta):
    M_y=np.mean(np.sin(theta))
    return M_y

def M_x(theta):
    M_x=np.mean(np.cos(theta))
    return M_x

def A(theta):
    return M_y(theta)*np.cos(theta)-M_x(theta)*np.sin(theta)
# creamos el archivo con los arrays
with h5py.File('scripts-dedicados/data.h5', 'w') as f:
    # Creamos el dataset inicial (0 filas, N columnas)
    # maxshape=(None, 10) permite filas infinitas
    dset_theta = f.create_dataset('theta', shape=(N, 0), maxshape=(N, None), dtype='float64')
    dset_theta[:,] = theta  # Guardamos el estado inicial
    
    dset_tiempo= f.create_dataset('tiempo', data=tem, dtype='float64')  #aun por implementar
    dset_tiempo=tem
    dset_p = f.create_dataset('p', shape=(N, 0), maxshape=(N, None), dtype='float64')
    dset_p[:,] = p  # Guardamos el estado inicial
    dset_M_y = f.create_dataset('M_y', shape=(1,), maxshape=(None,), dtype='float64')
    dset_M_y[0,] = M_y(theta)  # Guardamos el estado inicial
    dset_M_x = f.create_dataset('M_x', shape=(1,), maxshape=(None,), dtype='float64')
    dset_M_x[0,] = M_x(theta)  # Guardamos el estado inicial

    for i in tem:
        # Guardamos los nuevos datos al final
        p=p + dt*A(theta)*0.5
        theta=theta +   p*dt    #0.01=p[1]-p[0] ayudaaaa quitenme la ia, sabe siempre lo que intento hacer 
        p=p + dt*A(theta)*0.5   

        dset_theta.resize(dset_theta.shape[1]+1, axis=1)
        dset_theta[:,-1] = theta

        dset_p.resize(dset_p.shape[1]+1, axis=1)
        dset_p[:,-1] = p
        
        dset_M_y.resize(dset_M_x.shape[0]+1, axis=0)
        dset_M_y[-1] = M_y(theta)

        dset_M_x.resize(dset_M_x.shape[0]+1, axis=0)
        dset_M_x[-1] = M_x(theta)

    f.close()
 #XCreo que no necesitamos guardar los valores de t sino que informar la cantidad de pasos dados... es mejor dejar un dataset dado ndjsndjs.

