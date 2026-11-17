from matplotlib.pyplot import *
from numpy import *
from numpy.linalg import *
from time import *        

import os
import naive_search
import voxel_grid
import kd_tree


def loadPoints(file):
    #Load file
    X, Y, Z = [], [], [] ;

    with open(file) as f:

        for line in f:
            x, y, z = line.split('\t')

            X.append(float(x))
            Y.append(float(y))
            Z.append(float(z))

    return X, Y, Z


def drawPoints(X, Y, Z, bx, transp = 0.2):
    # Create figure
    fig = figure()
    ax = axes(projection = "3d")
    ax.set_aspect("equal")

    #Compute sphere scale: 1 pix = 25.4 mm
    scale = 1
    if bx > 0:
        scale = int(bx * bx * 40 * 40)

    #Plot points
    ax.scatter(X, Y, Z, s=scale, alpha = transp)

    show()


def drawVoxels(x_min, y_min, z_min, dx, dy, dz, V):
    # Create figure
    fig = figure()
    ax = axes(projection = "3d")
    ax.set_aspect("equal")

    #Create meshgrid
    xedges = linspace(x_min, x_min + dx, n_r+1)
    yedges = linspace(y_min, y_min + dy, n_r+1)
    zedges = linspace(z_min, z_min + dz, n_r+1)

    VX, VY, VZ = meshgrid(xedges, yedges, zedges,  indexing="ij")

    #Draw voxels
    ax.voxels(VX, VY, VZ, V, edgecolor="k")

    show()


def computeDensity(X, Y, Z, search):
    #Spatial density of the whole cloud
    n = len(X)
    sum_dist = 0

    for i in range(n):

        #Take two nearest points: [(distance, index), (distance, index)] 
        #Two because the nearest one can be a duplicate of the point at the distance 0
        neighbours = search(i, 2)

        #Take the nearest neighbour with the distance greater than zero
        for distance, j in neighbours:
            if distance > 0:
                sum_dist += distance
                break

    #Average distance and density
    d_aver = sum_dist / n
    rho = 1 / d_aver**3

    return d_aver, rho


def computeCurvaturePoint(i, X, Y, Z, search, k = 30):
    #Curvature of one point: kappa = l1 / (l1 + l2 + l3), l1 <= l2 <= l3
    #l1, l2, l3 are the eigenvalues of the covariance matrix of the point and its neighbours

    #Neighbourhood of the point i (distance, index) of the k nearest neighbours
    neighbours = search(i, k)              
    indices = [i]                           
    for distance, j in neighbours:
        indices.append(j)
    m = len(indices)                        #number of points (k + 1)

    #Coordinates of the points in the neighbourhood
    xs, ys, zs = [], [], []
    for j in indices:
        xs.append(X[j])
        ys.append(Y[j])
        zs.append(Z[j])

    #Centre of the neighbourhood: mean of the coordinates
    x_mean = sum(xs) / m
    y_mean = sum(ys) / m
    z_mean = sum(zs) / m

    #Covariance matrix of the neighbourhood
    sxx, syy, szz = 0, 0, 0                 #for the variances (x with x, y with y, z with z)
    sxy, sxz, syz = 0, 0, 0                 #for the covariances (x with y, x with z, y with z)

    for j in range(m):
        dx = xs[j] - x_mean
        dy = ys[j] - y_mean
        dz = zs[j] - z_mean

        sxx += dx * dx
        syy += dy * dy
        szz += dz * dz
        sxy += dx * dy
        sxz += dx * dz
        syz += dy * dz

    a11, a22, a33 = sxx / (m - 1), syy / (m - 1), szz / (m - 1)         #variances
    a12, a13, a23 = sxy / (m - 1), sxz / (m - 1), syz / (m - 1)         #covariances

    M = array([[a11, a12, a13],
               [a12, a22, a23],
               [a13, a23, a33]])            #symmetric matrix 3 x 3

    #Eigenvalues of the matrix (real, in ascending order)
    l = eigvalsh(M)

    #Curvature: the smallest eigenvalue divided by the sum of all three
    kappa = l[0] / (l[0] + l[1] + l[2])

    return kappa


def computeCurvature(X, Y, Z, search, k = 30):
    #Curvature of all points
    kappa = zeros(len(X))

    for i in range(len(X)):
        kappa[i] = computeCurvaturePoint(i, X, Y, Z, search, k)

    return kappa

#Load points
folder = os.path.dirname(os.path.abspath(__file__))
X, Y, Z = loadPoints(os.path.join(folder, "tree_18.txt"))
n = len(X)
print("Number of points:", n)

#Draw points
drawPoints(X, Y, Z, 0, 0.2)

#Methods: the naive search takes about 2 minutes, Octree and Rtree are just prepared for possible implementation
run_naive = True
use_octree = False
use_rtree = False


#Spatial indices (data preparation fo r naive search, voxel grid and the kd-tree (AI generated for cleaner data preparation and integration with the rest of the code))

#Voxel grid: n_r voxels in every axis, about 3 points in a voxel
#H: voxel -> points inside it, J: point -> voxel in which it lies
n_r = int(round((n / 3)**(1/3)))
H, J, n_r, box = voxel_grid.createSpatialIDXs(X, Y, Z, n_r)
x_min, y_min, z_min, dx, dy, dz = box

#kd-tree: the points are divided by the median in the axes x, y, z, x,... until a leaf has at most 16 points
tree = kd_tree.KDTree([X, Y, Z], 16)

#Octree: the box of the points is divided to 8 equal boxes until a leaf has at most 16 points
if use_octree:
    otree = octree.Octree([X, Y, Z], 16)

#R-tree: near points are grouped to nodes with a min-max box 16 items in a node at most
if use_rtree:
    rtree = r_tree.RTree([X, Y, Z], 16)

#Three search functions, every one returns for the point i its k nearest neighbors
search_naive = lambda i, k: naive_search.getKNN(i, X, Y, Z, k)
search_voxel = lambda i, k: voxel_grid.searchVoxels(i, X, Y, Z, k, H, J, n_r)
search_kd = lambda i, k: tree.query(i, k)

if use_octree:
    search_octree = lambda i, k: otree.query(i, k)

if use_rtree:
    search_rtree = lambda i, k: rtree.query(i, k)


#Calculation of spatial density for each method
print("Spatial density:")

if run_naive:
    t = time()
    d_aver, rho = computeDensity(X, Y, Z, search_naive)
    print("  naive search:  d_aver = %.6f   rho = %.4f   time = %.3f s" % (d_aver, rho, time() - t))

t = time()
d_aver, rho = computeDensity(X, Y, Z, search_voxel)
print("  voxel grid:    d_aver = %.6f   rho = %.4f   time = %.3f s" % (d_aver, rho, time() - t))

t = time()
d_aver, rho = computeDensity(X, Y, Z, search_kd)
print("  kd-tree:       d_aver = %.6f   rho = %.4f   time = %.3f s" % (d_aver, rho, time() - t))

if use_octree:
    t = time()
    d_aver, rho = computeDensity(X, Y, Z, search_octree)
    print("  octree:        d_aver = %.6f   rho = %.4f   time = %.3f s" % (d_aver, rho, time() - t))

if use_rtree:
    t = time()
    d_aver, rho = computeDensity(X, Y, Z, search_rtree)
    print("  R-tree:        d_aver = %.6f   rho = %.4f   time = %.3f s" % (d_aver, rho, time() - t))

#Curvature: kappa = l1 / (l1 + l2 + l3)
k = 30

print("Curvature:")

t = time()
kappa_voxel = computeCurvature(X, Y, Z, search_voxel, k)
print("voxel grid:  time = %.3f s" % (time() - t))

t = time()
kappa_kd = computeCurvature(X, Y, Z, search_kd, k)
print("kd-tree:     time = %.3f s" % (time() - t))

if use_octree:
    t = time()
    kappa_octree = computeCurvature(X, Y, Z, search_octree, k)
    print("octree:      time = %.3f s" % (time() - t))

if use_rtree:
    t = time()
    kappa_rtree = computeCurvature(X, Y, Z, search_rtree, k)
    print("R-tree:      time = %.3f s" % (time() - t))

print("maximal difference of the curvatures:", abs(kappa_voxel - kappa_kd).max())


#Draw curvature
#The upper limit of the colour scale is the 98th percentile, a few extremes would otherwise spoil the scale (AI generated solution for better visualization)
fig = figure()
ax = axes(projection = "3d")
ax.set_box_aspect((dx, dy, dz))
sc = ax.scatter(X, Y, Z, c = kappa_kd, cmap = "viridis", s = 2, vmax = percentile(kappa_kd, 98))
colorbar(sc, label = "curvature")
show()
