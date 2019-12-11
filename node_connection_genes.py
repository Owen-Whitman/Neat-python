import activations

a = activations.ActivationFunctionSet()
class connectiongenes():
    def __init__(self,innode,outnode,weight,enabled,innovation):
        self.innode = innode
        self.outnode = outnode
        self.weight = weight
        self.enabled = enabled
        self.innovation_number = innovation
    def copy(self):
        return connectiongenes(self.innode,self.outnode,self.weight,self.enabled,self.innovation_number)

class nodegenes():
    def __init__(self,types,innovation_number,activation):
        self.type = types
        self.innovation_number = innovation_number
        self.activation_name = activation
        try:
            self.activation = a.get(activation)
        except:
            print(a.get(activation))

    def copy(self):
        return nodegenes(self.type,self.innovation_number,self.activation_name)