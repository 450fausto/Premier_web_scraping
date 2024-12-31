import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def BarrasApiladas(titulo, loc, vis, mostrar=True, guardar=False, carpeta='.'):
    # Datos de ejemplo
    categorias = ['Gana', 'Empata', 'Pierde']

    # Crear gráfico de barras apiladas
    fig, ax = plt.subplots()

    # Barras apiladas
    barra1 = ax.bar(categorias, loc, label='como Local')
    barra2 = ax.bar(categorias, vis, bottom=loc, label='como Visitante')

    # Configuraciones adicionales
    ax.set_xlabel('Resultados')
    ax.set_ylabel('Frecuencia')
    ax.set_title(titulo)
    ax.legend()

    ax.spines['top'].set_visible(False)  # Desactiva el borde superior
    ax.spines['right'].set_visible(False)  # Desactiva el borde derecho
    ax.spines['bottom'].set_visible(True)  # Desactiva el borde inferior
    ax.spines['left'].set_visible(True)  # Desactiva el borde izquierdo

    if mostrar:
        plt.show()

    if guardar:
       name = ''.join([i for i in titulo if i not in '".:'])
       fig.savefig(f'{carpeta}/{name}.jpg', format='jpeg', dpi=600)


df = pd.read_csv('premier_cleaned.csv')

local_names = df.local.unique()
visit_names = df.visit.unique()

locales = {i:[0,0,0] for i in local_names}
visitantes = {i:[0,0,0] for i in visit_names}

for i in range(df.shape[0]):
    local = df.local[i]
    visit = df.visit[i]

    gl = df.g_loc[i]
    gv = df.g_vis[i]

    if gl>gv:
        locales[local][0] += 1
        visitantes[visit][2] += 1
    elif gl==gv:
        locales[local][1] += 1
        visitantes[visit][1] += 1
    elif gv>gl:
        locales[local][2] += 1
        visitantes[visit][0] += 1

for equipo in visitantes.keys():
    titulo = f'Desempeño del {equipo}'
    dir = 'Barras_Apiladas'
    BarrasApiladas(titulo, 
                locales[equipo], 
                visitantes[equipo], 
                mostrar=False, guardar=True, carpeta=dir)
