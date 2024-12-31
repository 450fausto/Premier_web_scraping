import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
import numpy as np


['Burnley', 'Brighton', 'Arsenal', 'Everton', 'Sheff Utd',
       'Newcastle', '"Bmouth"', 'Brentford', 'Chelsea', 'Man Utd',
       'N Forest', 'Man City', 'Tottenham', 'Wolves', 'Liverpool',
       'Fulham', 'West Ham', 'A Villa', 'C Palace', 'Luton']

encuentros = [
    ['C Palace', 'Brighton'],
    ['A Villa', 'Sheff Utd'],
    ['Man City', 'Brentford'],
    ['West Ham', 'Man Utd'],
    ['Tottenham', 'Everton'],
    ['N Forest', '"Bmouth"'],
    ['Fulham', 'Burnley'],
    ['Luton', 'Newcastle'],
    ['Liverpool', 'Arsenal'],
    ['Wolves', 'Chelsea']
]

def voronoi_finite_polygons_2d(vor, radius=None):
    """
    Reconstruct infinite voronoi regions in a 2D diagram to finite
    regions.
    Parameters
    ----------
    vor : Voronoi
        Input diagram
    radius : float, optional
        Distance to 'points at infinity'.
    Returns
    -------
    regions : list of tuples
        Indices of vertices in each revised Voronoi regions.
    vertices : list of tuples
        Coordinates for revised Voronoi vertices. Same as coordinates
        of input vertices, with 'points at infinity' appended to the
        end.
    """

    if vor.points.shape[1] != 2:
        raise ValueError("Requires 2D input")

    new_regions = []
    new_vertices = vor.vertices.tolist()

    center = vor.points.mean(axis=0)
    if radius is None:
        radius = vor.points.ptp().max()*2

    # Construct a map containing all ridges for a given point
    all_ridges = {}
    for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
        all_ridges.setdefault(p1, []).append((p2, v1, v2))
        all_ridges.setdefault(p2, []).append((p1, v1, v2))

    # Reconstruct infinite regions
    for p1, region in enumerate(vor.point_region):
        vertices = vor.regions[region]

        if all(v >= 0 for v in vertices):
            # finite region
            new_regions.append(vertices)
            continue

        # reconstruct a non-finite region
        ridges = all_ridges[p1]
        new_region = [v for v in vertices if v >= 0]

        for p2, v1, v2 in ridges:
            if v2 < 0:
                v1, v2 = v2, v1
            if v1 >= 0:
                # finite ridge: already in the region
                continue

            # Compute the missing endpoint of an infinite ridge

            t = vor.points[p2] - vor.points[p1] # tangent
            t /= np.linalg.norm(t)
            n = np.array([-t[1], t[0]])  # normal

            midpoint = vor.points[[p1, p2]].mean(axis=0)
            direction = np.sign(np.dot(midpoint - center, n)) * n
            far_point = vor.vertices[v2] + direction * radius

            new_region.append(len(new_vertices))
            new_vertices.append(far_point.tolist())

        # sort region counterclockwise
        vs = np.asarray([new_vertices[v] for v in new_region])
        c = vs.mean(axis=0)
        angles = np.arctan2(vs[:,1] - c[1], vs[:,0] - c[0])
        new_region = np.array(new_region)[np.argsort(angles)]

        # finish
        new_regions.append(new_region.tolist())

    return new_regions, np.asarray(new_vertices)

def voronoi(titulo, local, visit, mostrar=True, guardar=False, carpeta='.'):
    colores = []
    plt.figure()

    # Seri

    wx = (np.array([i[3] for i in gana[local]])+0.21377)/14.578
    wy = (np.array([i[2] for i in gana[local]])+0.34417)/22.896
    wx = 0.722881194858987*wx+0.690972342513970*wy
    wy = 6.5827*(-0.690972342513970*wx+0.722881194858987*wy)

    dx = (np.array([i[3] for i in empata[local]])+0.21377)/14.578
    dy = (np.array([i[2] for i in empata[local]])+0.34417)/22.896
    dx = 0.722881194858987*dx+0.690972342513970*dy
    dy = 6.5827*(-0.690972342513970*dx+0.722881194858987*dy)

    lx = (np.array([i[3] for i in pierde[local]])+0.21377)/14.578
    ly = (np.array([i[2] for i in pierde[local]])+0.34417)/22.896
    lx = 0.722881194858987*lx+0.690972342513970*ly
    ly = 6.5827*(-0.690972342513970*lx+0.722881194858987*ly)

    points = []
    points.extend([[wx[i], wy[i]] for i in range(len(wx))])
    # points.extend([[dx[i], dy[i]] for i in range(len(dx))])
    points.extend([[lx[i], ly[i]] for i in range(len(lx))])

    colores.extend(['lightgreen' for i in range(len(wx))])
    # points.extend(['gray' for i in range(len(dx))])
    colores.extend(['lightcoral' for i in range(len(lx))])

    vor = Voronoi(points)

    regions, vertices = voronoi_finite_polygons_2d(vor)
    i = 0
    for region in regions:
        polygon = vertices[region]
        plt.fill(*zip(*polygon), color=colores[i], edgecolor='black')
        i+=1

    vx = (tabla[local]-tabla[visit]+0.21377)/14.578
    vy = (dg[local]-dg[visit]+0.34417)/22.896
    vx = 0.722881194858987*vx+0.690972342513970*vy
    vy = 6.5827*(-0.690972342513970*vx+0.722881194858987*vy)

    plt.plot(wx, wy, '+', color='black', label='W')
    plt.plot(lx, ly, 'x', color='black', label='L')
    plt.plot(dx, dy, '.', color='black', label='D')
    plt.plot(vx, vy, 'o', color='yellow', label='V')
    plt.title(titulo)
    points.append([vx, vy])
    plt.xlim([np.array(points)[:,0].min()-0.2, np.array(points)[:,0].max()+0.2])
    plt.ylim([np.array(points)[:,1].min()-0.2, np.array(points)[:,1].max()+0.2])
    
    if mostrar:
        plt.show()
    if guardar:
        name = ''.join([i for i in titulo if i not in '".:'])
        plt.savefig(f'{carpeta}/{name}.jpg', format='jpeg', dpi=600)

df = pd.read_csv('premier_cleaned.csv')
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
df = df.sort_values(by='Date')

favor = {i:0 for i in df.local.unique()}
contra = {i:0 for i in df.local.unique()}
dg = {i:0 for i in df.local.unique()}
tabla = {i:0 for i in df.local.unique()}
w_local = {i:0 for i in df.local.unique()}
w_visit = {i:0 for i in df.local.unique()}

gana = {i:[] for i in df.local.unique()}
empata = {i:[] for i in df.local.unique()}
pierde = {i:[] for i in df.local.unique()}

for i in range(df.shape[0]):
    local = df.local[i]
    visit = df.visit[i]

    gl = df.g_loc[i]
    gv = df.g_vis[i]

    wl = gl>gv and ((favor[local]+favor[visit])>0 or (contra[local]+contra[visit])>0)
    dr = gl==gv and ((favor[local]+favor[visit])>0 or (contra[local]+contra[visit])>0)
    wv = gv>gl and ((favor[local]+favor[visit])>0 or (contra[local]+contra[visit])>0)

    if wl:
        gana[local].append([favor[local]-favor[visit], contra[local]-contra[visit], 
                            dg[local]-dg[visit], tabla[local]-tabla[visit], w_local[local]-w_visit[visit]])
        pierde[visit].append([favor[visit]-favor[local], contra[visit]-contra[local], 
                              dg[visit]-dg[local], tabla[visit]-tabla[local], w_visit[visit]-w_local[local]])
    elif dr:
        empata[local].append([favor[local]-favor[visit], contra[local]-contra[visit], 
                              dg[local]-dg[visit], tabla[local]-tabla[visit], w_local[local]-w_visit[visit]])
        empata[visit].append([favor[visit]-favor[local], contra[visit]-contra[local], 
                              dg[visit]-dg[local], tabla[visit]-tabla[local], w_visit[visit]-w_local[local]])
    elif wv:
        pierde[local].append([favor[local]-favor[visit], contra[local]-contra[visit], 
                              dg[local]-dg[visit], tabla[local]-tabla[visit], w_local[local]-w_visit[visit]])
        gana[visit].append([favor[visit]-favor[local], contra[visit]-contra[local], 
                            dg[visit]-dg[local], tabla[visit]-tabla[local], w_visit[visit]-w_local[local]])

    favor[local] += gl
    favor[visit] += gv
    contra[local] += gv
    contra[visit] += gl
    dg[local] += gl-gv
    dg[visit] += gv-gl
    tabla[local] += 3*int(gl>gv) + int(gl==gv)
    tabla[visit] += 3*int(gv>gl) + int(gl==gv)
    w_local[local] += 2*int(gl>gv) + int(gl==gv)
    w_visit[visit] += 2*int(gv>gl) + int(gl==gv)
    
for i in range(len(encuentros)):
    carpeta = 'Voronoi'
    local, visit = tuple(encuentros[i])
    titulo = f'{local} vs {visit} N'
    voronoi(titulo, local, visit, mostrar=False, guardar=True, carpeta=carpeta)

for i in range(len(encuentros)):
    carpeta = 'Voronoi'
    local, visit = tuple(encuentros[i])
    titulo = f'{local} vs {visit} R'
    voronoi(titulo, visit, local, mostrar=False, guardar=True, carpeta=carpeta)