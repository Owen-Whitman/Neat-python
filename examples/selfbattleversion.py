from math import dist
import random, select, keyboard, time, math
from time import sleep

maxhealth = 100
boardsize = 11

pointsforfirst = 30
pointsforsecond = 20
pointsforthird = 10
killing = 30
killingheadtohead = 40
timealive = 2.5
eating = 10
runningtoself = 0
runningintowall = 0

class character():
    def __init__(self, inheadx, inheady, incharacter, brain):
        self.character = incharacter
        self.size = 3
        self.realsize = 1
        self.eyesize = 9
        if(brain == 0):
            self.mode = False
        else:
            self.mode = True
            self.brain = brain
        self.health = maxhealth
        self.bodypos = [[inheadx,inheady]]
        self.score = 0 

    def getinput(self, board, oppontentshealth, foods):
        allin = [self.healthflattening(self.health)]
        eye = self.setupeye(board)
        
        for i in eye:
            allin.extend(i)
        check = True
        for i in oppontentshealth:
            i = i[1]
            if(not check or i.character != self.character):
                allin.append(i.bodypos[-1][0]-self.bodypos[-1][0])
                allin.append(i.bodypos[-1][1]-self.bodypos[-1][1])
            else:
                check = False
        
        allin.extend([self.wallflattening(self.bodypos[-1][0]), self.wallflattening(boardsize - self.bodypos[-1][0]),self.wallflattening(self.bodypos[-1][1]), self.wallflattening(boardsize -self.bodypos[-1][1])])
        food = [[0,0],[0,0],[0,0]]
        fooddistance = [0.0,0.0,0.0]
        for i in foods:
                holder = [i[0]-self.bodypos[-1][0],i[1]-self.bodypos[-1][1]]
                distance = math.sqrt(holder[0]**2 + holder[1]**2)
                if(distance<fooddistance[-1]):
                    continue
                else:
                    if(distance>fooddistance[0]):
                        food.insert(int(0),holder)
                        fooddistance.insert(int(0),distance)
                        food.pop(-1)
                        fooddistance.pop(-1)
                        continue
                    elif(distance>fooddistance[1]):
                        food.insert(1,holder)
                        fooddistance.insert(1,distance)
                        food.pop(-1)
                        fooddistance.pop(-1)
                        continue
                    else:
                        food.insert(2,holder)
                        fooddistance.insert(2,distance)
                        food.pop(-1)
                        fooddistance.pop(-1)
                        continue

        for i in food:
            allin.extend(i)
        
        if(self.mode):
            choices = [(1,(0,-1)),(2,(0,1)),(3,(-1,0)),(4,(1,0))]
            values = []
            for i in range(len(choices)):
                
                allin.append(choices[i][1][0])
                allin.append(choices[i][1][1])
                output = self.brain.feedforward(allin)[0]
                allin.pop(-1)
                allin.pop(-1)
                
                values.append(output)
            #print(values, values.index(max(values)), choices[values.index(max(values))][0])
            return choices[values.index(max(values))][0]
            
        else:
            print("press arrow key for character", self.character)
            inp = keyboard.read_key() 
            print(inp)
            time.sleep(0.1)
            if(inp == "w"):
                return 1
            if(inp == "s"):
                return 2
            if(inp == "a"):
                return 3
            if(inp == "d"):
                return 4

    def find_distance_food(self, food):
        closest = []
        head = self.bodypos[-1]
        for b in food:
            distance = math.sqrt((food[0]-head[0])**2 + (food[1]-head[1])**2 )
            if(len(closest[-1]) <= 2):
                closest[-1].append((food,distance))
                continue
            for c in range(len(closest)):
                if(distance>closest[c][1]):
                    closest.insert(c-1,(food,distance))
                    closest.pop(-1)
        return closest
    
    def setupeye(self,board):
        selfhead = self.bodypos[-1]
        addedsize= int((self.eyesize)/2)
        eye = []
        for i in range(selfhead[0]-addedsize,selfhead[0]+addedsize+1):              
            if(i <= 0 or i > boardsize):
                eye.append([0 for c in range(self.eyesize)])
            else:
                eye.append([])
                for b in range(selfhead[1]-addedsize,selfhead[1]+addedsize+1):
                    if(selfhead == [i,b]):
                        continue
                    if((b <= 0 or b > boardsize)):
                        eye[-1].append(0)
                        continue
                    elif( (board[i][b] == 0 or board[i][b] == -1 or board[i][b] == 'f')):
                        eye[-1].append(0)
                        continue
                    if(board[i][b] == self.character):
                        eye[-1].append(1)
                    else:
                       eye[-1].append(-1) 
        return eye
    
    def wallflattening(self, inp):
        ret = 1/(1+(math.exp((inp-5))*7))
        
        return ret
    
    def healthflattening(self, inp):
        return 1/(1+(math.exp((inp+10)/10)))
        
          
class board():
    def __init__(self,size, networks):
        self.board = [[-1 for i in range(size+2)]]
        self.characters = []
        self.killedcharacters = []
        self.size = size
        self.ticks = 0
        self.numfood = 0 
        self.movements = [(1,(0,-1)),(2,(0,1)),(3,(-1,0)),(4,(1,0))]
        self.foodlocations = []        
        for i in range(size):
            self.board.append([-1])
            for b in range(size):
                self.board[-1].append(0)
            self.board[-1].append(-1)
        self.board.append([-1 for i in range(size+2)])
        start_points = [2, int(size-1), int((size)/2)+1]
        start_positions  = []

        for i in start_points:
            for b in start_points:
                if( not(i == b and i == start_points[-1])):
                    start_positions.append((i,b))
        random.shuffle(start_positions)

        for i in range(len(networks)):
            a = character(start_positions[i][0],start_positions[i][1],i+1,networks[i])
            self.characters.append(a)
            self.board[start_positions[i][0]][start_positions[i][1]] = i+1
        self.addfood()

    def displayboard(self):
        for i in range(len(self.board)):
            print()
            for b in self.board[i]:
                if(b != -1):
                    print(b,end=" ")
        for i in self.characters:
            print("snake",str(i.character)+" \'s health:", str(i.health))
        print()

    def update(self):
        inps = [self.board,[], self.foodlocations]
        for i in self.characters:
            inps[1].append((i.health,i))

        for i in self.characters:
            inp = i.getinput(inps[0],inps[1],inps[2])
            for b in self.movements:
                if(inp == b[0]):
                    inp = b[1]
                    break
            checkcoll = self.checkcollisons(inp,i)
            if(checkcoll[0]):
                if(i.realsize == i.size):
                    self.board[i.bodypos[0][0]][i.bodypos[0][1]] = 0
                    i.bodypos.pop(0)
                else:
                    i.realsize += 1
                
                self.board[i.bodypos[-1][0]+inp[1]][i.bodypos[-1][1]+inp[0]] = i.character
                i.bodypos.append([i.bodypos[-1][0]+inp[1],i.bodypos[-1][1]+inp[0]])
                i.score += timealive
            elif(not checkcoll[1]):
                return (False, self.killedcharacters)
        self.addfood()
        return (True, 0)
    
    def checkcollisons(self, inp,i):
        inp = [i.bodypos[-1][0]+inp[1],i.bodypos[-1][1]+inp[0]]
        loc = self.board[inp[0]][inp[1]] 
        if(loc == "f"):
            i.size += 1
            i.score += eating
            i.health = maxhealth
            return (True, True)
        else:
            if(i.health == 1):
                return(False, self.kill(i))
            else:
                i.health -= 1
        if(loc != 0):
            if(loc == -1):
                i.score += runningintowall
                return (False, self.kill(i))
            if(loc == i.character):
                if(inp ==  i.bodypos[0] and len(i.bodypos) != 2):
                    return (True, True)
                i.score += runningtoself
                return (False, self.kill(i))    
            else:
                for b in self.characters:
                    if(b.character == loc):
                        if(b.bodypos[-1] == inp):
                            if(b.realsize > i.realsize):
                                b.score += killingheadtohead
                                return (False, self.kill(i))
                            elif(b.realsize == i.realsize):
                                self.kill(b)
                                return (False, self.kill(i))
                            else:
                                i.score += killingheadtohead
                                return (True, self.kill(b))
                        else:
                            b.score += killing
                            return(False, self.kill(i))
                print("error collided obj not found")
                raise(RuntimeError)
        else:
            return (True, True)

    def addfood(self):
        chance_of_food = 0.15
        addfood = False    
        if(self.numfood == 0):
            addfood = True
        elif(random.random()<= chance_of_food):
            addfood = True
        
        if(addfood):
            choice = random.choice(self.findemptysquares())
            self.numfood += 1
            self.board[choice[0]][choice[1]] = 'f'
            self.foodlocations.append((choice[0],choice[1]))

        
    def findemptysquares(self):
        possiblelocations = []
        for i in range(1,self.size+1):
            for b in range(1,self.size+1):
                possiblelocations.append([i,b])
        for i in self.characters:
            for b in i.bodypos:
                possiblelocations.remove(b)
        return possiblelocations
        
    def kill(self, character):
        for i in character.bodypos:
            self.board[i[0]][i[1]] = 0
        self.killedcharacters.append(character)
        self.characters.remove(character)
        if(len(self.characters) > 2):
            return True
        elif(len(self.characters) == 2):
            character.score += pointsforsecond
            return True
        elif(len(self.characters) == 3):
            character.score += pointsforthird
        elif(len(self.characters) == 1):
            self.characters[0].score += pointsforfirst
            #print("Character",str(self.characters[0].character),"won")
            self.killedcharacters.append(self.characters[0])
            return False
        else:
            #print("No characters left. No winner")
            return False
                

def run(networks):
    a = board(boardsize,networks)
    while True:
        up = a.update()
        #print(up)
        #a.displayboard()
        if(not up[0]):
            break
    ret = {}
    for i in up[1]:
        if(i.score < 0):
            i.score = 0
        ret[i.brain] = i.score
    #print(ret)
    return ret