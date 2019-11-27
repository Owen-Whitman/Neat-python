from network import network
import values


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
a = createtestnet()
b= createtestnet()
print(closeness(a,b))