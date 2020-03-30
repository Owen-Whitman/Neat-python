from network import network
from species import species
import values
import pickle
from examples.xor import run 
from copy import deepcopy
allnetworks = []
allspecies = []
    
            
 
    
def closeness(net1, net2):
    net1_geneinno = [i.innovation_number for i in net1.connectiongenes]
    net2_geneinno = [i.innovation_number for i in net2.connectiongenes]
     
    if(net1_geneinno[-1] < net2_geneinno[-1]):
        placeholer = net1_geneinno
        net1_geneinno = net2_geneinno
        net2_geneinno = placeholer
        
        placeholer = net1
        net1 = net2
        net2 = placeholer
    #print(len(net1_geneinno),len(net1.connectiongenes),type(net1_geneinno[0]))
    

    net1_locations = [x for x,_ in sorted(set(zip(net1.connectiongenes,net1_geneinno)), key=lambda x: x[1])]
    net2_locations = [x for x,_ in sorted(set(zip(net2.connectiongenes,net2_geneinno)), key=lambda x: x[1])]
    #print(net1_locations,net2_locations)
    net1_geneinno = sorted(net1_geneinno)
    net2_geneinno = sorted(net2_geneinno)

    
    alike = 0
    alike_weightdifference = 0
    disjoint = 0 
    excess = 0 
    #thanks finn for the insperation on this part!
    index1 = 0
    index2 = 0
    while(index1 < len(net1.connectiongenes) and index2 < len(net2.connectiongenes)):
        location1 = net1_geneinno[index1]
        location2 = net2_geneinno[index2]

        if(location1 == location2):
            alike += 1 
            if(net1_locations[index1] in net1.disabledgenes):
                net1_weight = net1.disabledgenes[net1_locations[index1]]
            else:
                net1_weight = net1.nodefromto[net1_locations[index1].outnode][net1_locations[index1].innode]
            if(net2_locations[index2] in net2.disabledgenes):
                net2_weight = net2.disabledgenes[net2_locations[index2]]
            else:
                net2_weight = net2.nodefromto[net2_locations[index2].outnode][net2_locations[index2].innode]
            alike_weightdifference += abs(net1_weight - net2_weight)
            index1 += 1
            index2 += 1
        if(location1 > location2):
            disjoint += 1
            index2 += 1
        if(location1 < location2):
            disjoint += 1
            index1 += 1
            
    excess = len(net1.connectiongenes) - index1

    if(len(net1.connectiongenes) <= 20 and len(net2.connectiongenes) <= 20):
        n = 1
    else:
        n = max(len(net1.connectiongenes),len(net2.connectiongenes))
    return ((values.c1*excess)/n)+((values.c2*disjoint)/n)+(values.c3*(alike_weightdifference/alike))


    
def createtestnet():
    net = network()
    values.addaconnection(net)
    values.mutitateaconnection(net)
    values.addaconnection(net)
    #net.mutitate()
    values.addaconnection(net)
    values.mutitateaconnection(net)
    values.addaconnection(net)
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

globalbest = 0 

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
    bestunweighted = 0
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
        
        if(bestunweighted == 0 or a[1].fullfitness > bestunweighted.fullfitness):
            bestunweighted = a[1]
    if(globalbest == 0 or bestunweighted.fullfitness > globalbest.fullfitness):
        globalbest = bestunweighted.copy()
    print("evaluated")
    print("size of prev pop", sizeofpop)
    print("numofspecies", len(allspecies))
    
    print("gen"+str(mainstuff))
    print("best fitness weightd", best.fitness)
    '''if(mainstuff%10 == 0 and mainstuff != 1):
        bestunweighted.draw("gen " + str(mainstuff))'''
    print("best fitness unweighted", bestunweighted.fullfitness)
    
    for i in allspecies:
        allnetworks.extend(i.mutitate(avg))

    sizeofpop = len(allnetworks)
    generation += 1
    print("mutitated")
    
    print(" ")

print("  ")
print("done")
print(run(globalbest))
print(globalbest.fullfitness)
#print(globalbest.draw("finalscore"))
