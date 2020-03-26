from random import random
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
added_connection_chace = 0.01
mutitate_connection_chace = 0.005
weight_prebutered_chance = 0.8
weight_prebuted_added = 0.2
weight_random_chance = 0.1
n = 1
top_reproduce = 0.5
populationsize = 150
closeness = 3

totalnodegenes = 4
totalconnectiongenes = 3
allconnectiongenes = [{'from':0,'to':3,'inno':0},{'from':1,'to':3,'inno':1},{'from':2,'to':3,'inno':2}]
allsplitnodes = []

def addaconnection(net):
    global totalconnectiongenes, allconnectiongenes
    ret = net.addconnection(totalconnectiongenes,allconnectiongenes)
    if(ret == 'impossible'):
        pass
        '''if(random() < mutitate_connection_chace):
            mutitateaconnection(net)'''
    elif(ret not in allconnectiongenes):
        allconnectiongenes.append(ret)
        totalconnectiongenes += 1
        
def mutitateaconnection(net):
    global totalconnectiongenes, totalnodegenes, allsplitnodes
    ret = net.mutitateconnection(totalnodegenes,totalconnectiongenes,allsplitnodes)
    if(ret == None):
        addaconnection(net)
    elif(ret not in allsplitnodes):
        allsplitnodes.append(ret)
        allconnectiongenes.append({'from':ret['from'],'to':ret['nodeinno'],'inno':ret['connectioninno']})
        allconnectiongenes.append({'from':ret['nodeinno'],'to':ret['to'],'inno':ret['connectioninno']+1})
        totalconnectiongenes += 2
        totalnodegenes += 1
