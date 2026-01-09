import numpy as np
import matplotlib.pyplot as plt
N=100
#theta= np.linspace(-1,1,N)
#p= np.linspace(-1,1,N)
theta,p=np.mgrid[-1:1:N*1j,-1:1:N*1j]
theta=theta.flatten()
p=p.flatten()

t=100
dtau=0.01
tau=np.arange(0,t,dtau)

def A(theta):
    M_x=np.mean(np.cos(theta))
    M_y=np.mean(np.sin(theta))
    return M_y*np.cos(theta)-M_x*np.sin(theta)

#Definir funcion M_x y M_y
for t in tau:
    p=p + dtau*A(theta)*0.5
    theta=theta +   p*dtau    #0.01=p[1]-p[0] ayudaaaa quitenme la ia, sabe siempre lo que intento hacer 
    p=p + dtau*A(theta)*0.5    

    
plt.hist2d(theta, p, bins=120, range=[[-np.pi,np.pi], [-2, 2]], cmap='plasma', cmin=1)  #Usemos cmin=1 para evitar problemas con bins vacíos    
plt.xlabel('Theta')
plt.ylabel('p')
plt.title('Phase Space Evolution')
plt.colorbar(label='Density')
plt.show()