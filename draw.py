import pygame
from math import sqrt, floor,ceil

length = 600
width = 600
background = None
test_nodefromto = None
test_layers = None
layers_radius = None
nodes = None
points = None
test_layerslist = None
seperation = None

class node:
    def __init__(self,x,y,radius,color,surface,name):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
          
        self.surface = surface
        if(x == 0):
            pygame.draw.circle(surface, pygame.Color(0, 0, 0),(radius+x,y),radius,1)
        elif(x == length):
            pygame.draw.circle(surface, pygame.Color(0, 0, 0),(x-radius,y),radius,1)
        else:
            pygame.draw.circle(surface, pygame.Color(0, 0, 0),(x,y),radius,1)

        if(radius> 1 and color != None):
            if(x == 0):
                pygame.draw.circle(surface, color,(radius+x,y),radius-1,0)
            elif(x == length):
                pygame.draw.circle(surface, color,(x-radius,y),radius-1,0)
            else:
                pygame.draw.circle(surface, color,(x,y),radius-1,0)
        if(name != None):
            font_obj = pygame.font.Font('freesansbold.ttf', 32)
            text_surface_obj = font_obj.render(str(name), True, pygame.Color(0, 0, 0), surface)
            text_rect_obj = text_surface_obj.get_rect()
            if(x == 0):
                text_rect_obj.center = (x+radius, y)
            else:
                text_rect_obj.center = (x, y)
            surface.blit(text_surface_obj, text_rect_obj)

class connect:
    def __init__(self,node1,node2,color,surface):
        if(node1.x == 0):
            if(color == None):
                pygame.draw.line(surface,pygame.Color(0, 0, 0),((node1.radius*2)+node1.x,node1.y),(node2.x-(node2.radius),node2.y),2)
            else:
                pygame.draw.line(surface,color,((node1.radius*2)+node1.x,node1.y),(node2.x-(node2.radius),node2.y),2)
        else:
            if(color == None):
                pygame.draw.line(surface,pygame.Color(0, 0, 0),((node1.radius)+node1.x,node1.y),(node2.x-(node2.radius),node2.y),2)
            else:
                pygame.draw.line(surface,color,((node1.radius)+node1.x,node1.y),(node2.x-(node2.radius),node2.y),2)
        '''slope = (node1.y-node2.y)/(node1.x-node2.x)
        print(slope)
        move = 50/sqrt(2)
        pygame.draw.polygon(surface,pygame.Color(255,0,0),
                            [
                                ((node1.x+node2.x)/2-25,(node1.y+node2.y)/2-(slope*25)),
                                ((node1.x+node2.x)/2-25-move,(node1.y+node2.y)/2-(slope*25)-move),
                                ((node1.x+node2.x)/2,(node1.y+node2.y)/2),
                                ((node1.x+node2.x)/2-25-move,(node1.y+node2.y)/2-(slope*25)+move)
                            ]

                            )'''


def decidecolor(weight):
    print(weight)
    if(weight == 1):
        return None
    if(weight == 0):
        return pygame.Color(255,255,255)
    if(weight < 0):
        minum = 150
        maxval = 4
        mutplier = ((255-minum)/maxval)
        colorshade = round(mutplier*abs(weight)+minum)
        if(colorshade > 255):
            colorshade = 255
        return pygame.Color(colorshade,0,0)
    else:
        minum = 100
        maxval = 7
        mutplier = ((255-minum)/maxval)
        colorshade = round(mutplier*abs(weight)+minum)
        if(colorshade > 255):
            colorshade = 255

        return pygame.Color(0,colorshade,0)

def addconnectionlayer(connectionlayer):
    nodes[connectionlayer] = {}
    solved = False
    guess = layers_radius[connectionlayer]
    between = []
    while solved == False:
        goal = len(test_layers[connectionlayer])
        counter = 0
        if(guess <= 1):
            raise ValueError
            print("not possible")

        if(points[connectionlayer][1]-guess > (guess * 2)):
            goal =- floor((points[connectionlayer][1]-1)/(guess * 2))
            if(goal <= 0):
                if(not solved):
                    between.append(len(test_layers[connectionlayer])-counter)
                    counter = len(test_layers[connectionlayer])
                    solved = True
                    break
                else:
                    between.append(floor((points[connectionlayer][1]-1)/(guess * 2)))
                    counter += floor((points[connectionlayer][1]-1)/(guess * 2))
        else:
            between.append(0)
            
        for i in range(2,len(points[connectionlayer])):
            if(points[connectionlayer][i] - points[connectionlayer][i-1]-1 > guess * 2):
                goal =- floor((points[connectionlayer][i] - points[connectionlayer][i-1]-1 )/ guess * 2)
                if(goal <= 0):
                    if(not solved):
                        between.append(len(test_layers[connectionlayer])-counter)
                        counter = len(test_layers[connectionlayer])
                        solved = True
                    break
                else:
                    between.append(floor((points[connectionlayer][i] - points[connectionlayer][i-1]-1 )/ guess * 2))
                    counter += floor((points[connectionlayer][i] - points[connectionlayer][i-1]-1 )/ guess * 2)
            else:
                between.append(0)
        print(between,goal,counter)
        if(width - points[connectionlayer][-1]-1 > (guess * 2)):
            goal =- floor((width-points[connectionlayer][0]-1)/(guess * 2))
            if(goal <= 0):
                if(not solved):
                    between.append(len(test_layers[connectionlayer])-counter)
                    solved = True
                break
            else:
                between.append(floor((width-points[connectionlayer][0]-1)/(guess * 2 )))
                counter += floor((width-points[connectionlayer][0]-1)/(guess * 2))
        else:
            between.append(0)
        if(goal <= 0):
            solved = True
        else:
            guess -= 5

    added = 0
    for i in range(len(between)):
        if(between[i] == 0):
            continue
        print(between[i],between)
        for b in range(0,between[i]):
            print(b)
            nodes[connectionlayer][test_layers[connectionlayer][added]] = node((test_layerslist.index(connectionlayer))*seperation,guess+points[connectionlayer][i]+(guess*2+10)*b,guess,None,background,test_layers[connectionlayer][added])
            added += 1


def drawit(net):
    global nodes,layers_radius,test_layers,test_nodefromto,background,points,test_layerslist,seperation

    pygame.display.init()
    pygame.init()
    pygame.display.set_caption('Quick Start')

    window_surface = pygame.display.set_mode((length, width))


    background = pygame.Surface((length, width))
    background.fill(pygame.Color(255, 255, 255))

    test_nodefromto = net.nodefromto
    test_layers = net.layers
    nodes = {'0.0':{}}
    connections = []
    test_layersrev = list(reversed([i for i in test_layers]))
    test_layerslist = [i for i in test_layers]
    print(test_layersrev,test_layerslist)
    test_layersrev.pop(-1)
    avgsize = 55
    layers_radius = {}
    if((avgsize*2) * len(test_layers)+ avgsize + 10*len(test_layers) > width):
        print("HERERERERRERDFHJBSKDF")
        avgsize = floor((width-(10*(len(test_layers)))-avgsize)/(len(test_layers)*2))
        print(avgsize)
    else:
        print((avgsize*2) * len(test_layers)+ avgsize + 10*len(test_layers),"YURD")
    points = {}
    for i in test_layers:
        points[i] = [0]

    seperation = round(length/(len(test_layers)-1))

    print(avgsize,len(test_layers))
    print(seperation)

    if(True):
        for i in test_layers:
            max_rad = floor((width-(10*(len(test_layers[i])-1)))/(len(test_layers[i])*2))
            print(max_rad,"max_rad")
            if(max_rad<avgsize):
                layers_radius[i] = max_rad
            else:
                layers_radius[i] = avgsize

        count = 0
        sepsize = floor((width-((layers_radius['0.0']*2)*len(test_layers['0.0'])))/len(test_layers['0.0']))
        print(sepsize)
        for i in test_layers['0.0']:
            b = '0.0'
            nodes[b][i] = (node(0,(count*layers_radius[b])*2+layers_radius[b]+(sepsize*count),layers_radius[b],None,background,test_layers['0.0'][count]))
            count += 1

        count = 1
        nodes['1.0'] = {}
        sepsize = floor((width)/(len(test_layers['1.0'])*2))

        for i in test_layers['1.0']:
            b = '1.0'
            print(sepsize,"sep",count)
            nodes[b][i] = node(length-layers_radius[b],(sepsize*count),layers_radius[b],None,background,test_layers['1.0'][count-1])
            count += 1


    for globallayer in test_layersrev:
        for addtonode in test_layers[globallayer]:
            for connectionlayer in test_layers:
                if(globallayer== connectionlayer):
                    break
                
       
                crossedpath = test_layerslist[test_layerslist.index(connectionlayer)+1:test_layerslist.index(globallayer)]
                
                for connection in test_layers[connectionlayer]:
                    
                    if(connection in test_nodefromto[addtonode]):
                        if(connectionlayer not in nodes):
                            addconnectionlayer(connectionlayer)
                        
                        color = decidecolor(test_nodefromto[addtonode][connection])

                        connections.append(connect(nodes[connectionlayer][connection],nodes[globallayer][addtonode],color,background))
                        slope = (nodes[connectionlayer][connection].y-nodes[globallayer][addtonode].y)/(nodes[connectionlayer][connection].x-nodes[globallayer][addtonode].x)
                        diffval = slope*-nodes[connectionlayer][connection].x + nodes[connectionlayer][connection].y
                        if(slope == 0):

                            for crossedlists in crossedpath:
                                points[crossedlists].append(nodes[connectionlayer][connection].y)

                        else:
                            for crossedlists in crossedpath:
                                points[crossedlists].append(round((slope * (seperation*test_layerslist.index(crossedlists))+diffval)))
                #print(points)


    is_running = True
    window_surface.blit(background, (0, 0))
    pygame.display.update()


    print("done")
    while is_running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False



    pygame.display.quit()