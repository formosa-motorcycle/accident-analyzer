import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
from pathlib import Path


# # Fixing random state for reproducibility
# np.random.seed(19680801)
plt.style.use('fivethirtyeight')


fig, ax = plt.subplots()
# ax.scatter

N = 9
r0 = 0.6
x = []
y = []
for i in range(1, 7, 2):
    for j in range(1, 7, 2):
        x.append(i)
        y.append(j)
# x = 0.9 * np.random.rand(N)
# y = 0.9 * np.random.rand(N)
area = (60 * np.random.rand(N))**2  # 0 to 10 point radii
c = np.sqrt(area)
# r = np.sqrt(x ** 2 + y ** 2)
# area1 = np.ma.masked_where(r < r0, area)
# area2 = np.ma.masked_where(r >= r0, area)
# plt.scatter(x, y, s=area1, marker='^', c=c)
ax.scatter(x, y, s=area, marker='o', c=c)
# Show the boundary between the regions:
# theta = np.arange(0, np.pi / 2, 0.01)
# plt.plot(r0 * np.cos(theta), r0 * np.sin(theta))
# plt.a

ax.set_xticks([0,2,4,6])
ax.set_xticks([1, 3, 5], labels=['汽車', '機車', '自行車'], minor=True, font=Path('TaipeiSansTCBeta-Regular.ttf'))

ax.xaxis.set_major_formatter(ticker.NullFormatter())
# ax.xaxis.set_minor_formatter(dates.DateFormatter('%b'))

for tick in ax.xaxis.get_minor_ticks():
    tick.tick1line.set_markersize(0)
    tick.tick2line.set_markersize(0)
    tick.label1.set_horizontalalignment('center')
ax.xaxis.tick_top()

ax.invert_yaxis()

ax.set_yticks([0,2,4,6])
ax.set_yticks([1, 3, 5], labels=['汽車', '機車', '自行車'], minor=True, font=Path('TaipeiSansTCBeta-Regular.ttf'))

ax.yaxis.set_major_formatter(ticker.NullFormatter())
# ax.yaxis.set_minor_formatter(dates.DateFormatter('%b'))

for tick in ax.yaxis.get_minor_ticks():
    tick.tick1line.set_markersize(0)
    tick.tick2line.set_markersize(0)
    tick.label1.set_verticalalignment('center')

ax.grid(True)
fig.tight_layout()

plt.show()