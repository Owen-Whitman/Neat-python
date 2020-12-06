from random import random
from node_connection_genes import connectiongenes
numofinputs = 99
numofoutputs = 1

activationfunctioninput = 'sigmoid'
activationfunctionmain = 'sigmoid'
activationfunctionoutinput = 'sigmoid'
weightminmax = [-2,2]

c1 = 1
c2 = 1.2
c3 = 0.1
species_target = 20
inherit_desabled = 0.75
added_connection_chace = 0.075
mutitate_connection_chace = 0.01
weight_prebutered_chance = 0.9
weight_prebutered_added = 0.075
weight_random_chance = 0.025
weight_mutitated_chance = 0.8

top_reproduce = 0.5
populationsize = 300
closeness = 1

interspeciestestamount = 15
vs_species_amount = 15

totalnodegenes = 0
totalconnectiongenes = 0
allconnectiongenes = []
allsplitnodes = []
def setup():
    global allconnectiongenes, totalnodegenes, totalconnectiongenes, populationsize, allsplitnodes
    allconnectiongenes = []
    allsplitnodes = []
    totalconnectiongenes = 0 
    totalnodegenes = 0
    totalnodegenes = numofinputs + numofoutputs
    for i in range(numofinputs):
        for b in range(numofoutputs):
            allconnectiongenes.append({'from':i,'to':numofinputs+b, 'class':connectiongenes(i,numofinputs+b,totalconnectiongenes), 'inno': totalconnectiongenes})
            totalconnectiongenes +=  1

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
    ret = net.mutitateconnection(totalnodegenes,totalconnectiongenes,allsplitnodes,allconnectiongenes)
    #print(ret,"ret")
    if(ret == "Na"):
        addaconnection(net)
    elif(ret != None ):
        allsplitnodes.append(ret)
        allconnectiongenes.append({'from':ret['from'],'to':ret['nodeinno'],'inno':ret['connectioninno'],'class':ret['connection1class']})
        allconnectiongenes.append({'from':ret['nodeinno'],'to':ret['to'],'inno':ret['connectioninno']+1,'class':ret['connection2class']})
        totalconnectiongenes += 2
        totalnodegenes += 1
