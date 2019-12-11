from examples.xor import run 
import values
from random import random, choice
import network
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
        return self.speciesavg, best

    def mutitate(self,globalavg):
        ret_nets = []
        numofnewpopulation = round((self.speciesavg/globalavg)*values.populationsize)
        if(numofnewpopulation> 1):
            maxx = 0 
            maxxscore = 0 
            for i in self.members_score:
                if(self.members_score[i]>maxxscore):
                    maxxscore = self.members_score[i]
                    maxx = i
            numofnewpopulation -= 1
             
            print(maxx,maxxscore,"KSJDFOSHDFN")
        for i in self.members:
            i.mutitate()
        onforthofpop = round(numofnewpopulation/4)
        print(onforthofpop,numofnewpopulation,"YEEE HAW",numofnewpopulation/4)
        while onforthofpop > 0:
            for i in self.members_score:
                print(self.members_score[i]/self.speciesavg)
                if((self.members_score[i]/self.speciesavg)>= random() or (self.members_score[i]/self.speciesavg) == 1):
                    print("madeit")
                    ret_nets.append(i)
                    onforthofpop -= 1
        numofnewpopulation -= onforthofpop 
        print(numofnewpopulation,"25% tooketh")
        while(numofnewpopulation>0):
            person1 = None
            person2 = None
            while (person1 == None or person2 == None):
                for i in self.members_score:
                    print(self.members_score[i]/self.speciesavg)
                    if(((self.members_score[i]/self.speciesavg)>= random() and (person1 != i or person2 != i)) or (self.members_score[i]/self.speciesavg) == 1):
                        if(person1 == None):
                            person1 = i 
                        else:
                            person2 = i
                print(person1,person2)
            print(person1,person2,"P1,p2",numofnewpopulation)
            ret_nets.append(network.network(parent1 = person1,parent2=person2))
            numofnewpopulation -= 1
        print(ret_nets)
        print(numofnewpopulation,"numofnewpopulation")
        self.leader = choice(self.members)
        print(self.leader)
        self.members = []
        self.members_score = {}
        return ret_nets
            #print(max(self.members_score),self.members_score,numofnewpopulation,"YEEE")
