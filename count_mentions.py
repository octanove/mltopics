import json
import sys
from collections import Counter, defaultdict


def main():
    ne_counts = defaultdict(Counter)
    for line in sys.stdin:
        mentions = defaultdict(set)
        data = json.loads(line)

        for ne in data['ner']:
            start, end, type = ne
            phrase = ' '.join(data['words'][start:end]).lower()
            mentions[type].add(phrase)
        
        for t, m in mentions.items():
            ne_counts[t].update(m)

    for type, counts in ne_counts.items():
        print(type)
        for ne, c in counts.most_common(15):
            print('\t', ne, c)

if __name__ == '__main__':
    main()
