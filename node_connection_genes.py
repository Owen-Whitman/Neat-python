class connectiongenes():
    def __init__(self,innode,outnode,weight,enabled,innovation):
        self.innode = innode
        self.outnode = outnode
        self.weight = weight
        self.enabled = enabled
        self.innovation_number = innovation

class nodegenes():
    def __init__(self,types,innovation_number):
        self.type = types
        self.innovation_number = innovation_number