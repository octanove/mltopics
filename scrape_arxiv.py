import arxiv
import json
import sys


def main():
    for i in range(0, 50000, 1000):
        num_dumped = 0

        while num_dumped != 1000:
            papers = []

            print(f'Running query starting {i}...', file=sys.stderr)
            result = arxiv.query(
                query='cat:cs.AI',
                start=i,
                sort_by='submittedDate',
                sort_order='descending',
                max_chunk_results=1000,
                max_results=1000,
                iterative=True
            )

            for paper in result():
                num_dumped += 1
                papers.append(paper)

            print(f'Number of returned papers: {num_dumped}', file=sys.stderr)

        for paper in papers:
            print(json.dumps(paper))


if __name__ == '__main__':
    main()
