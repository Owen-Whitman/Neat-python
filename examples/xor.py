
def run(net):
    score = 4
    score -= net.feedforward([1,0,0])[0]
    print(score)
    score -= net.feedforward([1,1,1])[0]
    print(score)
    score -= 1-net.feedforward([1,1,0])[0]
    print(score)
    score -= 1-net.feedforward([1,0,1])[0]
    print(score)
    return score