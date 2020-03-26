from examples.xor import run 
import values
from random import random, choice, choices
import network
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
        self.speciesavg = 0 
        for i in self.members:
            #print(i)
            i.fullfitness = run(i)
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
        #print(len(self.members_fitness))
        self.prevbestfitness.append(best.fitness)
        return [self.speciesavg, best]
    

    def mutitate(self,globalavg):
        ret_nets = []
        numofnewpopulation = floor((self.speciesavg/globalavg)*values.populationsize)
        #print(numofnewpopulation)
        a = round(values.populationsize*values.top_reproduce)
        sorts = sorted(self.sortedfitness,reverse = True)
        sortedfitness = []
        keptnet = []
        i = 0
        #print(sorts)
        while a > 0:
            if( a - len(self.sortedfitness[sorts[i]]) > 0):
                sortedfitness.extend(self.sortedfitness[sorts[i]])
                keptnet.extend([sorts[i] for b in range(len(self.sortedfitness[sorts[i]]))])
                a -= len(self.sortedfitness[sorts[i]])
                if(i + 1 > len(sorts) -1):
                    a = 0
                    break
                i += 1
            else:

                sortedfitness.extend(self.sortedfitness[sorts[i]][:int(len(self.sortedfitness[sorts[i]])-a)])
                keptnet.extend([sorts[i] for b in range(len(self.sortedfitness[sorts[i]][:int(len(self.sortedfitness[sorts[i]])-a)]))])
                a = 0
        #print(len(sortedfitness),len(keptnet))
        #sortedfitness = sorted(self.sortedfitness,reverse = True)[:ceil(len(self.sortedfitness)*values.top_reproduce)]
        



        #print(self.members_fitness)
        newmembers = {}
        for i in range(len(keptnet)):
            newmembers[keptnet[i]] = sortedfitness[i]
        

        self.members_fitness = newmembers 
        #self.members = keptnet
        if(numofnewpopulation> 1):
            a= sortedfitness[0].copy()
            ret_nets.append(a)
            numofnewpopulation -= 1

        self.rep = choice(sortedfitness).copy()


        
        #print(sortedfitness)
             
        for i in sortedfitness:
            i.mutitate()
            
        ret_nets.extend(choices(sortedfitness,keptnet,k=floor(numofnewpopulation*0.25)))
        numofnewpopulation -= floor(numofnewpopulation*0.25)
        print("creating babies")
        while(numofnewpopulation>0):

            choic = choices(sortedfitness,keptnet,k=2)
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