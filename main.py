from network import network
numofinputs = 2
numofoutputs = 2
totalnodegenes = 4
totalconnectiongenes = 1
allconnectiongenes = []
allsplitnodes = []

def addaconnection(net):
    global totalconnectiongenes, allconnectiongenes
    print(totalconnectiongenes,'connection')
    ret = net.addconnection(totalconnectiongenes,allconnectiongenes)
    if(ret == 'impossible'):
        mutitateaconnection(net)
    elif(ret not in allconnectiongenes):
        print("not")
        allconnectiongenes.append(ret)
        totalconnectiongenes += 1
    print("here")
        
def mutitateaconnection(net):
    global totalconnectiongenes, totalnodegenes, allsplitnodes
    ret = net.mutitateconnection(totalnodegenes,totalconnectiongenes,allsplitnodes)
    if(ret == None):
        addaconnection(net)
    elif(ret not in allsplitnodes):
        print("not")
        allsplitnodes.append(ret)
        totalconnectiongenes += 2
        totalnodegenes += 1
    print("here")
