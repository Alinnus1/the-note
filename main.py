import sys
import os
import copy
import stopit
import time
from math import sqrt

class Vertex:
    def __init__(self,info,position,parent,output="",cost=0,h=0):
        self.info = info # name of the kid
        self.position = position # position in the config
        self.parent = parent # probabil aici vom da si simbolul pentru afisare but idk ytet
        self.output = output
        self.g = cost
        self.h = h
        self.f = self.g + self.h

    def getPath(self):
        l = [self.info] # tine minte ca ai modificat aici
        vertex = self
        while vertex.parent is not None:
            l.insert(0,vertex.parent.info)
            vertex = vertex.parent
        return l 

    def printPath(self, showCost = False, showLength = False):
        l = self.getPath()
        print(l)
        for vertex in l:
            print(str(vertex))
        if showCost:
            print("Cost: ", self.g)
        if showCost:
            print("Lenght: ", len(l))
        return len(l)

    def isInPath(self, infoNewVertex):
        vertexPath = self
        while vertexPath is not None:
            if infoNewVertex == vertexPath.info:
                return True
            vertexPath = vertexPath.parent
        
        return False
    
    def __repr__(self):
        string =""
        string += self.info + "("
        string += "pos" + str(self.position) + " "
        string += "path= " 
        path = self.getPath()
        string += str(path)
        string += "g:{}".format(self.g)
        string += " h:{}".format(self.h)
        string += " f: {}".format(self.f) 
        return string

        
class Graph: # the graph of the problem

    maxVerticesGen = 0

    def __init__(self,file):
        f = open (file,"r")
        file_content = f.read()

        info = file_content.split("suparati")

        self.config = self.getColumns(info[0])

        self.height = len(self.config[1])
        info1 = info[1].strip().split("mesaj:")

        self.conditions = self.getConditions(info1[0])

        self.start,self.final = info1[1].strip().split("->")
        self.start = self.start.strip()
        self.final = self.final.strip()

        print("Initial config: ", self.config)
        print("Conditions: ", self.conditions)
        
        print("Start point:" , self.start)
        print("End point:" , self.final)
        # input();
    
    def getColumns(self,info):

        """A function that transforms the input information into valuable data.

        This functions makes a list of lists of lists corresponding to the 3 columns of desk benches given in the .in file.

        :param Graph self: The graph we are working with.
        :param str info: The innformation from the .in file.
        :return: A list of lists of lists corresponding to the information given.

        """

        config = [[],[],[]]
        try:
            rows = info.strip().split("\n")
            for x in rows:
                y = x.split()
                config[0].extend([[y[0],y[1]]])
                config[1].extend([[y[2],y[3]]])
                config[2].extend([[y[4],y[5]]])
        except IndexError:
            print("The information given does not respect the standard.")
            sys.exit()
        return config

    def getConditions(self,info):
        
        """A function that transforms the input information into valuable data.

        This functions makes a list of lists corresponding to the restrictions given in the .in file.

        :param Graph self: The graph we are working with.
        :param str info: The innformation from the .in file.
        :return: A list of lists corresponding to the given restrictions of the vertices.

        """

        config = []
        rows = info.strip().split("\n")

        for x in rows:
            y = x.split()
            config.extend([y])
        
        return config
            
    def test_final(self,currentVertex):
        return currentVertex.info in self.final

    def getPosition(self,currentInfoVertex):
        """A simple function that return the position of a given element in the graph.

        This function takes the configuration and searches through all of its elements to check if the given element (currentVertex) is in the config.

        :param Graph self: The graph we are working with.
        :param str currentInfoVertex: The value that resides in a vertex,
        :return: A list of 3 coordinates each coresponding to a list from self.config which represents a list of lists of lists

        """

        for i,columns in enumerate(self.config):
            for j, rows in enumerate(columns):
                for k, value in enumerate(rows):
                    if (value == currentInfoVertex):
                        return [i,j,k] 

    def verifyESolution(self,currentVertex):
        
        canWe = False

        directions = [[-1,0],[1,0],[0,-1],[0,1]]
        column, row, column_row = self.getPosition(currentVertex.info)

        for dl,dc in directions:
            rowNeighbor = row + dl
            column_rowNeighbor = column_row + dc

            try:
                if (rowNeighbor < 0) or (rowNeighbor > (self.height -1)) :
                    continue
                infoNewVertex = self.config[column][rowNeighbor][column_rowNeighbor]
                #if the latter can be passed to a person and the option was not tried yet
                if (infoNewVertex != "liber" and column_rowNeighbor>=0):
                    #if the "tuple" of the current vertex and the possible new vertex is acceptable
                    if ([infoNewVertex,currentVertex.info] not in self.conditions and [currentVertex.info,infoNewVertex] not in self.conditions): #if the new possible info is not already been in the path
                        if not currentVertex.isInPath(infoNewVertex) :
                            canWe = True
                            break
            except IndexError:
                pass

        #if the letter can be passed from the first column to the second column
        if ((column == 0 and row == (self.height-2) and column_row == 1) or (column == 0 and row == (self.height-1) and column_row == 1) ):
            infoNewVertex = self.config[1][row][0]
            if (infoNewVertex != "liber"):
                if ([infoNewVertex,currentVertex.info] not in self.conditions and [currentVertex.info,infoNewVertex] not in self.conditions):
                    if not currentVertex.isInPath(infoNewVertex):
                        canWe = True
                        
        #if the letter can be passed from the third column to the second column
        elif ((column == 2 and row == (self.height-2) and column_row == 0) or (column == 2 and row == (self.height-1)and column_row == 0) ):
            infoNewVertex = self.config[1][row][1]
            if (infoNewVertex != "liber"):
                if ([infoNewVertex,currentVertex.info] not in self.conditions and [currentVertex.info,infoNewVertex] not in self.conditions):
                    if not currentVertex.isInPath(infoNewVertex):
                            canWe = True
                            
        #if the letter can be passed from the second column to the first column
        elif ((column ==1 and row ==( self.height-2) and column_row == 0) or(column ==1 and row ==( self.height-1) and column_row == 0)):
            infoNewVertex = self.config[0][row][1]
            if (infoNewVertex != "liber"):
                if ([infoNewVertex,currentVertex.info] not in self.conditions and [currentVertex.info,infoNewVertex] not in self.conditions):
                    if not currentVertex.isInPath(infoNewVertex):
                        canWe = True
                        
        #if the letter can be passed from the second column to the third column 
        elif ((column ==1 and row ==( self.height-2) and column_row == 1) or(column ==1 and row ==( self.height-1) and column_row == 1)):
            infoNewVertex = self.config[2][row][0]
            if (infoNewVertex != "liber"):
                if ([infoNewVertex,currentVertex.info] not in self.conditions and [currentVertex.info,infoNewVertex] not in self.conditions):
                    if not currentVertex.isInPath(infoNewVertex):
                        canWe = True

        #if the letter can be passed from the starting point 
        if (canWe):
            return canWe
        else:
            return canWe

    def generateSuccesors(self,currentVertex, heuristic_type):

        """A function responsible for the generation of vertices and for the creation of the desired output.

        Our task is to find where we can pass the latter in order to reach the desired person. The latter can be passed in any direction except for diagonal so for that we we'll build a *directions* list of lists that indicate possible directions. According to the direction chosed we make sure that we have the right symbol for the output and that it satisfy all the conditions.

        :param Graph self: The graph we are working with which provides all the the possibilities (correct or not).
        :param str currentVertex: The vertex that we are trying to *expand*. We try to search to which vertex the currentVertex can pass the latter.
        :param str heuristic_type: A string that gives the heuristic we use.
        :return: A list of all the vertices that can be used to transport the latter.

        """

        listSuccesors = []
        directions = [[-1,0],[1,0],[0,-1],[0,1]]
        column, row, column_row = self.getPosition(currentVertex.info)

        for dl,dc in directions:
            rowNeighbor = row + dl
            column_rowNeighbor = column_row + dc
            if (dl == -1):
                simbol = " ^ "
            elif(dl == 1):
                simbol = " v "
            elif(dc == 1):
                simbol = " > "
            elif (dc == -1):
                simbol = " < "

            try :
                #if it's tried to pass the latter outside configuration
                if (rowNeighbor < 0) or (rowNeighbor > (self.height -1)) :
                    continue
                #if (row != (self.height-2) and row !=(self.height-1)): de optimizare era asta
                infoNewVertex = self.config[column][rowNeighbor][column_rowNeighbor]
                #if the latter can be passed to a person and the option was not tried yet
                if (infoNewVertex != "liber" and column_rowNeighbor>=0):
                    #if the "tuple" of the current vertex and the possible new vertex is acceptable
                    if ([infoNewVertex,currentVertex.info] not in self.conditions and [currentVertex.info,infoNewVertex] not in self.conditions): #if the new possible info is not already been in the path
                        if not currentVertex.isInPath(infoNewVertex) :
                            listSuccesors.append(Vertex(infoNewVertex,[column,rowNeighbor,column_rowNeighbor],currentVertex,(currentVertex.output + simbol + infoNewVertex),(currentVertex.g + 1),self.calculate_h(infoNewVertex,heuristic_type)))
                            #number of vertices generated increments
                            self.maxVerticesGen += 1

            except IndexError:
                pass
        
        #if the letter can be passed from the first column to the second column
        if ((column == 0 and row == (self.height-2) and column_row == 1) or (column == 0 and row == (self.height-1) and column_row == 1) ):
            infoNewVertex = self.config[1][row][0]
            if (infoNewVertex != "liber"):
                if ([infoNewVertex,currentVertex.info] not in self.conditions and [currentVertex.info,infoNewVertex] not in self.conditions):
                    if not currentVertex.isInPath(infoNewVertex):
                        listSuccesors.append(Vertex(infoNewVertex,[1,row,0],currentVertex, currentVertex.output + " >> " +infoNewVertex,currentVertex.g+1,self.calculate_h(infoNewVertex,heuristic_type)))
                        self.maxVerticesGen += 1
        #if the letter can be passed from the third column to the second column
        elif ((column == 2 and row == (self.height-2) and column_row == 0) or (column == 2 and row == (self.height-1)and column_row == 0) ):
            infoNewVertex = self.config[1][row][1]
            if (infoNewVertex != "liber"):
                if ([infoNewVertex,currentVertex.info] not in self.conditions and [currentVertex.info,infoNewVertex] not in self.conditions):
                    if not currentVertex.isInPath(infoNewVertex):
                        listSuccesors.append(Vertex(infoNewVertex,[1,row,1],currentVertex,currentVertex.output +" << "+infoNewVertex,currentVertex.g+1,self.calculate_h(infoNewVertex,heuristic_type)))
                        self.maxVerticesGen += 1
        #if the letter can be passed from the second column to the first column
        elif ((column ==1 and row ==( self.height-2) and column_row == 0) or(column ==1 and row ==( self.height-1) and column_row == 0)):
            infoNewVertex = self.config[0][row][1]
            if (infoNewVertex != "liber"):
                if ([infoNewVertex,currentVertex.info] not in self.conditions and [currentVertex.info,infoNewVertex] not in self.conditions):
                    if not currentVertex.isInPath(infoNewVertex):
                        listSuccesors.append(Vertex(infoNewVertex,[0,row,1],currentVertex,currentVertex.output + " << "+infoNewVertex,currentVertex.g+1,self.calculate_h(infoNewVertex,heuristic_type)))
                        self.maxVerticesGen += 1
        #if the letter can be passed from the second column to the third column 
        elif ((column ==1 and row ==( self.height-2) and column_row == 1) or(column ==1 and row ==( self.height-1) and column_row == 1)):
            infoNewVertex = self.config[2][row][0]
            if (infoNewVertex != "liber"):
                if ([infoNewVertex,currentVertex.info] not in self.conditions and [currentVertex.info,infoNewVertex] not in self.conditions):
                    if not currentVertex.isInPath(infoNewVertex):
                        listSuccesors.append(Vertex(infoNewVertex,[2,row,0],currentVertex,currentVertex.output + " >> "+infoNewVertex,currentVertex.g+1,self.calculate_h(infoNewVertex,heuristic_type)))
                        self.maxVerticesGen += 1

        return listSuccesors

    def calculate_h(self, infoVertex,heuristic_type = "heuristic_1"):
        if heuristic_type == "heuristic_1":
            return self.heuristic_1(infoVertex,heuristic_type)
        elif heuristic_type == "heuristic_2":
            return self.heuristic_2(infoVertex,heuristic_type)
        elif heuristic_type == "heuristic_3":
            return self.heuristic_3(infoVertex,heuristic_type)
        elif heuristic_type == "heuristic_4":
            return self.heuristic_4(infoVertex,heuristic_type)

    def heuristic_1(self,infoVertex,heuristic_type):
        return 0 if infoVertex in self.final else 1

    def heuristic_2(self,infoVertex,heuristic_type):

        """A simple function that returns the manhattan distance from a given element to the destination.

        This function takes the configuration and transforms it into a 2-dimensional matrix.

        :param Graph self: The graph we are working with.
        :param str infoVertex: The value that resides in the vertex from whom we want the distance to the destination.
        :return: The desired destiantion.

        """
        b,r,c = self.getPosition(gr.final)
        b1,r1,c1 = self.getPosition(infoVertex)
       
        cord1,cord11 = r,r1
        if (b == 0):
            cord2= c
        elif ( b== 1):
            cord2= c+2
        elif ( b==2):
            cord2 = c+4

        if (b1 == 0):
            cord22= c
        elif ( b1== 1):
            cord22= c+2
        elif ( b1==2):
            cord22 = c+4

        val = abs(cord1 - cord11) + abs(cord2 - cord22)
        return val

    def heuristic_3(self,infoVertex,heuristic_type):
        """A simple function that returns the euler distance from a given element to the destination.

        This function takes the configuration and transforms it into a 2-dimensional matrix.

        :param Graph self: The graph we are working with.
        :param str infoVertex: The value that resides in the vertex from whom we want the distance to the destination.
        :return: The desired destiantion.

        """
        b,r,c = self.getPosition(gr.final)
        b1,r1,c1 = self.getPosition(infoVertex)
       
        cord1,cord11 = r,r1
        if (b == 0):
            cord2= c
        elif (b == 1):
            cord2= c+2
        elif (b == 2):
            cord2 = c+4

        if (b1 == 0):
            cord22= c
        elif (b1 == 1):
            cord22= c+2
        elif (b1 == 2):
            cord22 = c+4

        val = sqrt((cord1-cord11)*2 - (cord2-cord22)*2)
        return val
    
    def heuristic_4(self,infoVertex,heuristic_type):
        return self.maxVerticesGen

    def __repr__(self):
        string = " "
        for (k,v) in self.__dict__.items():
            string+= "{} = {} \n".format(k,v)
        return string

    def __str__(self):
        string = "########\n"
        c1,c2,c3 = self.config
        for rows in range(len(c1)):
            string +="# "+c1[rows][0] + " " +c1[rows][1] + "\t " +c2[rows][0] +" " + c2[rows][1] + " \t" + c3[rows][0] + " " +c3[rows][1] +"\t# \n"
        string+= "########"
        return string

@stopit.threading_timeoutable(default="Timp Scurs")
def a_star(gr, nr_sol_searched, heuristic_type):
    
    
    start = time.time()
    maxVertices = 0

    c = [Vertex(gr.start,gr.getPosition(gr.start),None,gr.start,0,gr.calculate_h(gr.start,heuristic_type))]

    if not gr.verifyESolution(c[0]):
        print ("No solutions can be achieved")
        g.write("No solutions can be achieved")
        return

    while len(c) > 0:
        # print("Coada actuala: " + str(c))
        # input()
        currentVertex = c.pop(0)
        
        if gr.test_final(currentVertex):
            end = time.time()
            print("Solution: ")
            currentVertex.printPath(showCost=True,showLength=True)
            print("\n~~~~~~~~~~~~~~~~~~~\n")
            print(currentVertex.output)
            g.write(currentVertex.output + "\n")
            print(f"The solution was found in {end - start}")
            print("\n-------------------\n")
            nr_sol_searched -= 1
            if nr_sol_searched == 0:
                print(f"The maximum number of vertices saved at a time was {str(maxVertices)} and the total number of vertices generated is {str(gr.maxVerticesGen)}")
                return


        listSuccesors = gr.generateSuccesors(currentVertex,heuristic_type=heuristic_type)
        maxVertices = max(maxVertices,(len(listSuccesors)+len(c)))
        # print("succesori actuali: ")
        # print(listSuccesors)
        # input()
        for s in listSuccesors:
            i = 0
            while i< len(c):
                if c[i].f >= s.f:
                    break
                i += 1
            c.insert(i,s)

@stopit.threading_timeoutable(default="Timp Scurs")
def a_star_optim(gr,heuristic_type):

    start = time.time()    
    maxVertices = 0

    c = [Vertex(gr.start,gr.getPosition(gr.start),None,gr.start,0,gr.calculate_h(gr.start,heuristic_type))]
    closed = []

    if not gr.verifyESolution(c[0]):
        print ("No solutions can be achieved")
        g.write("No solutions can be achieved")
        return

    while len(c) >0 :
        # print("Coada actuala: " + str(c))
        # input()
        currentVertex = c.pop(0)
        closed.append(currentVertex)

        if gr.test_final(currentVertex):
            end = time.time()
            print("Solution: ")
            currentVertex.printPath(showCost=True,showLength=True)
            print("\n~~~~~~~~~~~~~~~~~~~\n")
            print(currentVertex.output)
            g.write(currentVertex.output + "\n")
            print(f"The solution was found in {end - start}")
            print(f"The maximum number of vertices saved at a time was {str(maxVertices)} and the total number of vertices generated is {str(gr.maxVerticesGen)}")
            print("\n-------------------\n")
            return
        listSuccesors = gr.generateSuccesors(currentVertex,heuristic_type=heuristic_type)
        listSuccesorsCopy = listSuccesors.copy()

        maxVertices = max(maxVertices,(len(listSuccesors)+len(c)+len(closed)))

        for s in listSuccesorsCopy:
            foundOpen = False
            for elem in c:
                if s.info == elem.info:
                    foundOpen = True
                    if s.f < elem.f:
                        c.remove(elem)
                    else:
                        listSuccesors.remove(s)
                    break
            if not foundOpen:
                for elem in closed:
                    if s.info == elem.info:
                        if s.f < elem.f:
                            closed.remove(elem)
                        else:
                            listSuccesors.remove(s)
                        break
        
        for s in listSuccesors:
            i = 0
            while i< len(c):
                if c[i].f >= s.f:
                    break
                i += 1
            c.insert(i,s)

@stopit.threading_timeoutable(default="Timp Scurs")
def uniform_cost(gr, nr_sol_searched,heuristic_type):
    
    start=  time.time()

    c = [Vertex(gr.start,gr.getPosition(gr.start),None,gr.start,0,gr.calculate_h(gr.start,heuristic_type))]
    maxVertices = 0

    if not gr.verifyESolution(c[0]):
        print ("No solutions can be achieved")
        g.write("No solutions can be achieved")
        return

    while len(c) > 0:
        currentVertex = c.pop(0)
        # print("Coada dupa pop:")
        # print(c)
        if gr.test_final(currentVertex):
            end = time.time()
            print("Solution: ")
            currentVertex.printPath(showCost=True,showLength=True)
            print("\n~~~~~~~~~~~~~~~~~~~\n")
            print(currentVertex.output)
            g.write(currentVertex.output + "\n")
            print(f"The solution was found in {end - start}")
            print("\n-------------------\n")
            # input()
            nr_sol_searched -= 1
            if nr_sol_searched == 0:
                print(f"The maximum number of vertices saved at a time was {str(maxVertices)} and the total number of vertices generated is {str(gr.maxVerticesGen)}")
                return
        
        listSuccesors = gr.generateSuccesors(currentVertex,heuristic_type=heuristic_type)
        maxVertices = max(maxVertices,(len(listSuccesors)+len(c)))
        # print("succesori actuali: ")
        # print(listSuccesors)
        # input()
        for s in listSuccesors:
            i = 0
            while i< len(c):
                if c[i].g > s.g:
                    break
                i += 1
            c.insert(i,s)

maxVertices = 0
@stopit.threading_timeoutable(default="Timp Scurs")
def ida_star(gr,nr_sol_searched,heuristic_type):

    start = time.time()
    
    
    limit = gr.calculate_h(gr.start)
    vertexStart = Vertex(gr.start,gr.getPosition(gr.start),None,gr.start,0,gr.calculate_h(gr.start,heuristic_type))

    if not gr.verifyESolution(vertexStart):
        print ("No solutions can be achieved")
        g.write("No solutions can be achieved")
        return

    while True:
        # print ("Starting limit: ", limit)
        nr_sol_searched, rez = build_path(gr,vertexStart,limit,nr_sol_searched,start,heuristic_type)

        if rez == "done":
            print(f"The maximum number of vertices saved at a time was {str(maxVertices)} and the total number of vertices generated is {str(gr.maxVerticesGen)}")
            break
        if rez == float("inf"):
            print(f"The maximum number of vertices saved at a time was {str(maxVertices)} and the total number of vertices generated is {str(gr.maxVerticesGen)}")
            print ("There are no solutions")
            break
        limit = rez
        # print(">>> New limit:" , limit)
        # input()


def build_path(gr, currentVertex, limit,nr_sol_searched,start,heuristic_type):
    # print("We've reached :", currentVertex)
    if currentVertex.f > limit :
        return nr_sol_searched, currentVertex.f
    if gr.test_final(currentVertex) and currentVertex.f == limit :
        end = time.time()
        print("Solution: ")
        currentVertex.printPath(showCost=True,showLength=True)
        print(limit)
        print("\n~~~~~~~~~~~~~~~~~~~\n")
        print(currentVertex.output)
        g.write(currentVertex.output + "\n")
        print(f"The solution was found in {end - start}")
        print ("\n------------------\n")
        # input()
        nr_sol_searched -= 1
        if nr_sol_searched == 0:
            return nr_sol_searched,"done"
    listSuccesors = gr.generateSuccesors(currentVertex,heuristic_type=heuristic_type)
    global maxVertices 
    maxVertices = max(maxVertices,len(listSuccesors))
    minimum = float("inf")
    for s in listSuccesors:
        nr_sol_searched, rez = build_path(gr, s,limit,nr_sol_searched,start,heuristic_type)
        if rez == "done":
            return nr_sol_searched, "done"
        # print("Compare ", rez, "cu",minimum)
        if rez < minimum:
            minimum = rez
            # print("New minimum:", minimum)
    return nr_sol_searched,minimum


init_path = "D:\Facultate an2 sem2\IA\TEMA 1" 

curr_path_in = init_path + sys.argv[1]
curr_path_out= init_path + sys.argv[2]
nr_sol_searched = int(sys.argv[3])
timeout = float(sys.argv[4])
maxVerticesGen = 0

for filename_in in os.listdir(curr_path_in):
    if filename_in.endswith(".in"):
        
        """A simple *for loop* do find the input files.

        This *for loop* checks in the directory that was given as a path and takes each file from the directory that has the extension .in using *endswith*.

        :param string filename_in: Whole name of a file in the directory

        """

        filename_out,eyt = filename_in.split(".")
        filename_out = filename_out + ".out"

        g = open(curr_path_out + "\\" + filename_out,"a")
        gr = Graph(curr_path_in + "\\" + filename_in)

        print("\n#########\n Solutions obtained with A*: ")
        a_star(gr,nr_sol_searched,"heuristic_2",timeout=timeout)

        g.close()

        print("\n ########### NEW FILE \n")
        
        
