import sys
from collections import defaultdict

counts = defaultdict(lambda:0)
context_counts = defaultdict(lambda:0)
a = 0

for line in open('wiki-en-train.word'):
    words = line.split()
    words.append('</s>')
    words.insert(0,'<s>')
    for i in range(1,len(words)):
        counts[words[i-1] + ' ' +  words[i]] += 1
        context_counts[words[i-1]] += 1
        counts[words[i]] += 1
        context_counts[''] += 1
        a += 1 
print(context_counts[""])
print(a)
model_file = open('model_file_ngram.txt','w')

for ngram, count in sorted(counts.items()):
    words = ngram.split()
    words.pop()
    context = ''.join(words)
    probability = counts[ngram]/context_counts[context]
    model_file.write(str(ngram) + '\t' + str(probability) + '\n')

