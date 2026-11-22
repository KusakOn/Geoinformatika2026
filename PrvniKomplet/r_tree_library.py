from turtle import distance
from rtree import index
from r_tree import distance_between_points


#Some basic definition: https://rtree.readthedocs.io/en/latest/tutorial.html   last example.


class R_tree_library:                           #Fake class only to preserve style of program.

    def __init__ (self, X,Y,Z):                
        p = index.Property()
        p.dimension = 3
        tree = index.Index(properties = p)      #Initiation of the tree.

        for point in range(len(X)):             #Point by point appending.
            tree.insert(point , (X[point], Y[point], Z[point], X[point], Y[point], Z[point]))

        self.tree = tree                        #Remember result

    def find_neighbours (self, point, k, X,Y,Z):         #Return k nearest neighbours.
        data = list((self.tree).nearest((X[point], Y[point], Z[point], X[point], Y[point], Z[point]), k+1))     #This is library function

        better_form = []                                       #We prefer to have tuples of the form (distance:point)
        for x in data:
            if x != point:                                    #Point itself is there.
                distance = distance_between_points(x,point,X,Y,Z)   
                better_form.append((distance,x))              #For other points just compute distance and save it.
        
        return better_form
