from network import network
from species import species
import values
import pickle
from examples.xor import run 
from copy import deepcopy
allnetworks = []
allspecies = []

def closeness(net1, net2):
    alike = 0
    alike_weightdifference = 0
    disjoint = 0 
    excess = 0 
    for i in net1.connectiongenes:
        alikes = False
        for b in net2.connectiongenes:
            if(i.innovation_number == b.innovation_number):
                alikes = True
                alike += 1
                alike_weightdifference += abs(i.weight - b.weight)
                break
        if(not alike):
            disjoint += 1
    
    if(len(net1.connectiongenes)>len(net2.connectiongenes)):
        excess = len(net1.connectiongenes) - len(net2.connectiongenes)
        disjoint += len(net2.connectiongenes) - alike
                
    elif(len(net1.connectiongenes)==len(net2.connectiongenes)):
        excess = 0
        disjoint += len(net2.connectiongenes) - alike
    
    else:
        excess = len(net2.connectiongenes) - len(net1.connectiongenes)
        disjoint += len(net2.connectiongenes) - alike - excess
    if(alike == 0):
        return ((values.c1*excess)/values.n)+((values.c2*disjoint)/values.n)
    if(len(net1.connectiongenes)<= 20 and len(net2.connectiongenes)<=20):
        return ((values.c1*excess)/values.n)+((values.c2*disjoint)/values.n)+(values.c3*(alike_weightdifference/alike))
    return (values.c1*excess)+(values.c2*disjoint)+(values.c3*(alike_weightdifference/alike))

    
def createtestnet():
    net = network()
    values.addaconnection(net)
    values.addaconnection(net)
    values.mutitateaconnection(net)
    values.addaconnection(net)
    values.addaconnection(net)
    #net.mutitate()
    return net

def save(gen,best):

    class Container(object):
        def __init__(self,allspecies,best,gen):
            self.allspecies = allspecies
            self.best = best
            self.gen = gen
    cont = Container(allspecies,best,gen)
    with open("saved_bests/"+str(gen)+"xor"+".pk1",'wb') as pickle_file:
        pickle.dump(cont,pickle_file)

for i in range(values.populationsize):
    allnetworks.append(network())
sizeofpop = values.populationsize
generation = 1



for mainstuff in range(0,100):
    for i in range(len(allnetworks)-1,-1,-1):
        found = False
        for b in allspecies:
            if(closeness(allnetworks[i],b.rep) < values.closeness):
                b.members.append(allnetworks[i])
                found = True
                break
        if(not found):
            allspecies.append(species(allnetworks[i]))
        allnetworks.pop(i)
        
    if(len(allspecies)<values.species_target):
        values.closeness -= 0.3
    elif(len(allspecies)>values.species_target):
        values.closeness += 0.3
    if(values.closeness<0.3):
        values.closeness = 0.3
    print("added")
    print("numofspecies", len(allspecies))
    avg = 0 
    best = 0
    for i in range(len(allspecies)-1,-1,-1):
        if(len(allspecies[i].members) <= 1): 
            allspecies.pop(i)
            continue
        if(len(allspecies[i].prevbestfitness)>=15 and max(allspecies[i].prevbestfitness[:len(allspecies[i].prevbestfitness)-14])>= max(allspecies[i].prevbestfitness[len(allspecies[i].prevbestfitness)-14:])):
            for b in allspecies[i].members:
                allnetworks.append(b)
            allspecies.pop(i)
            continue

    for i in allspecies:
        a = i.evaluate()
        avg += a[0]
        if(best == 0 or a[1].fitness > best.fitness):
            best = a[1]
    print("evaluated")
    print("size of prev pop", sizeofpop)
    print("numofspecies", len(allspecies))
    
    print("gen"+str(mainstuff))
    '''if(mainstuff%10 == 0):
        best.draw("gen"+str(mainstuff))'''
    print(best)
    print(best.fitness)

    runerup = run(best)
    print(runerup)
    if(runerup> 3.5):
        print("done")
        best.draw("gen"+str(mainstuff))
        break
    
    for i in allspecies:

        allnetworks.extend(i.mutitate(avg))

    sizeofpop = len(allnetworks)
    generation += 1
    print("mutitated")
    print(" ")

print("  ")
print("done")
print(run(best))
print(best.fitness)
