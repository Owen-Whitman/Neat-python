from node_connection_genes import connectiongenes, nodegenes
from random import randint, random

class network():
    def __init__(self,numinputs,numoutputs,**kwargs):
        self.nodegenes = []
        self.connectiongenes = []
        self.fitness = random()
        if(kwargs != {}):
            self.createbabynet(kwargs['parent1'],kwargs['parent2'])
        else:
            for i in range(numinputs):
                self.nodegenes.append(nodegenes('input',i))
            for i in range(numinputs,numoutputs+numinputs):
                self.nodegenes.append(nodegenes('output',i))
                
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
                    print(fitgene.enabled,'before')
                    self.connectiongenes.append(fitgene)
                    self.connectiongenes[-1].enabled = not self.connectiongenes[-1].enabled
                    print(fitgene.enabled,'after')
            for unfitgene in unfitparent.connectiongenes:
                cont = False
                for fitgene in fitparent.connectiongenes:
                    if(fitgene.innovation_number == unfitgene.innovation_number):
                        cont = True
                if(not cont):
                    self.connectiongenes.append(fitgene)
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
    
    def addconnection(self, innovationnumber,globalconnectiongenes):
        from_node = randint(0,len(self.nodegenes)-1)
        to_node = randint(0,len(self.nodegenes)-1)
        times = 0
        while True:
            reset = False
            print(from_node,to_node)
            for i in self.connectiongenes:
                if(i.outnode == self.nodegenes[from_node].innovationnumber and i.innumber == self.nodegenes[to_node].innovationnumber):
                    reset = True
                if(i.innode == self.nodegenes[from_node].innovationnumber and i.outnumber == self.nodegenes[to_node].innovationnumber):
                    reset = True
            if(self.nodegenes[to_node].type == "input" and self.nodegenes[from_node].type == "input"):
                reset = True
            if(self.nodegenes[to_node].type == "output" and self.nodegenes[from_node].type == "output"):
                reset = True
            if(times > 100):
                return 'impossible'
            if(reset):
                from_node = randint(0,len(self.nodegenes)-1)
                to_node = randint(0,len(self.nodegenes)-1)
            else:
                break
            times += 1
        if(to_node == 'input' or from_node =='output'):
            placeholer = to_node
            to_node = from_node
            from_node = placeholer
        for genes in globalconnectiongenes:
            if(genes['from'] == from_node and genes['to'] == to_node):
                innovationnumber = genes['inno']
                break
        self.connectiongenes.append(connectiongenes(from_node,to_node,random(),True,innovationnumber))
        return {'from':from_node,'to':to_node,'inno':innovationnumber}
    
    def mutitateconnection(self,nodegenesinno,connectiongenesinno,globalsplitconnections):
        '''if(len(self.connectiongenes)== 0):
            self.addconnection(connectiongenesinno)'''
        gene = randint(0,len(self.connectiongenes)-1)
        self.connectiongenes[gene].enabled = False
        for splitconnections in globalsplitconnections:
            if(self.connectiongenes[gene].outnode == splitconnections['from'] and self.connectiongenes[gene].innode == splitconnections['to']):
                nodegenesinno = splitconnections['nodeinno']
                connectiongenesinno = splitconnections['connectioninno']
        self.nodegenes.append(nodegenes('main',nodegenesinno))
        self.connectiongenes.append(connectiongenes(self.connectiongenes[gene].innode,nodegenesinno,1,True,connectiongenesinno))
        self.connectiongenes.append(connectiongenes(nodegenesinno,self.connectiongenes[gene].outnode,self.connectiongenes[gene].weight,True,connectiongenesinno+1))
        return {'from':self.connectiongenes[gene].outnode,'to':self.connectiongenes[gene].innode,'nodeinno':nodegenesinno,'connectioninno':connectiongenesinno}