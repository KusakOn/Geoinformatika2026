#Method 2: voxelization (grid)

from numpy import zeros

from naive_search import getKNN


def init_spat_index(X, Y, Z):
    #Compute bounding box
    x_min = min(X)
    x_max = max(X)
    y_min = min(Y)
    y_max = max(Y)
    z_min = min(Z)
    z_max = max(Z)

    #Min_max box edges
    dx = x_max - x_min
    dy = y_max - y_min
    dz = z_max - z_min

    return x_min, y_min, z_min, dx, dy, dz


def get3DIndex(x, y, z, x_min, y_min, z_min, dx, dy, dz, n_r):
    #Rounding constant (to avoid index out of bounds)
    c = 0.9999999999999

    #Reduced coordinates
    xr = (x - x_min) / dx
    yr = (y - y_min) / dy
    zr = (z - z_min) / dz

    #Compute indices
    jx = int(xr * n_r * c)
    jy = int(yr * n_r * c)
    jz = int(zr * n_r * c)

    return jx, jy, jz


def get1DIndex(jx, jy, jz, n_r):
    #Convert 3D index to unique 1D number
    return jx + jy * n_r + jz * (n_r**2)


def get3D_1D(idx, n_r):
    #Inverse function: 1D number -> 3D index
    return idx % n_r, idx // n_r % n_r, idx // (n_r**2)


def create3DIndex(X, Y, Z, x_min, y_min, z_min, dx, dy, dz, n_r):
    #Dictionary for spatial index H (voxel -> points) and list J (point -> voxel)
    H = {}
    J = []

    for i in range(len(X)):
        #Get address of the point
        jx, jy, jz = get3DIndex(X[i], Y[i], Z[i], x_min, y_min, z_min, dx, dy, dz, n_r)

        #Get hash key
        idx = get1DIndex(jx, jy, jz, n_r)

        #Create list if not exists
        if idx not in H:
            H[idx] = []

        #Save point ID i into the voxel
        H[idx].append(i)
        J.append(idx)

    return H, J


def createSpatialIDXs(X, Y, Z, n_r):
    #Create the spatial index (H and J), the bounding box is returned as well
    x_min, y_min, z_min, dx, dy, dz = init_spat_index(X, Y, Z)
    H, J = create3DIndex(X, Y, Z, x_min, y_min, z_min, dx, dy, dz, n_r)
    return H, J, n_r, (x_min, y_min, z_min, dx, dy, dz)


def getOccupancy(H, n_r):
    #3D array: True for every voxel containing at least one point (for drawing the voxels)
    V = zeros((n_r, n_r, n_r), dtype = bool)

    for idx in H:
        jx, jy, jz = get3D_1D(idx, n_r)
        V[jx, jy, jz] = True

    return V


def getShell(jx, jy, jz, r, n_r):
    #Voxels with the distance exactly r from the voxel [jx, jy, jz] = surface of a cube around it
    shell = []

    for kx in range(jx - r, jx + r + 1):
        for ky in range(jy - r, jy + r + 1):
            for kz in range(jz - r, jz + r + 1):

                #Check bounds
                if kx < 0 or kx >= n_r or ky < 0 or ky >= n_r or kz < 0 or kz >= n_r: continue

                #Only the surface of the cube
                if max(abs(kx - jx), abs(ky - jy), abs(kz - jz)) != r: continue

                shell.append(get1DIndex(kx, ky, kz, n_r))

    return shell


def searchVoxels(i, X, Y, Z, k, H, J, n_r, extra_rings = 2):
    #k-nearest neighbours of the point i
    jx, jy, jz = get3D_1D(J[i], n_r)

    #Candidates: the points from the same voxel
    candidates = set(H[J[i]])
    r = 0
    extra = 0

    while r < n_r - 1:

        #Enough candidates (the point i itself is not counted): add only a few extra layers of voxels, because a closer point can lie behind the edge of the voxel
        if len(candidates) - 1 >= k:
            if extra == extra_rings:
                break
            extra += 1

        #Add the next layer of voxels around the voxel of the point i
        r += 1
        for idx in getShell(jx, jy, jz, r, n_r):
            if idx in H:
                candidates.update(H[idx])

    # Ordinary search, but only among the candidates
    return getKNN(i, X, Y, Z, k, candidates)
