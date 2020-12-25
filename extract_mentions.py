import json
import sys
from collections import Counter, defaultdict


with open('synonyms.json') as f:
    SYNONYMS = json.load(f)


def main():
    for line in sys.stdin:
        mentions = defaultdict(set)
        data = json.loads(line)

        for ne in data['ner']:
            start, end, type = ne
            mention = ' '.join(data['words'][start:end]).lower()
            mention = SYNONYMS.get(mention, mention)    # normalize by the synonym dict
            mentions[type].add(mention)
        
        data['mentions'] = {t: list(ms) for t, ms in mentions.items()}

        print(json.dumps(data))


if __name__ == '__main__':
    main()
