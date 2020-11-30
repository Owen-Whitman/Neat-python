
def run(net):
    score = 4
    a=net.feedforward([1,0,0])
    score -= (a[0]-0) **2

    score -= (net.feedforward([1,1,1])[0]-0)**2

    score -= (net.feedforward([1,1,0])[0]-1) ** 2

    score -= (net.feedforward([1,0,1])[0]-1) ** 2
    if(score < 0):
        score = 0

    return score

