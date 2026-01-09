import numpy as np
import matplotlib.pyplot as plt
N=33
#theta= np.linspace(-1,1,N)
#p= np.linspace(-1,1,N)
theta,p=np.mgrid[-1:1:N*1j,-1:1:N*1j]
print( theta)
print( p)
theta=theta.flatten()
p=p.flatten()

print( theta)
print( p)