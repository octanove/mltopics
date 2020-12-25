import json
import sys
from collections import defaultdict, Counter


def main():
    mention_counts = defaultdict(Counter)

    for line in sys.stdin:
        data = json.loads(line)

        year, month = data['doc_id'].split('/')[-2:]
        for type, mentions in data['mentions'].items():
            key = (year, type)

            mention_counts[key].update(mentions)
        
    for key, counts in mention_counts.items():
        print(key)
        for m, c in counts.most_common(100):
            print('\t', m, c)

if __name__ == '__main__':
    main()

    