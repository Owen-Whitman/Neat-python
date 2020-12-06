from random import choices, sample
from network import network
from species import species
from keyboard import is_pressed
import values
from time import time
import matplotlib.pyplot as plt
from os import getcwd, path
from examples.selfbattleversion import run

t0 = time()



allnetworks = []
allspecies = []
generation = 1

x = []
best_scores = []
best_unweighted_scores = []
best_number_nodes = []
best_number_connections = []
averages = []
population_size = []
time_per_generation = []
numspecies_per_generation = []
besteverscore = 0
ylabels = ["best network's weighted fitness", "best network's unweighted fitness",
           "number of nodes for the best network", "number of connections for the best network", 
           "average fitness", "population size", "number of species", "time per generation"]
root=getcwd()
file_path = path.join(root,"saved","saved_data.txt") #C:\Users\owenw\Desktop\Battle snakes\local learning\Neat-python\saved\saved_data.txt
write_file = open(file_path,'w')
fig, axs = plt.subplots(2,4, sharex = True)
axsummer = 0
for ax in axs.flat:
    ax.set(ylabel = ylabels[axsummer])
    axsummer += 1 

values.setup()

def savedata(avg,best,bestunweighted, totaltime, numspecies, t1,t2,t3):
    global besteverscore
    # best.score bestunweighted.score, len(bestunweighted.nodegenes), len(bestunweighted.connectiongenes), avg, values.populationsize, numspecies, time
    x.append(generation)
    best_scores.append(best.fitness)
    best_unweighted_scores.append(bestunweighted.fullfitness)
    best_number_nodes.append(len(bestunweighted.nodegenes))
    best_number_connections.append(len(bestunweighted.connectiongenes))
    averages.append(avg)
    population_size.append(len(allnetworks))
    numspecies_per_generation.append(numspecies)
    time_per_generation.append(totaltime)
    if(len(x) > 150):
        start = len(x)-150
        axs[0,0].plot(x[start:],best_scores[start:])
        axs[0,1].plot(x[start:],best_unweighted_scores[start:])
        axs[0,2].plot(x[start:],best_number_nodes[start:])
        axs[0,3].plot(x[start:],best_number_connections[start:])
        axs[1,0].plot(x[start:],averages[start:])
        axs[1,1].plot(x[start:],population_size[start:])
        axs[1,2].plot(x[start:],numspecies_per_generation[start:])
        axs[1,3].plot(x[start:],time_per_generation[start:])
    else:
        axs[0,0].plot(x,best_scores)
        axs[0,1].plot(x,best_unweighted_scores)
        axs[0,2].plot(x,best_number_nodes)
        axs[0,3].plot(x,best_number_connections)
        axs[1,0].plot(x,averages)
        axs[1,1].plot(x,population_size)
        axs[1,2].plot(x,numspecies_per_generation)
        axs[1,3].plot(x,time_per_generation)
    plt.pause(0.05)
    write_file.write("generation"+ str(generation) +":\n")
    write_file.write("best score weighted: "+ str(best_scores[-1])+ "\n")
    write_file.write("best score unweighted: "+ str(best_unweighted_scores[-1])+ "\n")
    write_file.write("best number nodes: "+ str(best_number_nodes[-1])+ "\n")
    write_file.write("best number connections: "+ str(best_number_connections[-1])+ "\n")
    write_file.write("average score for this generation: "+ str(averages[-1])+ "\n")
    write_file.write("population size: "+ str(population_size[-1])+ "\n")
    write_file.write("number of species: "+ str(numspecies_per_generation[-1])+ "\n")
    write_file.write("time took to create species" + str(t1) + "\n")
    write_file.write("time took to evaulate" + str(t2) + "\n")
    write_file.write("time took to mutitate" + str(t3) + "\n")
    write_file.write("time took for this generation: "+ str(time_per_generation[-1])+ "\n")
    if(besteverscore == 0 or bestunweighted.fullfitness  > besteverscore):
        besteverscore = bestunweighted.fullfitness
    write_file.write("best score so far: " + str(besteverscore) + "\n")
    write_file.write("best score weighted avg: "+ str(sum(best_scores)/len(best_scores))+ "\n")
    write_file.write("best score unweighted avg: " + str(sum(best_scores)/len(best_scores))+ "\n")
    write_file.write("average score for all generations: "+ str(sum(averages)/len(averages))+ "\n")
    write_file.write("average time took per generation: "+ str(sum(time_per_generation)/len(time_per_generation))+ "\n")
    write_file.write("total time up to this point: "+ str(int(round(time()))-int(round(t0)))+ "\n")
    write_file.write("best structure:")
    write_file.write(str(bestunweighted.nodefromto))
    write_file.write("\n")
    write_file.write("\n")

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

def createspecies():
    for i in range(len(allnetworks)-1,-1,-1):
        
        found = False
        for b in allspecies:
            if(closeness(allnetworks[i],b.rep) < values.closeness):
                b.members.append(allnetworks[i])
                found = True

        if(not found):
            allspecies.append(species(allnetworks[i]))
            
        allnetworks.pop(i)
            

    for i in range(len(allspecies)-1,-1,-1):
        if(len(allspecies[i].members) <= 1):
            for b in allspecies[i].members:

                allnetworks.append(b)
            allspecies.pop(i)
            continue
        if(len(allspecies[i].prevbestfitness)>=15 and max(allspecies[i].prevbestfitness[:len(allspecies[i].prevbestfitness)-14])>= max(allspecies[i].prevbestfitness[len(allspecies[i].prevbestfitness)-14:])):
            for b in allspecies[i].members:
                allnetworks.append(b)
            allspecies.pop(i)
            continue
    if(len(allnetworks)>=2):
        allspecies.append(species(allnetworks[0]))
        allnetworks.pop(0)
        for i in range(len(allnetworks)-1,-1,-1):
            allspecies[-1].members.append(allnetworks[i])
            allnetworks.pop(i)
                
    if(len(allspecies)<values.species_target):
        values.closeness -= 0.1 * (1-(len(allspecies)/values.species_target))
    elif(len(allspecies)>values.species_target):
        
        values.closeness += 0.3 * ((len(allspecies)/values.species_target)-1)

    if(values.closeness<0.2):
        values.closeness = 0.2


def evaulate():
    avg = 0 
    best = 0
    bests = {}
    bestunweighted = 0
    vstestamount = values.vs_species_amount
    for i in allspecies:
        a = i.evaluate()
        bests[a[0]] = i
        
            
    played = {}    
    done = {}
    if(len(bests) == 1):
        bests[list(bests)[0]].speciesavg = list(bests)[0].fitness
        avg = list(bests)[0].fitness
        best = list(bests)[0]
        bestunweighted = list(bests)[0]

    elif(len(bests) < 4):
        for i in bests:
            played[i] = 0
        for b in range(vstestamount):
            dic = list(played)
            tocopy = sample(dic, k = 4-len(played))  
            dic.extend(tocopy)
            ret = run(dic)
            for i in ret:
                bests[i].speciesavg += ret[i]
                played[i] += 1 
        for i in list(played):
           bests[i].speciesavg /= played[i] 
           if(best == 0 or bests[i].speciesavg > bests[best].speciesavg):
                best = i
                bestunweighted = i
           avg += bests[i].speciesavg
             
    else:
        for network in bests:
            played[network] = vstestamount
        while(len(played) != 0):
            dic = list(played)
            if(len(dic) >= 4):
                ret = run(sample(dic, k=4))
                for i in ret:
                    bests[i].speciesavg += ret[i]
                    played[i] -= 1
                    if(played[i] == 0):
                        done[i] = vstestamount
                        played.pop(i)

            else:
                finones =  sample(list(done), k = 4-len(dic))
                dic.extend(finones)
                ret = run(dic)
                for i in ret:
                    bests[i].speciesavg += ret[i]
                    if(i in finones):
                        done[i] += 1
                    else:
                        played[i] -= 1
                        if(played[i] == 0):
                            done[i] = vstestamount
                            played.pop(i)

        for i in list(done):
            bests[i].speciesavg /= done[i]

            if(best == 0 or bests[i].speciesavg > bests[best].speciesavg):
                best = i
                bestunweighted = i
            avg += bests[i].speciesavg 
                        
    #print(avg,best,bestunweighted)
    return avg,best,bestunweighted, len(allspecies)
    
def mutitate(avg, best):
    for i in allspecies:
        mut = i.mutitate(avg) 
        allnetworks.extend(mut)
    return 0


def setup():    
    global allnetworks
    for a in range(values.populationsize):
        allnetworks.append(network())
setup()
while(True):
    t = time()
    createspecies()
    t1 = time() - t
    #print(t1, "t1")
    if(len(allspecies) == 0):
        if(len(allnetworks) == 0):
            print("reset")
            setup()
            createspecies()
        else:
            continue
    avg, best, bestunweighted, numspecies = evaulate()
    t2 = time() - t1
    #print(t2, "t2")
    mutitate(avg, best)
    t3 = time() - t2
    #print(t3, "t3")
    t = time()-t
    savedata(avg/numspecies,best,bestunweighted,t, numspecies, t1,t2,t3)
    '''if(is_pressed('q')):
        break'''
    generation += 1
print("quit")
write_file.close()
plt.show()
