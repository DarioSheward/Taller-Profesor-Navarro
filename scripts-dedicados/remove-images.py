import os
for i in range(0,10000,100):
    if os.path.exists(f'scripts-dedicados/graficos/phase_space_step_{i}.png'):
        os.remove(f'scripts-dedicados/graficos/phase_space_step_{i}.png')