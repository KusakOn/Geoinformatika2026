#Method 3: kd-tree

from naive_search import updateNeighbors, finishNeighbors


class KDNode:

    def __init__(self, point=None, axis=None, left=None, right=None, point_indices=None):

        self.point = point                      
        self.axis = axis                        
        self.left = left                       
        self.right = right                      
        self.point_indices = point_indices      


class KDTree:

    def __init__(self, data, leaf_size = 16):

        #data: list of the coordinates [X, Y, Z]
        self.data = data
        self.leaf_size = leaf_size             
        self.root = self._build_tree(list(range(len(data[0]))), 0)

    def _build_tree(self, idxs, depth):
        #Build the (sub)tree of the points idxs

        if len(idxs) <= self.leaf_size:
            #Few points: leaf
            return KDNode(point_indices = idxs)

        #The axis changes with the depth
        axis = depth % 3
        coords = self.data[axis]

        #Sort the points along the axis, the median is in the middle
        idxs.sort(key = coords.__getitem__)
        m = len(idxs) // 2

        #Divide the points to the left and the right part and continue recursively
        left = self._build_tree(idxs[:m], depth + 1)
        right = self._build_tree(idxs[m:], depth + 1)

        return KDNode(point = idxs[m], axis = axis, left = left, right = right)

    def query(self, i, k):
        #k nearest neighbours of the point i: list of pairs (distance, index)
        q = (self.data[0][i], self.data[1][i], self.data[2][i])
        best = []
        self._search(self.root, i, q, k, best)
        return finishNeighbors(best)

    def _search(self, node, i, q, k, best):
        #Search in the subtree of the node

        if node.point_indices is not None:
            #Leaf: test all its points
            X, Y, Z = self.data
            updateNeighbors(node.point_indices, i, q, k, best, X, Y, Z)
            return

        #Signed distance of the query point from the dividing plane
        diff = q[node.axis] - self.data[node.axis][node.point]

        #The nearer half is searched first
        if diff < 0:
            near, far = node.left, node.right
        else:
            near, far = node.right, node.left

        self._search(near, i, q, k, best)

        #The farther half only if the plane is closer than the worst neighbour
        if len(best) < k or diff * diff < best[-1][0]:
            self._search(far, i, q, k, best)
