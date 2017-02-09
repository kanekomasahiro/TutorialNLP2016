from collections import defaultdict
import math

emission = {}
transition = {}
possible_tags = {}
V = 1000000
lunk = 0.05

for line in open('hmm_model_file.txt'):
    types, context, word, prob = line.split()
    possible_tags[context] = 1
    if types == 'T':
        transition[context + ' ' + word] = float(prob)
    else:
        emission[context + ' ' + word] = float(prob)

for line in open('05-test-input.txt'):
    word = line.strip().split()
    I = len(word)
    best_edge = {}
    best_score = {}
    best_score['0 <s>'] = 0
    best_edge['0 <s>'] = None
    for i in range(I):
        for prev in possible_tags.keys():
            for nexts in possible_tags.keys():
                if best_score.get(str(i) + ' ' + prev) != None:
                    if transition.get(prev + ' ' + nexts) != None:
                        if emission.get(word[i] + ' ' + nexts) != None:
                            prob = (0.95 * float(emission[word[i] + ' ' + nexts]) + lunk/V)
                        else:
                            prob = lunk/V
                        print(word[i],prob)
                        score = best_score[str(i) + ' ' + prev] + -math.log(transition[prev + ' ' + nexts]) + -math.log(prob)
                        if best_score.get(str(i+1) + ' ' + nexts) == None or best_score[str(i+1) + ' ' + nexts] < score:
                            best_score[str(i+1) + ' ' + nexts] = score
                            best_edge[str(i+1) + ' ' + nexts] = str(i) + ' ' + prev

    for prev in possible_tags.keys():
        if best_score.get(str(I) + ' ' + prev) != None:
            if transition.get(prev + ' ' + '</s>') != None:
                score = best_score[str(I) + ' ' + prev] + -math.log(transition[prev + ' ' + '</s>'])
                if best_score.get(str(I+1) + ' ' + '</s>') == None or best_score[str(I+1) + ' ' + '</s>'] < score:
                    best_score[str(I+1) + ' ' + '</s>'] = score
                    best_edge[str(I+1) + ' ' + '</s>'] = str(I) + ' ' + prev
    print(best_edge, 'dddddd',best_score)
    tags = []
    next_edge = best_edge[str(I+1) + ' ' + '</s>']
    while next_edge != '0 <s>':
        position, tag = next_edge.split()
        tags.append(tag)
        next_edge = best_edge[next_edge]
    tags.reverse()
    print(' '.join(tags))




