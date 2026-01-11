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
tem=np.arange(0,t,dt)     #array de tiempos

def M_y(theta):
    M_y=np.mean(np.sin(theta))
    return M_y

def M_x(theta):
    M_x=np.mean(np.cos(theta))
    return M_x

def A(theta):           
    return M_y(theta)*np.cos(theta)-M_x(theta)*np.sin(theta)
# creamos el archivo con los arrays
with h5py.File('scripts-dedicados/data', 'w') as f:
    # Creamos el dataset inicial (0 filas, N columnas)
    # maxshape=(None, 10) permite filas infinitas
    dset_theta = f.create_dataset('theta', shape=(0, N), maxshape=(None, N), dtype='float32')
    

    dset_p = f.create_dataset('p', shape=(0, N), maxshape=(None, N), dtype='float32')
    
    dset_M_y = f.create_dataset('M_y', shape=(0,), maxshape=(None,), dtype='float32')
    

    dset_M_x = f.create_dataset('M_x', shape=(0,), maxshape=(None,), dtype='float32')
    
    for i in range(t+1):
        # Guardamos los nuevos datos al final
        dset_theta.resize(dset_theta.shape[0]+theta.shape[0], axis=0)
        dset_theta[-1] = theta

        dset_p.resize(dset_p.shape[0]+p.shape[0], axis=0)
        dset_p[-1] = p

        dset_M_y.resize(dset_M_y.shape[0]+1, axis=0)
        dset_M_y[-1] = M_y(theta)

        dset_M_x.resize(dset_M_x.shape[0]+1, axis=0)
        dset_M_x[-1] = M_x(theta)
        p=p + dt*A(theta)*0.5
        theta=theta +   p*dt    #0.01=p[1]-p[0] ayudaaaa quitenme la ia, sabe siempre lo que intento hacer 
        p=p + dt*A(theta)*0.5   


 

