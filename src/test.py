import matplotlib.pyplot as plt
import numpy as np

plt.style.use('_mpl-gallery')

t = np.arange(0.0, 2.0, 0.01)
s = np.sin(2 * np.pi * t)

fig, ax = plt.subplots()
ax.bar(t, s, width=1, edgecolor='white', linewidth=0.2)
ax.set(xticks=np.arange(-0.5, 2.5, 0.1))
# ax.grid(True, linestyle='-.')
ax.tick_params(labelcolor='r', labelsize='medium', width=3)

# plt.show()

plt.savefig('haha.png', dpi=500)