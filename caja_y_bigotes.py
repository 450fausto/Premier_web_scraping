import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def CajaBigotes(titulo, nombre1, serie1, nombre2, serie2, mostrar=True, guardar=False, carpeta='.'):
    serie1 = pd.Series(serie1)
    serie2 = pd.Series(serie2)

    nombre1 += f': \n{len(serie1)} goles'
    nombre2 += f': \n{len(serie2)} goles'

    nombre_del_eje_x = 'minutos del juego'
    titulo_del_grafico = titulo

    # De aquí para abajo no recomiendo modificar

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=False, figsize=(12, 7), gridspec_kw={'hspace': 0.4})

    ax1.boxplot(serie1, vert=False, manage_ticks=True, showfliers=True)
    ax2.boxplot(serie2, vert=False, manage_ticks=True, showfliers=True)

    ax2.set_xlabel(nombre_del_eje_x, fontsize=12)
    ax1.set_yticks([1])
    ax2.set_yticks([1])

    ax1.set_yticklabels([nombre1], fontsize=12)
    ax2.set_yticklabels([nombre2], fontsize=12)

    cuartiles1 = np.quantile(serie1, np.array([0.00, 0.25, 0.50, 0.75, 1.00])).round(2)
    cuartiles2 = np.quantile(serie2, np.array([0.00, 0.25, 0.50, 0.75, 1.00])).round(2)

    inferior = -5 #np.floor(np.min([cuartiles1.min(), cuartiles2.min()]))
    superior = 95# np.ceil(np.max([cuartiles1.max(), cuartiles2.max()]))

    ax1.vlines(cuartiles1, [0] * cuartiles1.size, [1] * cuartiles1.size, color='b', ls=':', lw=1, zorder=0)
    ax2.vlines(cuartiles2, [0] * cuartiles2.size, [1] * cuartiles2.size, color='b', ls=':', lw=1, zorder=0)

    ax1.set_ylim(0.5, 1.5)
    ax1.set_xlim(inferior,superior)

    ax2.set_ylim(0.5, 1.5)
    ax2.set_xlim(inferior,superior)

    xtick_labels1 = [str(q) for q in cuartiles1]
    xtick_labels2 = [str(q) for q in cuartiles2]

    ax1.set_xticks(cuartiles1)
    ax2.set_xticks(cuartiles2)

    ax1.set_xticklabels(xtick_labels1, rotation=90)
    ax2.set_xticklabels(xtick_labels2, rotation=90)

    ax1.plot([serie1.mean()], [1], 'xr')
    ax2.plot([serie2.mean()], [1], 'xr')

    ax1.spines['top'].set_visible(False)  # Desactiva el borde superior
    ax1.spines['right'].set_visible(False)  # Desactiva el borde derecho
    ax1.spines['bottom'].set_visible(True)  # Desactiva el borde inferior
    ax1.spines['left'].set_visible(True)  # Desactiva el borde izquierdo

    ax2.spines['top'].set_visible(False)  # Desactiva el borde superior
    ax2.spines['right'].set_visible(False)  # Desactiva el borde derecho
    ax2.spines['bottom'].set_visible(True)  # Desactiva el borde inferior
    ax2.spines['left'].set_visible(True)  # Desactiva el borde izquierdo

    # ax.axvline(x=sr.mean(), color='r', linestyle='--', label='Media', linewidth=0.5)

    ax1.set_title(titulo_del_grafico, # Título del gráfico
                fontsize=14, # Tamaño de letra del título
                loc='center') # Localización del título: 'left' 'center' 'right
    
    if mostrar:
        plt.show()

    if guardar:
       name = ''.join([i for i in titulo if i not in '".:'])
       fig.savefig(f'{carpeta}/{name}.jpg', format='jpeg', dpi=600)


df = pd.read_csv('premier_cleaned.csv')

local_names = df.local.unique()
visit_names = df.visit.unique()

minutes_local = {i:[] for i in local_names}
minutes_visit = {i:[] for i in visit_names}

anota = {i:[] for i in local_names}
recibe = {i:[] for i in local_names}

for i in range(df.shape[0]):
    local = df.local[i]
    visit = df.visit[i]

    if df.m_loc[i]!='[]':
      ml = [int(j) for j in df.m_loc[i][1:-1].split(',')]
    else:
      ml = []
    if df.m_vis[i]!='[]':
      mv = [int(j) for j in df.m_vis[i][1:-1].split(',')]
    else:
      mv = []

    minutes_local[local].extend(ml)
    minutes_visit[visit].extend(mv)

    anota[local].extend(ml)
    anota[visit].extend(mv)

    recibe[local].extend(mv)
    recibe[visit].extend(ml)

for i in minutes_local.keys():
    titulo = f'Goles anotados y recibidos: {i}'
    dir = 'CB_antados_recibidos'
    CajaBigotes(titulo, 
                'Anota', anota[i], 
                'Le anotan', recibe[i], 
                mostrar=False, guardar=True, carpeta=dir)

for i in minutes_local.keys():
    titulo = f'Goles de local y de visitante: {i}'
    dir = 'CB_local_visitante'
    CajaBigotes(titulo, 
                'Local', minutes_local[i], 'Visitante', minutes_visit[i], 
                mostrar=False, guardar=True, carpeta=dir)