import json
import sys
from collections import defaultdict, Counter
from scipy.stats import chisquare


def main():
    mention_counts = defaultdict(Counter)
    mode = sys.argv[1]
    assert mode in {'yearly', 'yearly-test', 'monthly'}

    for line in sys.stdin:
        data = json.loads(line)

        year, month = data['doc_id'].split('/')[-2:]
        for type, mentions in data['mentions'].items():
            if mode == 'yearly':
                key = (year, type)
            elif mode == 'yearly-test':
                key = year
            elif mode == 'monthly':
                month = int(month)
                key = f'{year}/{month:02d}'

            mention_counts[key].update(mentions)
    
    if mode == 'yearly':
        for key, counts in mention_counts.items():
            print(key)
            for m, c in counts.most_common(100):
                print('\t', m, c)

    elif mode == 'yearly-test':
        total_2019 = sum(mention_counts['2019'].values())
        total_2020 = sum(mention_counts['2020'].values())
        total = total_2019 + total_2020
        print('total', total_2019, total_2020)
        for m, obs2 in mention_counts['2020'].most_common(100):
            obs1 = mention_counts['2019'][m]
            exp1 = (obs1 + obs2) * (total_2019 / total)
            exp2 = (obs1 + obs2) * (total_2020 / total)

            _, p = chisquare([obs1, obs2], [exp1, exp2])

            sign = ''
            if obs2 > exp2 and p < .01:
                sign = 'up**'
            if obs2 < exp2 and p < .01:
                sign = 'down**'

            print(f'{m}\t{obs1}\t{obs2}\t{exp1:.0f}\t{exp2:.0f}\t{p:4.3f}\t{sign}')

    elif mode == 'monthly':
        total_2020_counter = Counter()
        sorted_keys = sorted(mention_counts.keys())
        papers_per_month = {}
        for key, counts in mention_counts.items():
            papers_per_month[key] = sum(counts.values())
            if key.startswith('2020'):
                total_2020_counter.update(counts)
        
        for m, _ in total_2020_counter.most_common(100):
            print(m, ','.join('{:3.2f}'.format(100. * mention_counts[key][m] / papers_per_month[key]) for key in sorted_keys)) 


if __name__ == '__main__':
    main()

    