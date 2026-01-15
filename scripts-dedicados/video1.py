import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation as fa
import h5py
import imageio_ffmpeg
from tqdm import tqdm  # Importamos tqdm

ruta_ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
plt.rcParams['animation.ffmpeg_path'] = ruta_ffmpeg

with h5py.File('./scripts-dedicados/data2.h5', 'r') as f:
    t = f['tiempo'][:]
    n_frames = t.shape[0]
    frames_to_process = int(n_frames*0.1) # Definimos la cantidad exacta

    fig, ax = plt.subplots(figsize=(8, 6))

    # --- INICIALIZACIÓN (QuadMesh) ---
    bins = 100
    range_lims = [[-np.pi, np.pi], [-2, 2]]
    theta0 = f['theta'][:, 0]
    p0 = f['p'][:, 0]
    
    # Creamos la gráfica base
    counts, xedges, yedges, quadmesh = ax.hist2d(
        theta0, p0, bins=bins, range=range_lims, cmap='plasma', cmin=1, vmin=1, vmax=50
    )

    ax.set_xlabel('Theta')
    ax.set_ylabel('p')
    title_artist = ax.set_title(f'Phase Space Evolution at time {t[0]:.2f}')
    cbar = plt.colorbar(quadmesh, ax=ax, label='Density')

    # --- FUNCIÓN UPDATE ---
    def update(frame):
        # Leemos datos
        theta = f['theta'][:, frame]
        p = f['p'][:, frame]
        
        # Calculamos histograma rápido con NumPy
        H, _, _ = np.histogram2d(theta, p, bins=bins, range=range_lims)
        H = H.T
        H[H < 1] = np.nan
        
        # Actualizamos la malla existente
        quadmesh.set_array(H.ravel())
        title_artist.set_text(f'Phase Space Evolution at time {t[frame]:.2f}')
        
        return quadmesh, title_artist

    # Creamos la animación (sin tqdm aquí)
    ani = fa(fig, update, frames=frames_to_process, interval=50, blit=True)

    # --- AQUÍ INTEGRAMOS LA BARRA DE PROGRESO ---
    print("Renderizando video...")
    
    # 1. Creamos la barra de tqdm con el total de frames
    bar = tqdm(total=frames_to_process, unit="frame")

    # 2. Definimos una función que Matplotlib llamará en cada frame
    def progress_callback(current_frame, total_frames):
        # Actualizamos la barra en 1 unidad cada vez
        bar.update(1)

    # 3. Pasamos esa función a ani.save
    ani.save(
        './scripts-dedicados/graficos/video_optimiza3.mp4', 
        writer='ffmpeg', 
        fps=30, 
        dpi=80,
        progress_callback=progress_callback  # <--- EL TRUCO
    )
    
    # 4. Cerramos la barra al finalizar para que no queden líneas sueltas en la consola
    bar.close()
    print("Video guardado exitosamente.")