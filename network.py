from node_connection_genes import connectiongenes, nodegenes
from random import randint, random
import values


class network():

    def __init__(self,**kwargs):
        self.nodegenes = []
        self.connectiongenes = []
        self.fitness = random()
        self.order = [] #TODO work on order for feedforward
        if(kwargs != {}):
            self.createbabynet(kwargs['parent1'],kwargs['parent2'])
        else:
            for i in range(values.numofinputs):
                self.nodegenes.append(nodegenes('input',i,values.activationfunctioninput))

            for i in range(values.numofinputs,values.numofoutputs+values.numofinputs):
                self.nodegenes.append(nodegenes('output',i,values.activationfunctionoutinput))
                
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
                        else:
                            self.connectiongenes.append(unfitgene.copy())
                if(not cont):
                    self.connectiongenes.append(fitgene.copy())
                    
            for unfitgene in unfitparent.connectiongenes:
                cont = False
                for fitgene in fitparent.connectiongenes:
                    if(fitgene.innovation_number == unfitgene.innovation_number):
                        cont = True
                if(not cont):
                    self.connectiongenes.append(fitgene.copy())
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
                    else:
                        self.connectiongenes.append(unfitgene.copy())
            if(not cont):
                self.connectiongenes.append(fitgene.copy())
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
                break
            times += 1
        for genes in globalconnectiongenes:
            if(genes['from'] == from_node and genes['to'] == to_node):
                innovationnumber = genes['inno']
                break
        self.connectiongenes.append(connectiongenes(from_node,to_node,random(),True,innovationnumber))
        return {'from':from_node,'to':to_node,'inno':innovationnumber}
    
    def mutitateconnection(self,nodegenesinno,connectiongenesinno,globalsplitconnections):
        if(len(self.connectiongenes)== 0):
            return None
        gene = randint(0,len(self.connectiongenes)-1)
        self.connectiongenes[gene].enabled = False
        for splitconnections in globalsplitconnections:
            if(self.connectiongenes[gene].outnode == splitconnections['from'] and self.connectiongenes[gene].innode == splitconnections['to']):
                nodegenesinno = splitconnections['nodeinno']
                connectiongenesinno = splitconnections['connectioninno']
        self.nodegenes.append(nodegenes('main',nodegenesinno,values.activationfunctionmain))
        self.connectiongenes.append(connectiongenes(self.connectiongenes[gene].innode,nodegenesinno,1,True,connectiongenesinno))
        self.connectiongenes.append(connectiongenes(nodegenesinno,self.connectiongenes[gene].outnode,self.connectiongenes[gene].weight,True,connectiongenesinno+1))
        return {'from':self.connectiongenes[gene].outnode,'to':self.connectiongenes[gene].innode,'nodeinno':nodegenesinno,'connectioninno':connectiongenesinno}