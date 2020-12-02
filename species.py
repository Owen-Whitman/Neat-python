
import values
from random import random, choice, choices, sample
import network
from examples.selfbattleversion import run
from math import floor, ceil
class species():

    def __init__(self, leader):
        self.rep = leader
        self.members = [leader]
        self.members_fitness = {}
        self.prevbestfitness = []
        self.sortedfitness = {}
        self.speciesavg =  0

        
    def evaluate(self):
        best = 0
        unweightedbest = 0
        self.speciesavg = 0
        testamount = values.interspeciestestamount 
        
        played = {}
        
        done = {}
        
            
        
        if(len(self.members)<4):
            for i in self.members:
                played[i] = 0
            for b in range(testamount):
                dic = list(played)
                if(len(self.members) == 1):
                    tocopy = [self.members[0] for i in range(testamount)]
                else:
                    tocopy = sample(dic, k = 4-len(self.members))
                dic.extend(tocopy)
                ret = run(dic)
                for i in ret:
                    i.fullfitness += ret[i]
                    played[i] += 1
            
                
            for i in list(played):
                i.fullfitness /= played[i]
                i.fitness = i.fullfitness/len(self.members)
                if(best == 0 or i.fitness > best.fitness ):
                    best = i
                if(unweightedbest == 0 or i.fullfitness > best.fullfitness):
                    unweightedbest = i  
                self.members_fitness[i] = i.fitness
                added = False
                if(i.fitness in self.sortedfitness):
                    self.sortedfitness[i.fitness].append(i)
                else:
                    self.sortedfitness[i.fitness] = [i]
                
                
                    
                    
        else:
            for i in self.members:
                played[i] = testamount 
            while(len(played) != 0):
                dic = list(played)
                #print(dic)
                if(len(dic)>= 4):
                    ret = run(sample(dic, k = 4))
                    for i in ret:
                        i.fullfitness += ret[i]
                        played[i] -= 1
                        
                        if(played[i] == 0):
                            done[i] = testamount
                            played.pop(i)
                            
                else:
                    finones =  sample(list(done), k = 4-len(dic))
                    dic.extend(finones)
                    ret = run(dic)
                    for i in ret:
                        i.fullfitness += ret[i]
                        if(i in finones):
                            #print(i)
                            done[i] += 1
                        else:
                            played[i] -= 1
                            if(played[i] == 0):
                                done[i] = testamount
                                played.pop(i)
                        
            for i in list(done):
                i.fullfitness /= done[i]
                i.fitness = i.fullfitness/len(self.members)
                if(best == 0 or i.fitness > best.fitness ):
                    best = i
                if(unweightedbest == 0 or i.fullfitness > best.fullfitness):
                    unweightedbest = i  
                self.members_fitness[i] = i.fitness
                added = False
                if(i.fitness in self.sortedfitness):
                    self.sortedfitness[i.fitness].append(i)
                else:
                    self.sortedfitness[i.fitness] = [i]
        
        self.prevbestfitness.append(best.fitness)
        return [best, unweightedbest]
    

    def mutitate(self,globalavg):
        ret_nets = []
        numofnewpopulation = round((self.speciesavg/globalavg)*values.populationsize)
        #print(numofnewpopulation, self.speciesavg, globalavg)
        a = round(values.populationsize*values.top_reproduce)
        sorts = sorted(self.sortedfitness,reverse = True)
        sorted_fitness = []
        keptnet = []
        i = 0
        if(a == 0):
            a = 1

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
        if(numofnewpopulation > 1):
            numofnewpopulation -= 1
    


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
        #print(sorted_fitness)              
        weights = []
        for i in keptnet:
            weights.append(i/sum(keptnet))
        unbabied_size = floor(numofnewpopulation*0.25)
        counter = 0
        addedany = False
        while unbabied_size != 0:
            if(sorted_fitness[counter] not in ret_nets and weights[counter]>random()):
                ret_nets.append(sorted_fitness[counter])
                unbabied_size -= 1
                addedany = True
            if(counter+1 == len(weights)):
                if(not addedany):
                    break
                else:
                    counter = 0
                    addedany = False
            else:
                counter += 1
        numofnewpopulation -=  floor(numofnewpopulation*0.25) - unbabied_size
            
        for i in range(len(ret_nets)):
            if(ret_nets[i] in ret_nets[:i] or ret_nets[i] in ret_nets[i+1:]):
                print("duplicate added!")
                print(ret_nets[i], i)
                raise ValueError


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
        for i in range(len(ret_nets)):
            if(ret_nets[i] in ret_nets[:i] or ret_nets[i] in ret_nets[i+1:]):
                print("duplicate added!")
                raise ValueError
        #print(len(ret_nets))
        return ret_nets

        #print(max(self.members_fitness),self.members_fitness,numofnewpopulation,"YEEE")