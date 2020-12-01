
import values
from random import random, choice, choices
import network
from examples.xor import run
from math import floor, ceil
class species():

    def __init__(self, leader):
        self.rep = leader
        self.members = [leader]
        self.members_fitness = {}
        self.prevbestfitness = []
        self.sortedfitness = {}
        self.speciesavg =  -1

        
    def evaluate(self):
        best = 0
        unweightedbest = 0
        self.speciesavg = 0 
        for i in self.members: 
            i.fullfitness = run(i)
            if(unweightedbest == 0 or i.fullfitness> unweightedbest.fullfitness):
                unweightedbest = i 
            fitness =  i.fullfitness/len(self.members)
            if(best == 0 or fitness > best.fitness ):
                best = i
            
            i.fitness = fitness
            self.members_fitness[i] = fitness
            added = False
            if(fitness in self.sortedfitness):
                self.sortedfitness[fitness].append(i)
            else:
                self.sortedfitness[fitness] = [i]
                
            self.speciesavg += fitness

        self.speciesavg = self.speciesavg/len(self.members)
        self.prevbestfitness.append(best.fitness)
        return [self.speciesavg, best, unweightedbest]
    

    def mutitate(self,globalavg):
        ret_nets = []
        numofnewpopulation = floor((self.speciesavg/globalavg)*values.populationsize)
        print(numofnewpopulation)
        a = round(values.populationsize*values.top_reproduce)
        sorts = sorted(self.sortedfitness,reverse = True)
        sorted_fitness = []
        keptnet = []
        i = 0
        if(a == 0):
            a = 1
        #print(sorts)
        
        while a > 0:
            if( a - len(self.sortedfitness[sorts[i]]) > 0):
                sorted_fitness.extend(self.sortedfitness[sorts[i]])
                keptnet.extend([sorts[i] for b in range(len(self.sortedfitness[sorts[i]]))])
                a -= len(self.sortedfitness[sorts[i]])
                if(i + 1 > len(sorts) -1):
                    a = 0
                    break
                i += 1
            else:
                
                sorted_fitness.extend(self.sortedfitness[sorts[i]][:int(len(self.sortedfitness[sorts[i]])-a)])
                keptnet.extend([sorts[i] for b in range(len(self.sortedfitness[sorts[i]][:int(len(self.sortedfitness[sorts[i]])-a)]))])
                a = 0

        a= sorted_fitness[0].copy()
        a.connectiongenes = [i for i in sorted_fitness[0].connectiongenes]
        a.enabledgenes = [i for i in sorted_fitness[0].enabledgenes]
            
        a.disabledgenes = {}
        for i in sorted_fitness[0].disabledgenes:
            a.disabledgenes[i] = sorted_fitness[0].disabledgenes[i]
        ret_nets.append(a)




        newmembers = {}
        for i in range(len(keptnet)):
            newmembers[keptnet[i]] = sorted_fitness[i]
        

        self.members_fitness = newmembers 
        #self.members = keptnet
        

        try:
            self.rep = choice(sorted_fitness).copy()
        except:
            print(len(self.members))
            print(sorted_fitness)
            print(self.members_fitness)
            raise ArithmeticError
        #print(ret_nets[0].nodefromto)     
        for i in sorted_fitness:
            i.mutitate()
        #print(ret_nets[0].nodefromto)               
            
        ret_nets.extend(choices(sorted_fitness,keptnet,k=floor(numofnewpopulation*0.25)))
        numofnewpopulation -= floor(numofnewpopulation*0.25)

        while(numofnewpopulation>0):

            choic = choices(sorted_fitness,keptnet,k=2)
            person1 = choic[0]
            person2 = choic[1]

            
            ret_nets.append(network.network(parent1 = person1,parent2=person2))
                
            numofnewpopulation -= 1
       
       
        self.members = []

        self.members_fitness = {}
        self.sortedfitness = {}
        #print(len(ret_nets))

        return ret_nets

        #print(max(self.members_fitness),self.members_fitness,numofnewpopulation,"YEEE")