from random import random
from node_connection_genes import connectiongenes
numofinputs = 3
numofoutputs = 1

activationfunctioninput = 'sigmoid'
activationfunctionmain = 'sigmoid'
activationfunctionoutinput = 'sigmoid'
weightminmax = [-2,2]

c1 = 1
c2 = 1 
c3 = 0.4
species_target = 10
inherit_desabled = 0.75
added_connection_chace = 0.02
mutitate_connection_chace = 0.015
weight_prebutered_chance = 0.8
weight_prebuted_added = 0.2
weight_random_chance = 0.1

top_reproduce = 0.5
populationsize = 150
closeness = 3

totalnodegenes = 4
totalconnectiongenes = 3
allconnectiongenes = [{'from':0,'to':3,'inno':0,'class':connectiongenes(0,3,0)},{'from':1,'to':3,'inno':1,'class':connectiongenes(1,3,1)},{'from':2,'to':3,'inno':2,'class':connectiongenes(2,3,2)}]
allsplitnodes = []

def addaconnection(net):
    global totalconnectiongenes, allconnectiongenes
    ret = net.addconnection(totalconnectiongenes,allconnectiongenes)
    for i in range(len(net.enabledgenes)):
        if(net.enabledgenes[i] in net.enabledgenes[0:i] or net.enabledgenes[i] in net.enabledgenes[i+1:0]):
            raise ValueError
    if(ret == 'impossible'):
        if(random() < mutitate_connection_chace):
            mutitateaconnection(net)
    elif(ret != None):
        allconnectiongenes.append(ret)
        totalconnectiongenes += 1
        
def mutitateaconnection(net):
    global totalconnectiongenes, totalnodegenes, allsplitnodes
    ret = net.mutitateconnection(totalnodegenes,totalconnectiongenes,allsplitnodes)
    for i in range(len(net.enabledgenes)):
        if(net.enabledgenes[i] in net.enabledgenes[0:i] or net.enabledgenes[i] in net.enabledgenes[i+1:0]):
            print(i)
            raise ValueError
    if(ret == "Na"):
        addaconnection(net)
    elif(ret != None ):
        allsplitnodes.append(ret)
        allconnectiongenes.append({'from':ret['from'],'to':ret['nodeinno'],'inno':ret['connectioninno'],'class':ret['connection1class']})
        allconnectiongenes.append({'from':ret['nodeinno'],'to':ret['to'],'inno':ret['connectioninno']+1,'class':ret['connection2class']})
        totalconnectiongenes += 2
        totalnodegenes += 1
