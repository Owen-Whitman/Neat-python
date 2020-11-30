import activations
from copy import deepcopy
a = activations.ActivationFunctionSet()
class connectiongenes():
    def __init__(self,innode,outnode,innovation):
        self.innode = innode
        self.outnode = outnode
        self.innovation_number = innovation
    

class nodegenes():
    def __init__(self,types,innovation_number,activation,location):
        self.location = location
        self.value = 0
        self.type = types
        self.innovation_number = innovation_number
        self.activation_name = activation
        try:
            self.activation = a.get(activation)
        except:
            pass
            #print(a.get(activation))

    def copy(self):
        return deepcopy(self)