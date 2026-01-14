import numpy as np      #importamos los paquetes a usar
import matplotlib.pyplot as plt
import h5py
N=1000 #numero de particulas


theta= np.random.uniform(-np.pi,np.pi,N)   #inicializamos las particulas en theta y p

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

def periodicidad(theta):    #Seguramente es menos confuso no usar thetha.
    for i in range(len(theta)):
        
        if theta[i]<-np.pi:
            theta[i]=theta[i]+2*np.pi
        elif theta[i]>np.pi:
            theta[i]=theta[i]-2*np.pi    #Me da miedo que esto sea terrible para cambios muuuuy grandes que no deberian ocurrir.
            
    return theta
def M_y(theta):
    seno=np.sin(theta)
    M_y=np.mean(seno)
    return M_y, seno

def M_x(theta):
    coseno=np.cos(theta)
    M_x=np.mean(coseno)
    return M_x, coseno

#def A(theta):
#    return M_y(theta)[0]*M_y(theta)[1]-M_x(theta)[0]*M_x(theta)[1]
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
    dset_M_y[0,] = M_y(theta)[0]  # Guardamos el estado inicial
    dset_M_x = f.create_dataset('M_x', shape=(1,), maxshape=(None,), dtype='float64')
    dset_M_x[0,] = M_x(theta)[0]      # Guardamos el estado inicial

    for i in tem:
        # Guardamos los nuevos datos al final
        M_y_val = M_y(theta)
        M_x_val = M_x(theta)
        A=M_y_val[0]*M_y_val[1]-M_x_val[0]*M_x_val[1]
        p=p + dt*A*0.5
        theta=theta +   p*dt 
        theta=periodicidad(theta)   #0.01=p[1]-p[0] ayudaaaa quitenme la ia, sabe siempre lo que intento hacer 
        p=p + dt*A*0.5   

        dset_theta.resize(dset_theta.shape[1]+1, axis=1)
        dset_theta[:,-1] = theta

        dset_p.resize(dset_p.shape[1]+1, axis=1)
        dset_p[:,-1] = p
        
        dset_M_y.resize(dset_M_x.shape[0]+1, axis=0)
        dset_M_y[-1] = M_y_val[0]
        dset_M_x.resize(dset_M_x.shape[0]+1, axis=0)
        dset_M_x[-1] = M_x_val[0]
 #XCreo que no necesitamos guardar los valores de t sino que informar la cantidad de pasos dados... es mejor dejar un dataset dado ndjsndjs.

