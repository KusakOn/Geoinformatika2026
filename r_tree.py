
from naive_search import getKNN

def distance_between_points (first, second, X, Y, Z):        #Euclidean distance between 2 points by Pythagorean theorem
    first_coordinate = (X[first] - X[second])**2
    druha_coordinate = (Y[first] - Y[second])**2
    third_coordinate = (Z[first] - Z[second])**2
    return (first_coordinate + druha_coordinate + third_coordinate) ** (1/2)


class R_tree:                                                 #R tree class. It has only root.

    def __init__ (self, X,Y,Z):                              #Construction: From top to down

        self.root = R_node([X[0], Y[0], Z[0]],0,0,0,[0])     #Start with root and first point

        for point in range (1, len(X)):                      #One by one add every point
            (self.root).extra_point(point, X,Y,Z)


    def find_neighbours (self, point, k, X,Y,Z):             #Finds k closes neigbours using existing R tree

        father = self.root
        son = father.which_child(point, X,Y,Z)

        while son.children is not None:                      #Find the closes box which is not leaf. There will be enought candidates.
            father = son
            son = father.which_child(point, X,Y,Z)

        candidate = father.data

        possibilities = getKNN(point, X,Y,Z, k, candidate)     #Out of them only k best will be used.

        queue = [self.root]                                   #queue ob boxes, where we need to search

        while queue:      
            current = queue.pop()                             #Pick first

            if current.point_to_octant(point, X,Y,Z) < possibilities[k-1][0]:     #If it is too far, we are done here

                if (current.children is not None):                                #Otherwise we will inspect his children, if he had some...
                    for child in current.children:
                        queue.append(child)

                else:                                                             #Else we will look to his points and update neigbourhood
                    together = set(current.data)
                    for x in possibilities:
                        together.add(x[1])
                    possibilities = getKNN(point, X,Y,Z, k, together)


        return possibilities

class R_node:                 #One box in R tree.

    def __init__ (self, bottom, lenght, width, height, data, children = None):

        self.bottom = bottom                    #Point (list of 3 int) with minimal coordinates in data
        self.lenght = lenght                    #Size in x
        self.width = width                      #Size in y
        self.height = height                    #Size in z
        
        self.data = data                        #Points in box
        self.children = children                #List of Subboxes


    def point_in_node (self, point,X,Y,Z):            #Is point inside of box?
        
        first_ok = self.bottom[0] <= X[point] and X[point] <= self.bottom[0] + self.lenght   #Checking coordinates one by one
        second_ok = self.bottom[1] <= Y[point] and Y[point] <= self.bottom[1] + self.width
        third_ok = self.bottom[2] <= Z[point] and Z[point] <= self.bottom[2] + self.height

        return first_ok and second_ok and third_ok               #All 3 must fit.



    def volume (self):                                       #Compute volume of box by multiplying sizes.
        return self.lenght * self.width * self.height


    def insert_point(self, point, X, Y, Z):                  #Insert new point to data and recalculate characteristics

        if X[point] < self.bottom[0]:                        #If point is not in box, we need to find new bottom and take bigger lenght
            self.lenght += self.bottom[0] - X[point]
            self.bottom[0] = X[point]
        elif self.bottom[0] + self.lenght < X[point]:
            self.lenght = X[point] - self.bottom[0]

        if Y[point] < self.bottom[1]:                        #Same for y-coordinate
            self.width += self.bottom[1] - Y[point]
            self.bottom[1] = Y[point]
        elif self.bottom[1] + self.width < Y[point]:
            self.width = Y[point] - self.bottom[1]

        if Z[point] < self.bottom[2]:                        #Same for z-coordinate 
            self.height += self.bottom[2] - Z[point]
            self.bottom[2] = Z[point]
        elif self.bottom[2] + self.height < Z[point]:
            self.height = Z[point] - self.bottom[2]

        (self.data).append(point)


    def split_tree (self, X,Y,Z):                                #Split box. It use litle of heuristics

        x,y = self.the_most_distant_pair(X,Y,Z)                  #Find the most distance pair

        first = R_node([X[x], Y[x], Z[x]] ,0 ,0, 0, [x])         #They must be in different boxes
        second = R_node([X[y], Y[y], Z[y]] ,0 ,0, 0, [y])
        
        for point in self.data:                                  #Other point are added in manner not to increse volume of existing boxes (or as little as possible)
            if point != x and point != y:
                if first.volume_after_adding(point, X,Y,Z) < second.volume_after_adding(point, X,Y,Z):
                    first.insert_point(point, X,Y,Z)
                else:
                    second.insert_point(point, X, Y, Z)

        self.children = [first, second]



    def the_most_distant_pair(self,X,Y,Z):                         #Find two points with the biggest distance in box
        
        maximum = 0
        first = None
        second = None

        for x in self.data:                                        #Just trivial algorithm. It is likely for them to be on boundary, but it is not sufficient
            for y in self.data:

                if distance_between_points(x,y, X,Y,Z) > maximum:
                    maximum = distance_between_points(x,y, X,Y,Z)
                    first = x
                    second = y

        return first, second

    def volume_after_adding(self, point, X, Y, Z):                 #How much will volume insrece after adding new point?

        lenght_r = self.lenght
        height_r = self.height
        width_r = self.width

        if X[point] < self.bottom[0]:
            lenght_r += self.bottom[0] - X[point]                  #Look, if some size is changed, same as "insert_point"
        elif self.bottom[0] + lenght_r < X[point]:
            lenght_r = X[point] - self.bottom[0]

        if Y[point] < self.bottom[1]:

            width_r += self.bottom[1] - Y[point]
        elif self.bottom[1] + width_r < Y[point]:
            width_r = Y[point] - self.bottom[1]

        if Z[point] < self.bottom[2]:
            height_r += self.bottom[2] - Z[point]
        elif self.bottom[2] + self.height < Z[point]:
            height_r = Z[point] - self.bottom[2]

        return lenght_r * height_r * width_r - self.volume()      #Compute volume with new sizes, but extract old volume.



    def extra_point(self, point, X,Y,Z):                                #Add new point to node
        self.insert_point(point, X,Y,Z)

        if self.children is not None:                                   # If node has children, pass it. But try not to increse size.
            if (self.children[0]).volume_after_adding(point, X,Y,Z) < (self.children[1]).volume_after_adding(point, X,Y,Z):
                self.children[0].extra_point(point, X,Y,Z)
            else:
                self.children[1].extra_point(point, X,Y,Z)


        else:
            if (len(self.data) > 30):                                   #Even if it does not, but size of data is to big, split it in 2.
                self.split_tree(X,Y,Z)


    def point_to_octant (self, point, X,Y,Z):                 #The smallest distance between point and box

        #Count the smallest diference in all coordinates
        if X[point] > self.bottom[0] and X[point] < self.bottom[0] + self.lenght:     
            x_d = 0                                                                         #It is 0 if it would fit inside the box
        else:
            x_d = (min(abs(X[point] - self.bottom[0]) , abs(X[point] - self.bottom[0] - self.lenght) )) ** 2   #Otherwise it is the smallest distance to boundary.
             
        if Y[point] > self.bottom[1] and Y[point] < self.bottom[1] + self.width:
            y_d = 0
        else:
            y_d = (min(abs(Y[point] - self.bottom[1]) , abs(Y[point] - self.bottom[1] - self.width) )) ** 2

        if Z[point] > self.bottom[2] and Z[point] < self.bottom[2] + self.height:
            z_d = 0
        else:
            z_d = (min(abs(Z[point] - self.bottom[2]) , abs(Z[point] - self.bottom[2] - self.height) )) ** 2

        return (x_d + z_d + y_d) ** (1/2)        #Eucledean distance


    def which_child(self, point, X,Y,Z):                  #Which child containt point?

        if (self.children[0]).point_in_node(point, X,Y,Z):      #Is it first one? Otherwise it is second.
            return self.children[0]
        else:
            return self.children[1]


