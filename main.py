from network import network
from species import species
import values

allnetworks = []
allspecies = []

def closeness(net1, net2):
    print(net1.nodefromto,net2.nodefromto)
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
    values.addaconnection(net)
    values.addaconnection(net)
    values.mutitateaconnection(net)
    net.mutitate()
    return net

for i in range(5):
    a = network()
    '''
    for i in a.nodegenes:
        print(i.innovation_number,i.type)
    
    for i in a.connectiongenes:
        print(i.innode,i.outnode,i.weight,i.enabled,i.innovation_number)'''
    allnetworks.append(a)

for mainstuff in range(0,1):
    print(mainstuff)
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
    print("sorted")
    print(allnetworks,allspecies)

    avg = 0 
    for i in allspecies:
        if(len(i.members) == 0): 
            allnetworks.append(i.members)
            allspecies.remove(i)
            continue
        if(len(i.prevbestscore)>=15 and max(i.prevbestscore[:len(i.prevbestscore)-14])>= max(i.prevbestscore[len(i.prevbestscore)-14:])):
            allnetworks.append(i.members)
            allspecies.remove(i)
            continue
        print("evaulating")
        i.evaluate()
        avg += i.evaluate()
    for i in allspecies:
        for b in i.mutitate(avg):
            allnetworks.append(b)

    print(allnetworks,allspecies)

