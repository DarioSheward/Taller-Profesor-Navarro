import numpy as np      #importamos los paquetes a usar
import matplotlib.pyplot as plt
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
dtau=0.01   # paso temporal propuesto
tau=np.arange(0,t,dtau)     #array de tiempos

# creamos el archivo con los arrays



def A(theta):           
    M_x=np.mean(np.cos(theta))
    M_y=np.mean(np.sin(theta))
    return M_y*np.cos(theta)-M_x*np.sin(theta)


for t in tau:
    p=p + dtau*A(theta)*0.5
    theta=theta +   p*dtau    #0.01=p[1]-p[0] ayudaaaa quitenme la ia, sabe siempre lo que intento hacer 
    p=p + dtau*A(theta)*0.5    

