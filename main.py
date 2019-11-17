from network import network
import values

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
        allconnectiongenes.append(ret)
        totalconnectiongenes += 1

        
def mutitateaconnection(net):
    global totalconnectiongenes, totalnodegenes, allsplitnodes
    ret = net.mutitateconnection(totalnodegenes,totalconnectiongenes,allsplitnodes)
    if(ret == None):
        addaconnection(net)
    elif(ret not in allsplitnodes):
        allsplitnodes.append(ret)
        totalconnectiongenes += 2
        totalnodegenes += 1


net = network()
addaconnection(net)
addaconnection(net)
addaconnection(net)
addaconnection(net)
mutitateaconnection(net)
mutitateaconnection(net)
mutitateaconnection(net)
mutitateaconnection(net)
print(net.nodegenes,net.connectiongenes)
net.feedforward([1,2])