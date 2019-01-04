# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 11:26:32 2018

@author: USP
"""

from random  import randint
from sandpile_model import Table
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns

rows, cols = 8, 8
runs = 32

tab = Table(rows,cols)
tab.fill_randomly()

def animate(a):
    i, j = randint(0,tab.n_rows-1), randint(0,tab.n_cols-1)
    print('Dropping over ', (i,j))
    tab.drop_grain(i,j)
    #sns.heatmap(tab.grains_per_cell(),cmap='OrRd')
    plt.imshow(tab.grains_per_cell(),cmap='OrRd')

plt.rcParams['animation.ffmpeg_path'] = 'C:\\ffmpeg\\bin\\ffmpeg.exe'

Writer = animation.writers['ffmpeg']
writer = Writer(fps=10, metadata=dict(artist='Me'), bitrate=1800)

fig = plt.figure(figsize=(6,6))
plt.title('Sandpile')

anim = animation.FuncAnimation(fig,animate,frames=runs,repeat=True)
anim.save('sandpile.mp4', writer=writer)