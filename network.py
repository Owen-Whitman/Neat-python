from node_connection_genes import connectiongenes, nodegenes
from random import randint, random,uniform
import values


class network():

    def __init__(self,**kwargs):
        self.nodegenes = []
        self.connectiongenes = []
        self.fitness = random()
        self.order = [0,1,2,3] 
        self.nodefromto = {}
        self.score = 0
        if(kwargs != {}):
            self.createbabynet(kwargs['parent1'],kwargs['parent2'])
        else:
            for i in range(values.numofinputs):
                self.nodegenes.append(nodegenes('input',i,values.activationfunctioninput))
                self.nodefromto[i] = {}
            for i in range(values.numofinputs,values.numofoutputs+values.numofinputs):
                self.nodegenes.append(nodegenes('output',i,values.activationfunctionoutinput))
                self.nodefromto[i] = {}
            for b in range(0,values.numofinputs,1):
                weight = uniform(values.weightminmax[0],values.weightminmax[1])
                self.nodefromto[3][b] = weight
                self.connectiongenes.append(connectiongenes(b,3,uniform(-2,2),True,i))

    def createbabynet(self,parent1,parent2):
        if(parent1.fitness>parent2.fitness):
            fitparent = parent1
            unfitparent = parent2
        else:
            fitparent = parent2
            unfitparent = parent2
            
        if(fitparent.fitness == unfitparent.fitness):
            for fitgene in fitparent.connectiongenes:
                cont = False
                for unfitgene in unfitparent.connectiongenes:
                    if(fitgene.innovation_number == unfitgene.innovation_number):
                        cont = True
                        if(random() > 0.5):
                            self.connectiongenes.append(fitgene.copy())
                            if(not fitgene.enabled and random() > values.inherit_desabled):
                                self.connectiongenes[-1].enabled = True
                        else:
                            self.connectiongenes.append(unfitgene.copy())
                            if(not fitgene.enabled and random() > values.inherit_desabled):
                                self.connectiongenes[-1].enabled = True
                if(not cont):
                    self.connectiongenes.append(fitgene.copy())
                    if(not fitgene.enabled and random() > values.inherit_desabled):
                        self.connectiongenes[-1].enabled = True
                    
            for unfitgene in unfitparent.connectiongenes:
                cont = False
                for fitgene in fitparent.connectiongenes:
                    if(fitgene.innovation_number == unfitgene.innovation_number):
                        cont = True
                if(not cont):
                    self.connectiongenes.append(fitgene.copy())
                    if(not fitgene.enabled and random() > values.inherit_desabled):
                        self.connectiongenes[-1].enabled = True
            for i in fitparent.nodegenes:
                self.nodegenes.append(i.copy())
            for i in unfitparent.nodegenes:
                self.nodegenes.append(i.copy())
            return
        
        for fitgene in fitparent.connectiongenes:
            cont = False
            for unfitgene in unfitparent.connectiongenes:
                if(fitgene.innovation_number == unfitgene.innovation_number):
                    cont = True
                    if(random() > 0.5):
                        self.connectiongenes.append(fitgene.copy())
                        if(random() > values.inherit_desabled and not fitgene.enabled):
                            self.connectiongenes[-1].enabled = True
                    else:
                        self.connectiongenes.append(unfitgene.copy())
                        if(random() > values.inherit_desabled and not fitgene.enabled):
                            self.connectiongenes[-1].enabled = True
            if(not cont):
                self.connectiongenes.append(fitgene.copy())
                if(not fitgene.enabled and random() > values.inherit_desabled):
                    self.connectiongenes[-1].enabled = True
                        
        self.nodegenes = [i.copy() for i in fitparent.nodegenes]

    def checkforproblem(self,fnumber,tnumber):
        for i in self.nodegenes:
            if((fnumber == i.innovation_number and i.type == 'input') or (tnumber == i.innovation_number and i.type == 'input')):
                return True
        for i in self.connectiongenes:
            if(tnumber == i.outnode):
                if(i.innode == fnumber and i.enabled == False):
                    return False
                else:
                    if(self.checkforproblem(fnumber,i.innode)):
                        continue
                    else:
                        return False
                    
    def addconnection(self, innovationnumber,globalconnectiongenes):
        from_node = randint(0,len(self.nodegenes)-1)
        to_node = randint(0,len(self.nodegenes)-1)
        times = 0
        while True:
            reset = False
            if(self.nodegenes[to_node].type == 'input' or self.nodegenes[from_node].type =='output'):
                placeholer = to_node
                to_node = from_node
                from_node = placeholer
            if(from_node == to_node):
                reset = True
            for i in self.connectiongenes:
                if(i.outnode == self.nodegenes[from_node].innovation_number and i.innode == self.nodegenes[to_node].innovation_number):
                    reset = True
                if(i.innode == self.nodegenes[from_node].innovation_number and i.outnode == self.nodegenes[to_node].innovation_number):
                    reset = True
            if(self.nodegenes[to_node].type == "input" and self.nodegenes[from_node].type == "input"):
                reset = True
            if(self.nodegenes[to_node].type == "output" and self.nodegenes[from_node].type == "output"):
                reset = True
            if(times > 1000):
                return 'impossible'
            if(reset != True and self.checkforproblem(from_node,to_node) == False):
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
                innovationnumber = genes['inno']
                break
        weight = uniform(values.weightminmax[0],values.weightminmax[1])
        self.nodefromto[to_node][from_node] = weight
        self.connectiongenes.append(connectiongenes(from_node,to_node,weight,True,innovationnumber))
        self.sort()
        return {'from':from_node,'to':to_node,'inno':innovationnumber}
    
    def mutitateconnection(self,nodegenesinno,connectiongenesinno,globalsplitconnections):
        if(len(self.connectiongenes)== 0):
            return None
        gene = randint(0,len(self.connectiongenes)-1)
        while not self.connectiongenes[gene].enabled:
            gene = randint(0,len(self.connectiongenes)-1)
        self.connectiongenes[gene].enabled = False
        del self.nodefromto[self.connectiongenes[gene].outnode][self.connectiongenes[gene].innode]
        for splitconnections in globalsplitconnections:
            if(self.connectiongenes[gene].outnode == splitconnections['from'] and self.connectiongenes[gene].innode == splitconnections['to']):
                if( splitconnections['nodeinno']in self.nodegenes and  splitconnections['connectioninno'] in self.connectiongenes):
                    print("HEIUHIHJKFH:DAS")
                    return None
                nodegenesinno = splitconnections['nodeinno']
                connectiongenesinno = splitconnections['connectioninno']
        self.nodegenes.append(nodegenes('main',nodegenesinno,values.activationfunctionmain))
        self.nodefromto[nodegenesinno] = {self.connectiongenes[gene].innode:1}
        self.nodefromto[self.connectiongenes[gene].outnode][nodegenesinno] = self.connectiongenes[gene].weight
        self.connectiongenes.append(connectiongenes(self.connectiongenes[gene].innode,nodegenesinno,1,True,connectiongenesinno))
        self.connectiongenes.append(connectiongenes(nodegenesinno,self.connectiongenes[gene].outnode,self.connectiongenes[gene].weight,True,connectiongenesinno+1))
        self.sort()
        return {'from':self.connectiongenes[gene].outnode,'to':self.connectiongenes[gene].innode,'nodeinno':nodegenesinno,'connectioninno':connectiongenesinno}
    
    def feedforward(self,inputs):
        alikes = {}
        for i in self.nodegenes:
            alikes[i.innovation_number] = i
        value = {}
        output = []
        for i in self.order:
            if(alikes[i].type == 'input'):
                value[i] = inputs[i]
                continue
            total = 0
            for b in self.nodefromto[i]:
                total += value[b] * self.nodefromto[i][b]
            value[i] =  alikes[i].activation(total)
        print(inputs, [value[values.numofinputs + i] for i in range(values.numofoutputs)])
        return [value[values.numofinputs + i] for i in range(values.numofoutputs)]

    def mutitate(self):
        if(random()<values.weight_prebutered_chance):
            print("changing weights")
            for i in self.connectiongenes:
                if(random()<= values.weight_random_chance):
                    i.weight = uniform(values.weightminmax[0],values.weightminmax[1])
                    self.nodefromto[i.outnode][i.innode] = i.weight
                else:
                    i.weight = uniform(i.weight-values.weight_prebuted_added,i.weight+values.weight_prebuted_added)
                    self.nodefromto[i.outnode][i.innode] = i.weight
        
        if(values.added_connection_chace <= random()):  
            print("addedconnection")   
            values.addaconnection(self)
            
        if(values.mutitate_connection_chace <= random()):   
            print('mutitatedconnectons')  
            values.mutitateaconnection(self)
    
    def sort(self):
        order = [i.innovation_number for i in self.nodegenes]
        print(order,"sorting",self.nodefromto)
        while True:
            brake = True
            for i in order:
                for b in self.nodefromto[i]:
                    if(order.index(b)>order.index(i)):
                        brake = False
                        order.remove(i)
                        order.insert(order.index(b)+1,i)
            if(brake):
                break
            #print(order)
        print("donesorting",order)
        self.order = order