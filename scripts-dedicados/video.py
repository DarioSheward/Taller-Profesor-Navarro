import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation as fa
import h5py
import imageio_ffmpeg
ruta_ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
plt.rcParams['animation.ffmpeg_path'] = ruta_ffmpeg
with h5py.File('./scripts-dedicados/data.h5', 'r') as f:
    t = f['tiempo'][:]
    n_frames = t.shape[0]
    
    fig, ax = plt.subplots(figsize=(8, 6))

    def update(frame):
        ax.clear()
        theta = f['theta'][:, frame]
        p = f['p'][:, frame]
        h = ax.hist2d(theta, p, bins=120, range=[[-np.pi, np.pi], [-2, 2]], cmap='plasma', cmin=1 , cmax=10)
        ax.set_xlabel('Theta')
        ax.set_ylabel('p')
        ax.set_title(f'Phase Space Evolution at time {t[frame]:.2f}')
        return h
    ani = fa(fig, update, frames=n_frames, blit=False, repeat=False)

    mappable = plt.cm.ScalarMappable(cmap='plasma', norm=plt.Normalize(vmin=1, vmax=10))
    mappable.set_array([])

    cbar = plt.colorbar(mappable, ax=ax, label='Density')

    ani.save('./scripts-dedicados/graficos/video0.mp4', writer='ffmpeg', fps=30, dpi=60, extra_args=['-vcodec', 'libx264', '-pix_fmt', 'yuv420p'])