import h5py
import numpy as np
import matplotlib.pyplot as plt

with h5py.File('./scripts-dedicados/data.h5', 'r') as f:
    # Acceder a variables específicas
    t=f['tiempo'][:]

    for i in range(len(t)):
        theta = f['theta'][i,:]
        p = f['p'][i,:]
        print(theta.shape, p.shape)
    plt.hist2d(theta, p, bins=120, range=[[-np.pi,np.pi], [-2, 2]], cmap='plasma', cmin=1)  #Usemos cmin=1 para evitar problemas con bins vacíos    
    plt.xlabel('Theta') 
    plt.ylabel('p') 
    plt.title('Phase Space Evolution at step {}'.format(i))
    plt.colorbar(label='Density')   
    plt.show()
#Recordar que los graficos iran dentro del loop