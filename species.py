from examples.xor import run 
import values
class species():

    def __init__(self, leader):
        self.rep = leader
        self.members = [leader]
        self.members_score = {}
        self.prevbestscore = []
        
    def evaluate(self):
        best = 0
        self.speciesavg = 0 
        for i in self.members:
            score =  run(i)/len(self.members)
            if(score > best):
                best = score
            self.members_score[i] = score
            self.speciesavg += score
        self.prevbestscore.append(best)
        return self.speciesavg

    def mutitate(self,globalavg):
        ret_nets = []
        numofnewpopulation = round((self.speciesavg/globalavg)*values.populationsize)
        if(numofnewpopulation> 1):
            print(max(self.members_score),self.members_score,numofnewpopulation,"YEEE")