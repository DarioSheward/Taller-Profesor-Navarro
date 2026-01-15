import h5py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
with h5py.File('replicacion_paper/output/data_caso2.h5', 'r') as f:
    # Acceder a variables específicas
    t=f['tiempo'][:]
    respuesta=input("¿Generar gráficos de Magnetizacion o Espacio de Fase (m/f): ")
    if respuesta.lower()=='m':
        M_y=f['M_y'][0:-1]
        M_x=f['M_x'][0:-1]
        M_T=np.sqrt(M_x**2+M_y**2)
        plt.figure(figsize=(10,6))
        plt.plot(t,M_x,label='M_x')
        plt.plot(t,M_y,label='M_y')
        plt.plot(t,M_T,label='M_T')
        plt.xlabel('Tiempo')
        plt.ylabel('Magnetización')
        plt.title('Evolución de la Magnetización en el Tiempo')
        plt.legend()
        plt.savefig('replicacion_paper/output/magnetizacion_caso2.png')
    elif respuesta.lower()=='f':
        for i in range(0,t.shape[0],100): # Queda buscar como poner el ... resuelto
            theta = f['theta'][:,i]
            p =f['p'][:,i]
            plt.hist2d(theta, p, bins=120, range=[[-np.pi,np.pi], [-2, 2]], cmap='plasma', cmin=1)  #Usemos cmin=1 para evitar problemas con bins vacíos    
            plt.xlabel('Theta') 
            plt.ylabel('p') 
            plt.title('Phase Space Evolution at step {}'.format(i))
            plt.colorbar(label='Density')   
            plt.savefig(f'replicacion_paper/output/phase_space_step_{i}.png')
            plt.clf()
#Recordar que los graficos iran dentro del loop