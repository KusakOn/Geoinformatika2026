from naive_search import getKNN


class OCtree:                                                    #Class for octree. I has only root, where searching starts.

    def __init__(self, X, Y, Z):
        top_vertex = [min(X), max(Y), max(Z)]
        bottom_vertex =[max(X), min(Y), min(Z)]
        root = Octree_vertex("", top_vertex, bottom_vertex)      #First build root.

        data = [i for i in range (len(X))]                       #Every point is there.

        root.fill_vertex(data, X, Y, Z)                          #Than recursively build rest of the tree.
        self.root = root



    def find_neighbours (self, point, k, X, Y, Z):               #Finding k closest neigbours

        father = self.root

        son = (self.root).which_child(point, X,Y,Z)

        while son.data is None:                                  #Start search in root and reach leaf with point.
            father = son
            son = father.which_child(point, X, Y, Z)

        candidates = father.extract_data()                       #We will find at least "k" points, which likely would be near. 

        posibbilities = getKNN(point, X,Y,Z, k , candidates)     #Out of them only "k" can be good.

        queue = [self.root]

        while queue :                                            #Our walk throught tree.

            current = queue.pop(0)

            if current.point_octant_distance(point, X,Y,Z) < posibbilities[k-1][0] and current is not father:  #We can ignor distant octants.

                if (current.data is None):                      #If octant is close, we will later visit his children...
                    for child in current.children:
                        queue.append(child)

                else:                                           #Or look in to his data and try to improve our neighbours.
                    together = set(current.data)
                    for x in posibbilities:
                        together.add(x[1])
                    posibbilities = getKNN(point, X,Y,Z, 30, together)

        return posibbilities                                    #After evaluating of the tree, we can output solution.



class Octree_vertex:                                            #Class of one vertex in tree

    def __init__(self, label, top_vertex, bottom_vertex, points = None, children = None):

        self.children = children
        self.label = label
        self.data = points
        self.top_vertex = top_vertex          
        self.bottom_vertex = bottom_vertex


    def fill_vertex (self, data, X, Y, Z):

        if (len(data) < 31):
            self.data = data

        else:
            oc_1 = []             #List of point which will pass to each suboctant
            oc_2 = []
            oc_3 = []
            oc_4 = []
            oc_5 = []
            oc_6 = []
            oc_7 = []
            oc_8 = []

            centre_x = (self.top_vertex[0] + self.bottom_vertex[0])/2               #Coordinates of the centre of octant.
            centre_y = (self.top_vertex[1] + self.bottom_vertex[1])/2
            centre_z = (self.top_vertex[2] + self.bottom_vertex[2])/2

            for point in data:                                                      #Every point is passed dependently on his position.

                if (X[point] > centre_x):
                    if (Y[point] > centre_y ):
                        if (Z[point] > centre_z):
                            oc_7.append(point)
                        else:
                            oc_3.append(point)
                    else:
                        if Z[point] > centre_z:
                            oc_6.append(point)
                        else:
                            oc_2.append(point)
                else:
                    if Y[point] > centre_y:

                        if Z[point] > centre_z:
                            oc_8.append(point)
                        else:
                            oc_4.append(point)
                    else:
                        if Z[point] > centre_z:
                            oc_5.append(point)
                        else:
                            oc_1.append(point)


            min_x = self.top_vertex[0]                  #Some preprocesing for easier notation.
            min_y = self.bottom_vertex[1]
            min_z = self.bottom_vertex[2]

            max_x = self.bottom_vertex[0]
            max_y = self.top_vertex[1]
            max_z = self.top_vertex[2]

            first = Octree_vertex( self.label +"1", top_vertex=[min_x, centre_y,centre_z] , bottom_vertex=[centre_x, min_y,min_z]  )   #Contruct each of 8 octant independently.
            second = Octree_vertex( self.label +"2", top_vertex= [centre_x, centre_y, centre_z], bottom_vertex= self.bottom_vertex )
            third = Octree_vertex( self.label +"3", top_vertex= [centre_x, max_y, centre_z], bottom_vertex=[max_x, centre_y, min_z] )
            fourth = Octree_vertex( self.label +"4",top_vertex=[min_x, max_y ,centre_z] , bottom_vertex=[centre_x, centre_y, min_z])
            fifth = Octree_vertex( self.label +"5", top_vertex=[min_x, centre_y, max_z], bottom_vertex=[centre_x, min_y, centre_z])
            sixth = Octree_vertex( self.label +"6", top_vertex=[centre_x, centre_y, max_z], bottom_vertex=[max_x, min_y, centre_z])
            seventh = Octree_vertex( self.label +"7", top_vertex=[centre_x, max_y, max_z], bottom_vertex=[max_x, centre_y, centre_z])
            eighth = Octree_vertex( self.label +"8", top_vertex=self.top_vertex, bottom_vertex=[centre_x, centre_y, centre_z] )


            first.fill_vertex(oc_1 ,X, Y, Z)                                                 #Aply same procedure for every child recursively.
            second.fill_vertex(oc_2 ,X, Y, Z)
            third.fill_vertex(oc_3 ,X, Y, Z)
            fourth.fill_vertex(oc_4 ,X, Y, Z)
            fifth.fill_vertex(oc_5 ,X, Y, Z)
            sixth.fill_vertex(oc_6 ,X, Y, Z)
            seventh.fill_vertex(oc_7 ,X, Y, Z)
            eighth.fill_vertex(oc_8 ,X, Y, Z)

            self.children = [first, second, third, fourth, fifth, sixth, seventh, eighth]   #We have sucefully built children of vertex.

    
    def which_child (self, point, X,Y,Z):                                #Function will output, in which child of vertex is given point.
                                                                         #It works as "fill_vertex"
            centre_x = (self.top_vertex[0] + self.bottom_vertex[0])/2
            centre_y = (self.top_vertex[1] + self.bottom_vertex[1])/2
            centre_z = (self.top_vertex[2] + self.bottom_vertex[2])/2
               
            if (X[point] > centre_x):
                if (Y[point] > centre_y ):
                    if (Z[point] > centre_z):
                        return self.children[6]
                    else:
                        return self.children[2]
                else:
                    if Z[point] > centre_z:
                        return self.children[5] 
                    else:
                        return self.children[1]

            else:
                if Y[point] > centre_y:

                    if Z[point] > centre_z:
                        return self.children[7]   
                    else:
                        return self.children[3]
                else:
                    if Z[point] > centre_z:
                        return self.children [4] 
                    else:
                        return self.children[0]
    


    def extract_data (self):                                #It will return set of points in given octant.

        if self.data is not None:                           #They can be as atribut precalculed.
            return set(self.data) 

        else:
            posibbilities = set()

            for x in self.children:                         #Otherwise we need to visit all of the child and find out their points.
                posibbilities = posibbilities.union(x.extract_data())

            return posibbilities

        
    def point_octant_distance (self, point, X, Y, Z):                   #It will return the smallest distance between point and octant.
                                                                        #Work coordinate by coordinate.
        if  self.top_vertex[0]<= X[point] <= self.bottom_vertex[0]:     #If points fit, distance is zero.
            x_d = 0
        else:                                                           #Otherwise it is distance to one of the edges.
            x_d = min(abs(X[point] - self.top_vertex[0]), abs(X[point] - self.bottom_vertex[0]) ) ** 2


        if  self.bottom_vertex[1] <= Y[point] <=  self.top_vertex[1]:
            y_d = 0
        else:
            y_d = min(abs(Y[point] - self.top_vertex[1]), abs(Y[point] - self.bottom_vertex[1]) ) ** 2


        if  self.bottom_vertex[2] <= Z[point] <=  self.top_vertex[2]:
            z_d = 0
        else:
            z_d = min(abs(Z[point] - self.top_vertex[2]), abs(Z[point] - self.bottom_vertex[2]) ) ** 2

        return (x_d + y_d + z_d) ** (1/2)                                 #Use Pythagorean theorem.


