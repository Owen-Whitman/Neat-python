from node_connection_genes import connectiongenes, nodegenes
from random import randint, random,uniform
from viznet import connecta2a, node_sequence, NodeBrush, EdgeBrush, DynamicShow
import values
from copy import deepcopy
class network():

    def __init__(self,**kwargs):
        self.nodegenes = []
        self.connectiongenes = []
        self.alikes = {}
        self.nodefromto = {}
        self.layers = {'0.0':[],'1.0':[]}
        self.fitness = 0
        self.fullfitness = 0
        self.enabledgenes = []
        self.disabledgenes = {}
        self.mutitations = []
        if(kwargs != {}):
            self.createbabynet(kwargs['parent1'],kwargs['parent2'])
        else:
            for i in range(values.numofinputs):
                self.nodegenes.append(nodegenes('input',i,values.activationfunctioninput,'0.0'))
                self.nodefromto[i] = {}
                self.alikes[i] = self.nodegenes[i]
                self.layers['0.0'].append(i)
            for i in range(values.numofinputs,values.numofoutputs+values.numofinputs):
                self.nodegenes.append(nodegenes('output',i,values.activationfunctionoutinput,'1.0'))
                self.alikes[i] = self.nodegenes[i]
                self.nodefromto[i] = {}
                self.layers['1.0'].append(i)
            for b in range(0,values.numofinputs,1):
                weight = uniform(values.weightminmax[0],values.weightminmax[1])
                self.nodefromto[5][b] = weight
                self.connectiongenes.append(values.allconnectiongenes[b]['class'])
                self.enabledgenes.append(values.allconnectiongenes[b]['class'])

    def createbabynet(self,parent1,parent2):
        if(parent1.fitness>parent2.fitness):
            fitparent = parent1
            unfitparent = parent2
        else:
            fitparent = parent2
            unfitparent = parent1
            
            
        self.nodegenes = [i.copy() for i in fitparent.nodegenes]
        for i in self.nodegenes:
            self.nodefromto[i.innovation_number] = {}
            self.alikes[i.innovation_number] = i
            if(i.location in self.layers):
                self.layers[i.location].append(i.innovation_number)
            else:
                self.layers[i.location] = [i.innovation_number]
        
        for fitgene in fitparent.connectiongenes:
            
            
            cont = False
            self.connectiongenes.append(fitgene)
            if(fitgene in unfitparent.connectiongenes):
                if(random() < 0.5):

                    if(fitgene in fitparent.enabledgenes):
                        self.enabledgenes.append(fitgene)
                        self.nodefromto[fitgene.outnode][fitgene.innode] = fitparent.nodefromto[fitgene.outnode][fitgene.innode]
                    elif(random() > values.inherit_desabled):
                        self.enabledgenes.append(fitgene)
                        self.nodefromto[fitgene.outnode][fitgene.innode] = fitparent.disabledgenes[fitgene]
                    else:
                        self.disabledgenes[fitgene] = fitparent.disabledgenes[fitgene]         
                else:

                    if(fitgene in unfitparent.enabledgenes):

                        self.enabledgenes.append(fitgene)
                        self.nodefromto[fitgene.outnode][fitgene.innode] = unfitparent.nodefromto[fitgene.outnode][fitgene.innode]

                    elif(random() > values.inherit_desabled):

                        self.enabledgenes.append(fitgene)
                        self.nodefromto[fitgene.outnode][fitgene.innode] = unfitparent.disabledgenes[fitgene]

                    else:
                        self.disabledgenes[fitgene] = unfitparent.disabledgenes[fitgene]
            else:
                if(fitgene in fitparent.enabledgenes):
                    self.enabledgenes.append(fitgene)
                    self.nodefromto[fitgene.outnode][fitgene.innode] = fitparent.nodefromto[fitgene.outnode][fitgene.innode]
                elif(random() > values.inherit_desabled):
                    self.enabledgenes.append(fitgene)
                    self.nodefromto[fitgene.outnode][fitgene.innode] = fitparent.disabledgenes[fitgene]
                else:
                    self.disabledgenes[fitgene] = fitparent.disabledgenes[fitgene] 
        self.mutitations.append("baby was created")            
        self.sort()
                   
    def addconnection(self, innovationnumber,globalconnectiongenes):
        from_node = randint(0,len(self.nodegenes)-1)
        to_node = randint(0,len(self.nodegenes)-1)
        times = 0
        changedinnovationnumber = -1
        while True:
            reset = False
            if((self.nodegenes[to_node].type == 'input' or self.nodegenes[from_node].type =='output') or (float(self.nodegenes[to_node].location) < float(self.nodegenes[from_node].location))):
                placeholer = to_node
                to_node = from_node
                from_node = placeholer
            if(from_node == to_node):
                reset = True
            if(not reset and (self.nodegenes[to_node].type == "input" and self.nodegenes[from_node].type == "input")):
                reset = True
            if(not reset and (self.nodegenes[to_node].type == "output" and self.nodegenes[from_node].type == "output")):
                reset = True
            if(not reset and (float(self.nodegenes[to_node].location) == float(self.nodegenes[from_node].location))):
                reset = True
            if(times > 1000):

                return 'impossible'
            if(not reset):
                for i in self.enabledgenes: 
                    if(i.outnode == self.nodegenes[from_node].innovation_number and i.innode == self.nodegenes[to_node].innovation_number):
                        reset = True
                    if(i.innode == self.nodegenes[from_node].innovation_number and i.outnode == self.nodegenes[to_node].innovation_number):
                        reset = True
            if(reset):
                from_node = randint(0,len(self.nodegenes)-1)
                to_node = randint(0,len(self.nodegenes)-1)
            else:
                from_node = self.nodegenes[from_node].innovation_number
                to_node = self.nodegenes[to_node].innovation_number
                break
            times += 1
        
        for genes in globalconnectiongenes:
            if(genes['from'] == from_node and genes['to'] == to_node):
                print("Heree")
                location = globalconnectiongenes.index(genes)
                innovationnumber = genes['inno']
                if(innovationnumber == -1):
                    innovationnumber = 0
                changedinnovationnumber = 1
                break

        
        
        if(changedinnovationnumber == -1):
            clas = connectiongenes(from_node,to_node,innovationnumber)
            self.connectiongenes.append(clas)
            self.enabledgenes.append(clas)
            weight = uniform(values.weightminmax[0],values.weightminmax[1])
            self.nodefromto[to_node][from_node] = weight
            self.mutitations.append("created two new connections")
            return {'from':from_node,'to':to_node,'inno':innovationnumber,'class':clas}
        else:
            print(globalconnectiongenes[location],innovationnumber)
            clas = globalconnectiongenes[location]['class']
            print(clas,clas.innode,clas.outnode,from_node,to_node)
            if(clas in self.connectiongenes):
                print("in")
                if(clas not in self.enabledgenes):
                    print("indisabled")
                    self.enabledgenes.append(clas)
                    self.nodefromto[to_node][from_node] = self.disabledgenes[clas]
                    self.disabledgenes.pop(clas)
                    self.mutitations.append("moved a disabled connectiongene")
                    return None
                else:
                    print("inenabled")
                    return None
            else:
                print("out")
                weight = uniform(values.weightminmax[0],values.weightminmax[1])
                self.nodefromto[to_node][from_node] = weight
                self.connectiongenes.append(clas)
                self.enabledgenes.append(clas)
                self.mutitations.append("added a previous connection")
                return None
          
    def mutitateconnection(self,nodegenesinno,connectiongenesinno,globalsplitconnections,allconnectiongenes):
        if(len(self.connectiongenes)== 0):
            return None
        gene = randint(0,len(self.connectiongenes)-1)
        #error comes from 
        print(self.nodefromto)
        if(self.connectiongenes[gene] in self.enabledgenes):
            self.disabledgenes[self.connectiongenes[gene]] = self.nodefromto[self.connectiongenes[gene].outnode][self.connectiongenes[gene].innode]
            prevweight = self.nodefromto[self.connectiongenes[gene].outnode][self.connectiongenes[gene].innode]

            del self.nodefromto[self.connectiongenes[gene].outnode][self.connectiongenes[gene].innode] #TODO fix this so it dosent delete whole node in node connection gene if connection is arleady tehere

            self.enabledgenes.remove(self.connectiongenes[gene]) 
            
        else:
            prevweight = self.disabledgenes[self.connectiongenes[gene]]

        
        
        
        for splitconnections in globalsplitconnections:
            if(self.connectiongenes[gene].innode == splitconnections['from'] and self.connectiongenes[gene].outnode == splitconnections['to']):
                if((splitconnections['connection1class'] in self.connectiongenes and splitconnections['connection2class'] in self.connectiongenes)):
                    return "Na"
                
                print("heere")
                #TODO add a check to see if its in connection genes
                print(splitconnections['from'],splitconnections['to'],splitconnections['nodeinno'])

                if(splitconnections['connection1class'] not in self.connectiongenes):
                    print("splitconnectiononeisntin")
                    if(splitconnections['nodeinno'] in self.nodefromto):
                        self.nodefromto[splitconnections['nodeinno']][self.connectiongenes[gene].innode] = 1
                    else:
                        self.nodefromto[splitconnections['nodeinno']] = {self.connectiongenes[gene].innode:1}
                    self.connectiongenes.append(splitconnections['connection1class'])
                    self.enabledgenes.append(splitconnections['connection1class'])
                else:
                    if(splitconnections['connection1class'] in self.disabledgenes):
                        print("1indisabled")
                        if(splitconnections['nodeinno'] in self.nodefromto):
                            self.nodefromto[splitconnections['nodeinno']][self.connectiongenes[gene].innode] = 1
                        else:
                            self.nodefromto[splitconnections['nodeinno']] = {self.connectiongenes[gene].innode:1}
                        self.enabledgenes.append(splitconnections['connection1class'])
                        self.disabledgenes.remove(splitconnections['connection1class'])
                
                if(splitconnections['connection2class'] not in self.connectiongenes):
                    print("splitconnectiontwoisntin")
                    if(self.connectiongenes[gene].outnode in self.nodefromto):
                        self.nodefromto[self.connectiongenes[gene].outnode][splitconnections['nodeinno']] = prevweight  
                    else:
                        self.nodefromto[self.connectiongenes[gene].outnode]= {splitconnections['nodeinno']:prevweight}
                    self.connectiongenes.append(splitconnections['connection2class'])
                    self.enabledgenes.append(splitconnections['connection2class'])
                else:
                    if(splitconnections['connection2class']  in self.disabledgenes):
                        print("2indisabled")
                        if(self.connectiongenes[gene].outnode in self.nodefromto):
                            self.nodefromto[self.connectiongenes[gene].outnode][splitconnections['nodeinno']] = prevweight  
                        else:
                            self.nodefromto[self.connectiongenes[gene].outnode]= {splitconnections['nodeinno']:prevweight}
                        self.enabledgenes.append(splitconnections['connection2class'])
                        self.disabledgenes.remove(splitconnections['connection2class'])
                
                xpos = str((float(self.alikes[self.connectiongenes[gene].innode].location)+float(self.alikes[self.connectiongenes[gene].outnode].location))/2)
                self.nodegenes.append(nodegenes('main',splitconnections['nodeinno'],values.activationfunctionmain,xpos))
                self.alikes[splitconnections['nodeinno']] = self.nodegenes[-1]
                
                if(xpos in self.layers):
                    if(splitconnections['nodeinno'] in self.layers[xpos]):
                        pass
                    else:
                        self.layers[xpos].append(splitconnections['nodeinno'])
                else:
                    self.layers[xpos] = []
                    self.layers[xpos].append(splitconnections['nodeinno'])
                    self.sort()
                
                self.mutitations.append("added a previous split connection")
                for i in self.enabledgenes:
                    test = self.nodefromto[i.outnode][i.innode]
                return None


        xpos = str((float(self.alikes[self.connectiongenes[gene].innode].location)+float(self.alikes[self.connectiongenes[gene].outnode].location))/2)
        self.nodegenes.append(nodegenes('main',nodegenesinno,values.activationfunctionmain,xpos))
        
        self.nodefromto[nodegenesinno] = {self.connectiongenes[gene].innode:1}
        self.nodefromto[self.connectiongenes[gene].outnode][nodegenesinno] = prevweight
        self.alikes[nodegenesinno] = self.nodegenes[-1]
        
        if(xpos in self.layers):
                self.layers[xpos].append(nodegenesinno)
        else:
            self.layers[xpos] = []
            self.layers[xpos].append(nodegenesinno)
            self.sort()
        
        newgene1 = connectiongenes(self.connectiongenes[gene].innode,nodegenesinno,connectiongenesinno)
        newgene2 = connectiongenes(nodegenesinno,self.connectiongenes[gene].outnode,connectiongenesinno+1)
        self.connectiongenes.append(newgene1)
        self.connectiongenes.append(newgene2)
        self.enabledgenes.append(newgene1)
        self.enabledgenes.append(newgene2)
        self.mutitations.append("added a new split connection")
        return {'to':self.connectiongenes[gene].outnode,'from':self.connectiongenes[gene].innode,'nodeinno':nodegenesinno,'connectioninno':connectiongenesinno,'connection1class':newgene1,'connection2class':newgene2}
    
    def sort(self):
        lst = self.layers
        newlst = {}
        sort = sorted([float(i) for i in lst])
        for i in range(len(sort)):
            newlst[str(sort[i])] = []
            newlst[str(sort[i])] = lst[str(sort[i])]
        self.layers = newlst
                      
    def feedforward(self,inputs):
        for i in range(len(inputs)):
            self.alikes[self.layers['0.0'][i]].value = inputs[i]
        for i in self.layers:
            if(i == '0.0'):
                continue
            for b in self.layers[i]:
                total = 0
                for c in self.nodefromto[b]:
                    total += self.alikes[c].value * self.nodefromto[b][c]
                self.alikes[b].value = self.alikes[b].activation(total)        
        return [self.alikes[i].value for i in self.layers["1.0"]]

    def mutitate(self):
        if(random()<values.weight_prebutered_chance):
            for i in self.enabledgenes:
                if(random()<= values.weight_random_chance):
                    newweight = uniform(values.weightminmax[0],values.weightminmax[1])
                    self.nodefromto[i.outnode][i.innode] = newweight
                else:
                    oldweight = self.nodefromto[i.outnode][i.innode]
                    newweight = uniform(oldweight-values.weight_prebuted_added,oldweight+values.weight_prebuted_added)
                    self.nodefromto[i.outnode][i.innode] = newweight
        
        if(values.added_connection_chace >= random()):  
            #print("addedconnection")   
            values.addaconnection(self)
            
        if(values.mutitate_connection_chace >= random()):   
            #print('mutitatedconnectons')  
            values.mutitateaconnection(self)
        
        
    
    def draw(self,name):
        self.sort()
        with DynamicShow(filename="saved_bests\\" + name+".png") as d:
            nodes = []
            numoflayers = 0
            for i in self.layers:
                nodes.append([])
                x = 0
                if(i != '0.0' and i != '1.0'):
                    x = 1
                if(numoflayers == 0):
                    brush = NodeBrush('nn.input', size='normal')
                elif(numoflayers == len(self.layers)-1):
                    brush = NodeBrush('nn.output', size='normal')
                else:
                    brush = NodeBrush('nn.hidden', size='normal')
                for b in self.layers[i]:
                    c = brush >> (numoflayers,x)
                    if(brush.style == 'nn.output' and x == 0):
                        c.text("score:"+str(self.fullfitness),'bottom')
                    c.text(str(b),'center')
                    nodes[numoflayers].append(c)
                    x += 1
                numoflayers += 1
            edge = EdgeBrush('->-', lw=2)
            for a in range(len(nodes)):
                selflayersa = self.layers[sorted(self.layers)[a]]
                if(a == 0 ):
                    continue
                for b in range(len(nodes[a])):
                    for i in self.nodefromto[selflayersa[b]]:
                        for one in range(len(nodes)):
                            for two in range(len(nodes[one])):
                                if(i == self.layers[sorted(self.layers)[one]][two]):
                                   e = edge >> (nodes[one][two],nodes[a][b])
                                   e.text(str(round(self.nodefromto[selflayersa[b]][i],4)),'top')
                                   break
                               
    def copy(self):
        return deepcopy(self)
        