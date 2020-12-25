import argparse
import json
import spacy
nlp = spacy.load('en_core_web_sm')
import sys
import re


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', type=int)
    args = parser.parse_args()

    for line in sys.stdin:
        data = json.loads(line)
        if data['published_parsed'][0] != args.year:
            continue

        words = []
        sentences = []

        title = data['title']
        title = re.sub('\n +', ' ', title)
        summary = data['summary'].replace('\n', ' ')

        tokens = [t.text for t in nlp(title)]
        sentences.append((len(words), len(words)+len(tokens)))
        words.extend(tokens)
        for sent in nlp(summary).sents:
            tokens = [t.text for t in nlp(sent.text, disable=["parser"])]
            sentences.append((len(words), len(words)+len(tokens)))
            words.extend(tokens)

        doc_id = f"{data['id']}/{data['published_parsed'][0]}/{data['published_parsed'][1]}"

        result = {
            'doc_id': doc_id,
            'words': words,
            'sentences': sentences,
            'sections': [[0, len(words)]],
            'n_ary_relations': []
        }

        print(json.dumps(result))

if __name__ == '__main__':
    main()
