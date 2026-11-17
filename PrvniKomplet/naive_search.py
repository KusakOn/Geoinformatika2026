#Method 1: naive search, every point is compared with every other point

from bisect import insort


def insertNeighbor(best, d2, idx, k):
    #Keep the k nearest points found so far

    if len(best) < k:
        #Too few neighbours so far
        insort(best, (d2, idx))

    elif d2 < best[-1][0]:
        #Better than the worst neighbour: insert it and drop the farthest one
        insort(best, (d2, idx))
        best.pop()


def updateNeighbors(candidates, i, q, k, best, X, Y, Z):
    #Test all the candidate points and update the list of the k nearest neighbours of the point i
    #q = (x, y, z) are the coordinates of the point i
    for j in candidates:
        if j != i:
            #Squared distance
            dx, dy, dz = q[0] - X[j], q[1] - Y[j], q[2] - Z[j]
            d2 = dx*dx + dy*dy + dz*dz

            #Fast test before the insertion
            if len(best) < k or d2 < best[-1][0]:
                insertNeighbor(best, d2, j, k)


def finishNeighbors(best):
    #Output format: list of pairs (distance, index of the point), the nearest first
    return [(d2**0.5, idx) for d2, idx in best]


def getKNN(i, X, Y, Z, k, candidates = None):
    #k nearest neighbours of the point i, searched among the candidates
    #candidates = None means all the points (naive search)
    if candidates is None:
        candidates = range(len(X))

    best = []
    updateNeighbors(candidates, i, (X[i], Y[i], Z[i]), k, best, X, Y, Z)

    return finishNeighbors(best)


def boxDistance(q, box):
    #Squared distance of the point q = (x, y, z) from the box (x_min, y_min, z_min, x_max, y_max, z_max)
    dx = max(box[0] - q[0], 0, q[0] - box[3])
    dy = max(box[1] - q[1], 0, q[1] - box[4])
    dz = max(box[2] - q[2], 0, q[2] - box[5])
    return dx*dx + dy*dy + dz*dz


def searchBoxTree(node, i, q, k, best, X, Y, Z):
    #Search in a tree of boxes: the node has a box, a list of children (inner node) or a list of points (leaf)

    if node.point_indices is not None:
        #Leaf: test all its points
        updateNeighbors(node.point_indices, i, q, k, best, X, Y, Z)
        return

    #Distances of the query point from the boxes of the children, the nearest box first
    children = []
    for child in node.children:
        children.append((boxDistance(q, child.box), child))
    children.sort(key = lambda c: c[0])

    for d2, child in children:
        #The box is farther than the worst neighbour, so are all the following boxes
        if len(best) == k and d2 >= best[-1][0]:
            break

        searchBoxTree(child, i, q, k, best, X, Y, Z)
